
## 📦 backend/app/routers/sales.py
import logging
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[schemas.Sale])
async def get_sales(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None),
        db: Session = Depends(get_db)
):
    try:
        sales = crud.get_sales(db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)
        return sales
    except Exception as e:
        logger.error(f"Error in get_sales: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch sales")


@router.post("/", response_model=schemas.Sale)
async def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    try:
        for item in sale.items:
            product = crud.get_product(db, item.product_id)
            if not product:
                raise HTTPException(status_code=400, detail=f"Product with ID {item.product_id} not found")
            if not product.is_active:
                raise HTTPException(status_code=400, detail=f"Product {product.name} is not active")
            if product.current_stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")

        return crud.create_sale(db=db, sale=sale)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_sale: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create sale")