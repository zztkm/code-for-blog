from sqlalchemy.orm import Session

from . import schemas
from .gen.sqlacodegen import models


def get_udon_by_id(db: Session, udon_code: str) -> models.Menus | None:
    return db.query(models.Menus).filter(models.Menus.code == udon_code).first()


def get_udons(db: Session, skip: int = 0, limit: int = 100) -> list[models.Menus]:
    return db.query(models.Menus).offset(skip).limit(limit).all()


def create_udon(db: Session, udon: schemas.MenusCreate) -> models.Menus:
    db_udon = models.Menus(**dict(udon))
    db.add(db_udon)
    db.commit()
    db.refresh(db_udon)
    return db_udon


def update_udon(db: Session, udon_code: str, udon: schemas.MenusUpdate) -> models.Menus | None:
    db_udon = db.query(models.Menus).filter(models.Menus.code == udon_code).first()
    if db_udon is None:
        return None
    db_udon.price = udon.price
    db_udon.description = udon.description
    db.commit()
    db.refresh(db_udon)
    return db_udon
