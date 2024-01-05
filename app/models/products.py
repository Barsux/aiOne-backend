from datetime import date
from pydantic import BaseModel, field_validator, ValidationError
from enum import Enum


class ProductCategory(str, Enum):
    electronics = "Электроника"
    clothes = "Одежда"
    furniture = "Мебель"
    sports = "Спорттовары"
    hoz = "Бытовые товары"


class InputProduct(BaseModel):
    name: str
    description: str
    price: int
    category: ProductCategory


class Product(InputProduct):
    id: int
    image_name: str

    class Config:
        from_attributes = True
