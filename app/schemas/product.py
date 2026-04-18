from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    stock: int

class ProductOut(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True