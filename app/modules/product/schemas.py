from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    inventory: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    inventory: Optional[int] = None

class ProductResponse(ProductBase):
    id: str
    created_at: datetime
    inventory_quantity: int

    class Config:
        from_attributes = True
