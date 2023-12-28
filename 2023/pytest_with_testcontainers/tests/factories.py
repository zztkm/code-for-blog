from factory import Faker, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from src.udonya.gen.sqlacodegen import models


class MenusFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Menus

    id = Sequence(lambda n: n)
    code = Faker("code")
    name = Faker("name")
    price = Faker("price")
    description = Faker("description")
