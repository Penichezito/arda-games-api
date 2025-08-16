from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.core.db import get_db

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = Query(None),
    store: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """ Listar produtos com filtros opcionais """
    query = db.query(Product)

    if category:
        query = query.filter(Product.category.ilke(f"%{category}%"))
    if store:
        query = query.filter(Product.store.ilke(f"%{store}%"))

    products = query.offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Criar novo produto"""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    """ Busca e Obter detalhes de um produto pelo ID """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produtonão encontrado")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: uuid.UUID,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """ Atualizar um produto pelo ID """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete("{product_id}")
def delete_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    """ Deletar um produto """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(product)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}

@router.get("/categories/list")
def get_categories(db: Session = Depends(get_db)):
    """ Listar todas as categorias disponíveis"""
    categories = db.query(Product.category).distinct().all()
    return [cat[0] for cat in categories]

@router.get("/stores/list")
def get_stores(db: Session = Depends(get_db)):
    """ Listar todas as lojas disponíveis"""
    stores = db.query(Product.store).distinct().all()
    return [store[0] for store in stores]




