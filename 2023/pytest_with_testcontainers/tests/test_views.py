from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.udonya import app
from src.udonya.gen.sqlacodegen import models

from .factories import MenusFactory

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "いらっしゃいませー"}


def test_create_udon(test_db: Session):
    response = client.post(
        "/udon",
        json={
            "name": "かけうどん",
            "code": "kake_udon",
            "price": 300,
            "description": "かけうどんです",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "code": "kake_udon",
        "name": "かけうどん",
        "price": 300,
        "description": "かけうどんです",
    }

    udon = test_db.query(models.Menus).filter(models.Menus.code == "kake_udon").first()
    assert udon is not None
    assert udon.id == 1


def test_update_udon(test_db: Session):
    menu = MenusFactory(
        name="かけうどん",
        code="kake_udon",
        price=300,
        description="かけうどんです",
    )
    response = client.put(
        f"/udon/{menu.code}",
        json={
            "price": 400,
            "description": "かけうどんです",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "code": "kake_udon",
        "name": "かけうどん",
        "price": 400,
        "description": "かけうどんです",
    }

    udon = test_db.query(models.Menus).filter(models.Menus.name == "かけうどん").first()
    assert udon is not None
    assert udon.price == 400

def test_get_udon(test_db: Session):
    menu = MenusFactory(
        name="かけうどん",
        code="kake_udon",
        price=300,
        description="かけうどんです",
    )

    response = client.get(f"/udon/{menu.code}")
    assert response.status_code == 200
    assert response.json() == {
        "code": "kake_udon",
        "name": "かけうどん",
        "price": 300,
        "description": "かけうどんです",
    }


def test_get_udon_not_found():
    response = client.get("/udon/99999999")
    assert response.status_code == 404