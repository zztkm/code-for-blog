from pydantic import BaseModel, ConfigDict


class Menus(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    price: int
    description: str


class MenusCreate(BaseModel):
    name: str
    code: str
    price: int
    description: str


class MenusUpdate(BaseModel):
    price: int
    description: str
