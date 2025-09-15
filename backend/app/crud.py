import logging
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from . import models, schemas

logger = logging.getLogger(__name__)


def get_products(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True):
    query = db.query(models.Product)
    if active_only:
        query = query.filter(models.Product.is_active == True)
    return query.offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_categories(db: Session, category_type: Optional[str] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Category)
    if category_type:
        query = query.filter(models.Category.category_type == category_type)
    return query.offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_expenses(db: Session, skip: int = 0, limit: int = 100,
                 start_date: Optional[date] = None, end_date: Optional[date] = None):
    query = db.query(models.Expense)
    if start_date:
        query = query.filter(models.Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(models.Expense.expense_date <= end_date)
    return query.order_by(desc(models.Expense.expense_date)).offset(skip).limit(limit).all()


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_sales(db: Session, skip: int = 0, limit: int = 100,
              start_date: Optional[date] = None, end_date: Optional[date] = None):
    query = db.query(models.Sale)
    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    return query.order_by(desc(models.Sale.sale_date)).offset(skip).limit(limit).all()


def create_sale(db: Session, sale: schemas.SaleCreate):
    total_amount = sum(item.quantity * item.unit_price for item in sale.items) - sale.discount_amount + sale.tax_amount

    sale_data = sale.dict(exclude={'items'})
    sale_data['total_amount'] = total_amount
    db_sale = models.Sale(**sale_data)

    db.add(db_sale)
    db.flush()

    for item in sale.items:
        item_data = item.dict()
        item_data['sale_id'] = db_sale.id
        item_data['total_price'] = item.quantity * item.unit_price

        db_sale_item = models.SaleItem(**item_data)
        db.add(db_sale_item)

        # Update product stock
        db_product = get_product(db, item.product_id)
        if db_product:
            db_product.current_stock -= item.quantity

    db.commit()
    db.refresh(db_sale)
    return db_sale


def get_dashboard_summary(db: Session):
    today = date.today()

    # Today's metrics
    today_sales = db.query(func.coalesce(func.sum(models.Sale.total_amount), 0)).filter(
        models.Sale.sale_date == today
    ).scalar()

    today_expenses = db.query(func.coalesce(func.sum(models.Expense.amount), 0)).filter(
        models.Expense.expense_date == today
    ).scalar()

    # This month metrics
    month_start = today.replace(day=1)
    month_sales = db.query(func.coalesce(func.sum(models.Sale.total_amount), 0)).filter(
        and_(models.Sale.sale_date >= month_start, models.Sale.sale_date <= today)
    ).scalar()

    month_expenses = db.query(func.coalesce(func.sum(models.Expense.amount), 0)).filter(
        and_(models.Expense.expense_date >= month_start, models.Expense.expense_date <= today)
    ).scalar()

    # Low stock products
    low_stock_count = db.query(func.count(models.Product.id)).filter(
        models.Product.current_stock <= models.Product.minimum_stock_level,
        models.Product.is_active == True
    ).scalar()

    # Recent sales count
    recent_sales_count = db.query(func.count(models.Sale.id)).filter(
        models.Sale.sale_date == today
    ).scalar()

    return {
        "metrics": {
            "today": {
                "total_sales": float(today_sales),
                "total_expenses": float(today_expenses),
                "net_profit": float(today_sales - today_expenses),
                "profit_margin": float((today_sales - today_expenses) / today_sales * 100) if today_sales > 0 else 0
            },
            "this_month": {
                "total_sales": float(month_sales),
                "total_expenses": float(month_expenses),
                "net_profit": float(month_sales - month_expenses),
                "profit_margin": float((month_sales - month_expenses) / month_sales * 100) if month_sales > 0 else 0
            }
        },
        "alerts": {
            "low_stock_products": low_stock_count,
            "recent_sales_count": recent_sales_count
        }
    }


def get_product_profit_analysis(db: Session):
    results = db.query(
        models.Product.id,
        models.Product.name,
        models.Category.name.label('category_name'),
        func.coalesce(func.sum(models.SaleItem.quantity), 0).label('total_quantity_sold'),
        func.coalesce(func.sum(models.SaleItem.total_price), 0).label('total_revenue'),
        func.coalesce(func.sum(models.SaleItem.cost_price * models.SaleItem.quantity), 0).label('total_cost')
    ).outerjoin(models.Category).outerjoin(models.SaleItem).group_by(
        models.Product.id, models.Product.name, models.Category.name
    ).all()

    return [
        {
            "id": result.id,
            "name": result.name,
            "category_name": result.category_name or "Uncategorized",
            "total_quantity_sold": result.total_quantity_sold,
            "total_revenue": float(result.total_revenue),
            "total_cost": float(result.total_cost),
            "total_profit": float(result.total_revenue - result.total_cost),
            "profit_margin_percentage": float((
                                                          result.total_revenue - result.total_cost) / result.total_revenue * 100) if result.total_revenue > 0 else 0
        }
        for result in results
    ]