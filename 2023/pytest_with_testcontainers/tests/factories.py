from factory.alchemy import SQLAlchemyModelFactory
from factory import Sequence, Faker

from src.udonya.gen.sqlacodegen import models


class MenusFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Menus

    id = Sequence(lambda n: n)
    name = Faker("name")
    price = Faker("price")
    description = Faker("description")
