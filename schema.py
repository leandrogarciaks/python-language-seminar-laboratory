import string
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from datetime import date, time

class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0.0)

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    model_config = ConfigDict(from_attributes=True)

class SaleCreate(BaseModel):
    date_sale: date
    time_sale: time
    id_cart: int
    id_customer: int

class SaleCartAssign(BaseModel):
    id_cart: int

class CartItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class CartResponse(BaseModel):
    id: int
    creation_date: date
    state: Literal["open", "closed"]
    products: list[CartItemResponse]

    model_config = ConfigDict(from_attributes=True)

class SaleResponse(BaseModel):
    id: int
    date_sale: date
    time_sale: time
    total_price: float
    cart: CartResponse
    id_customer: int | None = None

    model_config = ConfigDict(from_attributes=True)

class CartCreate(BaseModel):
    creation_date: date
    state: Literal["open", "closed"]

class CartUpdate(BaseModel):
    creation_date: date
    state: Literal["open", "closed"]

class CartProductAdd(BaseModel):
    id_product: int
    quantity: int = Field(gt=0)

class CustomerResponse(BaseModel):
    id: int
    name: str
    lastname: str
    dni: int

class CustomerCreate(BaseModel):
    name: str
    lastname: str
    dni: int