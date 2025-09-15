# backend/app/routers/products.py
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[schemas.Product])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    try:
        products = crud.get_products(db, skip=skip, limit=limit, active_only=active_only)
        return products
    except Exception as e:
        logger.error(f"Error in get_products: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")

@router.get("/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = crud.get_product(db, product_id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch product")

@router.post("/", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_product(db=db, product=product)
    except Exception as e:
        logger.error(f"Error in create_product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.get("/categories/", response_model=List[schemas.Category])
async def get_categories(
    category_type: Optional[str] = Query(None, regex="^(expense|product)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        return crud.get_categories(db, category_type=category_type, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error in get_categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")

@router.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_category(db=db, category=category)
    except Exception as e:
        logger.error(f"Error in create_category: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create category")