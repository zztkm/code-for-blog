package main

import (
	"database/sql"
	"encoding/csv"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/godror/godror"
	"github.com/labstack/echo/v4"
)

func fatal(format string, err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, format, err)
	} else {
		fmt.Fprint(os.Stderr, format)
	}
	os.Exit(1)
}

func dbFromEnv() *sql.DB {
	var P godror.ConnectionParams
	P.Username = os.Getenv("USER")
	P.Password = godror.NewPassword(os.Getenv("PASS"))
	P.ConnectString = fmt.Sprintf("%s:%s/%s", os.Getenv("HOST"), os.Getenv("PORT"), os.Getenv("SERVICE"))
	P.SessionTimeout = 42 * time.Second
	return sql.OpenDB(godror.NewConnector(P))
}

func dbFromTnsora(conn string) (*sql.DB, error) {
	parts := strings.FieldsFunc(conn, func(r rune) bool {
		return r == '/' || r == '@'
	})

	if len(parts) != 3 {
		return nil, errors.New("invalid input format")
	}
	var P godror.ConnectionParams
	P.Username = parts[0]
	P.Password = godror.NewPassword(parts[1])
	P.ConnectString = parts[2]
	P.SessionTimeout = 42 * time.Second
	return sql.OpenDB(godror.NewConnector(P)), nil
}

type ExportRequest struct {
	Table   string `json:"table"`
	Outfile string `json:"outfile"`
}

type App struct {
	db *sql.DB
}

func (app App) export(c echo.Context) error {
	var req ExportRequest
	if err := c.Bind(&req); err != nil {
		return c.String(500, fmt.Sprintf("failed to bind request: %s\n", err))
	}

	countQuery := "SELECT COUNT(1) FROM " + req.Table
	var count int
	err := app.db.QueryRow(countQuery).Scan(&count)
	if err != nil {
		return c.String(500, fmt.Sprintf("failed to query: %s\n", err))
	}

	// 書き出し用csv
	file, err := os.Create(filepath.Join("/data", req.Outfile))
	if err != nil {
		fatal("failed to create file: %s\n", err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	q := fmt.Sprintf("SELECT * FROM %s ORDER BY LS_SEQ", req.Table)
	rows, err := app.db.Query(q)
	if err != nil {
		return c.String(500, fmt.Sprintf("failed to query: %s\n", err))
	}

	columns, err := rows.Columns()
	colsLen := len(columns)
	if err != nil {
		return c.String(500, fmt.Sprintf("failed to get columns: %s\n", err))
	}
	values := make([]sql.NullString, colsLen)
	for rows.Next() {
		valuePointers := make([]interface{}, colsLen)
		for i := range values {
			valuePointers[i] = &values[i]
		}
		err = rows.Scan(valuePointers...)
		if err != nil {
			return c.String(500, fmt.Sprintf("failed to scan row: %s\n", err))
		}
		data := make([]string, colsLen)
		for i, value := range values {
			if value.Valid {
				data[i] = value.String
			} else {
				data[i] = ""
			}
		}
		err := writer.Write(data)
		if err != nil {
			return c.String(500, fmt.Sprintf("failed to write string: %s\n", err))
		}
	}
	return nil
}

func initDB() *sql.DB {
	conn := dbFromEnv()
	//err := conn.Ping()
	//if err != nil {
	//	fatal("failed to ping connection: %s\n", err)
	//}
	return conn
}

func initEcho() *echo.Echo {
	app := App{
		db: initDB(),
	}
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		return c.String(200, "Hello, World!")
	})
	e.GET("/ping", func(c echo.Context) error {
		err := app.db.Ping()
		if err != nil {
			// TODO: エラー内容をそのまま返すのはセキュリティ的によくないので
			// エラー内容を隠蔽するようにする
			return c.String(500, fmt.Sprintf("failed to ping connection: %s\n", err))
		}
		return c.String(200, "pong")
	})
	e.POST("/export", app.export)
	return e
}

func main() {
	e := initEcho()
	e.Logger.Fatal(e.Start(":1323"))
}
