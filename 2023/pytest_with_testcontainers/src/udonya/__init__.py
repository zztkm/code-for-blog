from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from . import schemas
from .db import SessionLocal
from .gen.sqlacodegen import models

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
    db_udon = models.Menus(**dict(udon))
    db.add(db_udon)
    db.commit()
    db.refresh(db_udon)
    return db_udon


@app.get("/udon/{id}", response_model=schemas.Menus)
async def get_udon(id: int, db: Session = Depends(get_db)):
    udon = db.query(models.Menus).filter(models.Menus.id == id).first()
    if udon is None:
        raise HTTPException(status_code=404, detail="Udon not found")
    return udon

