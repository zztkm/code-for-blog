from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.udonya.gen.sqlacodegen import models
from src.udonya import app


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
            "price": 300,
            "description": "かけうどんです",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "かけうどん",
        "price": 300,
        "description": "かけうどんです",
    }

    udon = test_db.query(models.Menus).filter(models.Menus.name == "かけうどん").first()
    assert udon is not None
    assert udon.id == 1


def test_get_udon(test_db: Session):
    test_db.add(
        models.Menus(
            name="かけうどん",
            price=300,
            description="かけうどんです",
        )
    )

    response = client.get("/udon/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "かけうどん",
        "price": 300,
        "description": "かけうどんです",
    }