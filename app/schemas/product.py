from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional
import uuid

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    image_url: HttpUrl
    affiliate_url: HttpUrl
    category: str = Field(..., min_length=1, max_length=100)
    store: str = Field(..., min_length=1, max_length=100)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[HttpUrl] = None
    affiliate_url: Optional[HttpUrl] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    store: Optional[str] = Field(None, min_length=1, max_length=100)

class ProductResponse(ProductBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class config:
        from_attributes = True



