from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    total_price: int