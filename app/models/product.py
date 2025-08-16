from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship, Mapped 
from sqlalchemy.sql import func 
import uuid
from app.core.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    affiliate_url = Column(String, nullable=True)
    category = Column(String, nullable=False, index=True) # Simple for now
    store = Column(String, nullable=False, index=True) # Simple for now
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
