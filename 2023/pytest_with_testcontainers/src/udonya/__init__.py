from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .db import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
async def health():
    return {"status": "open"}


@app.get("/")
async def root():
    return {"message": "いらっしゃいませー"}


@app.post("/udon", response_model=schemas.Menus)
async def create_udon(udon: schemas.MenusCreate, db: Session = Depends(get_db)):
    return crud.create_udon(db, udon)


@app.put("/udon/{code}", response_model=schemas.Menus)
async def update_udon(code: str, udon: schemas.MenusUpdate, db: Session = Depends(get_db)):
    db_udon = crud.update_udon(db, code, udon)
    if db_udon is None:
        raise HTTPException(status_code=404, detail="Udon not found")
    return db_udon


@app.get("/udon/{code}", response_model=schemas.Menus)
async def get_udon_by_code(code: str, db: Session = Depends(get_db)):
    udon = crud.get_udon_by_id(db, code)
    if udon is None:
        raise HTTPException(status_code=404, detail="Udon not found")
    return udon


@app.get("/udon", response_model=list[schemas.Menus])
async def get_udons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_udons(db, skip=skip, limit=limit)
