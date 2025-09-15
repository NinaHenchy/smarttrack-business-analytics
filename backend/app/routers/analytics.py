import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    try:
        summary = crud.get_dashboard_summary(db)
        summary["generated_at"] = datetime.now().isoformat()
        return summary
    except Exception as e:
        logger.error(f"Error in get_dashboard_summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard summary")

@router.get("/products/profit")
async def get_product_profit_analysis(db: Session = Depends(get_db)):
    try:
        return {"data": crud.get_product_profit_analysis(db)}
    except Exception as e:
        logger.error(f"Error in get_product_profit_analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch product profit analysis")