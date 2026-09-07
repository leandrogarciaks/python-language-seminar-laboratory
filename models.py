from pydantic import BaseModel

class CreateProduct(BaseModel):
    name: str
    price: float

    class Config:
        from_attributes = True

class UpdateProduct(BaseModel):
    name: str | None = None
    price: float | None = None
