from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from datetime import date, time

class ProductCreate(BaseModel):
    name: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    model_config = ConfigDict(from_attributes=True)


class SaleCreate(BaseModel):
    date: date
    time: time
    id_cart: int

class CartItemResponse(BaseModel):
     id: int
     product: ProductResponse
     quantity: int

     model_config = ConfigDict(from_attributes=True)

class CartResponse(BaseModel):
    id: int
    creation_date: date
    state: str
    products: list[CartItemResponse]

    model_config = ConfigDict(from_attributes=True)

class SaleResponse(BaseModel):
    id: int
    date: date
    time: time
    total_price: float
    cart: CartResponse

    model_config = ConfigDict(from_attributes=True)

class CartCreate(BaseModel):
    creation_date: date
    state: Literal["open", "close"]

class CartProductAdd(BaseModel):
    id_product: int
    quantity: int = Field(gt=0)

class SaleCartAssign(BaseModel):
    id_cart: int
