import logging
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[schemas.Expense])
async def get_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        expenses = crud.get_expenses(db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)
        return expenses
    except Exception as e:
        logger.error(f"Error in get_expenses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch expenses")

@router.post("/", response_model=schemas.Expense)
async def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_expense(db=db, expense=expense)
    except Exception as e:
        logger.error(f"Error in create_expense: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create expense")