from pydantic import BaseModel, ConfigDict

class Menus(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: int
    description: str


class MenusCreate(BaseModel):
    name: str
    price: int
    description: str
