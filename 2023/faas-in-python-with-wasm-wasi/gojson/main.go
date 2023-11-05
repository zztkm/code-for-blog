package main

import (
	"encoding/json"
	"os"
)

type Input struct {
	Name string `json:"name"`
	Age int `json:"age"`
}

type Output struct {
	Name string `json:"name"`
	Age int `json:"age"`
	Description string `json:"description"`
}

func main() {
	d := os.Getenv("DATA")
	var input Input
	json.Unmarshal([]byte(d), &input)

	output := Output{
		Name: input.Name,
		Age: input.Age,
		Description: "This is a description",
	}

	b, _ := json.Marshal(output)
	os.Stdout.Write(b)
}
