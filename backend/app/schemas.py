from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, validator
from enum import Enum


class CategoryType(str, Enum):
    expense = "expense"
    product = "product"


class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"
    bank_transfer = "bank_transfer"
    check = "check"
    mobile_money = "mobile_money"


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_type: CategoryType


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    unit_of_measure: str = 'piece'
    cost_price: Decimal
    selling_price: Decimal
    current_stock: int = 0
    minimum_stock_level: int = 10
    is_active: bool = True


class ProductCreate(ProductBase):
    @validator('cost_price', 'selling_price')
    def validate_prices(cls, v):
        if v < 0:
            raise ValueError('Prices must be non-negative')
        return v


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    description: str
    amount: Decimal
    category_id: Optional[int] = None
    expense_date: date
    payment_method: PaymentMethod = PaymentMethod.cash
    vendor_name: Optional[str] = None
    receipt_number: Optional[str] = None
    notes: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v


class Expense(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None

    class Config:
        from_attributes = True


class SaleItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal
    cost_price: Decimal


class SaleItemCreate(SaleItemBase):
    pass


class SaleItem(SaleItemBase):
    id: int
    sale_id: int
    total_price: Decimal
    created_at: datetime
    product: Optional[Product] = None

    class Config:
        from_attributes = True


class SaleBase(BaseModel):
    sale_date: date
    payment_method: PaymentMethod = PaymentMethod.cash
    customer_name: Optional[str] = None
    discount_amount: Decimal = 0.00
    tax_amount: Decimal = 0.00
    notes: Optional[str] = None


class SaleCreate(SaleBase):
    items: List[SaleItemCreate]


class Sale(SaleBase):
    id: int
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
    sale_items: List[SaleItem] = []

    class Config:
        from_attributes = True