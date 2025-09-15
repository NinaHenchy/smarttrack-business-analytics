from datetime import date, datetime, timedelta
from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)

def format_currency(amount: Union[int, float, str]) -> str:
    """Format amount as Nigerian Naira currency"""
    try:
        if isinstance(amount, str):
            amount = float(amount)
        return f"₦{amount:,.2f}"
    except (ValueError, TypeError):
        logger.warning(f"Invalid currency amount: {amount}")
        return "₦0.00"

def calculate_percentage_change(current: Union[int, float], previous: Union[int, float]) -> float:
    """Calculate percentage change between two values"""
    try:
        if previous == 0:
            return 0.0 if current == 0 else 100.0
        return ((current - previous) / previous) * 100
    except (TypeError, ZeroDivisionError):
        return 0.0

def format_percentage(value: Union[int, float], decimal_places: int = 1) -> str:
    """Format value as percentage"""
    try:
        return f"{value:.{decimal_places}f}%"
    except (TypeError, ValueError):
        return "0.0%"

def calculate_profit_margin(selling_price: Union[int, float], cost_price: Union[int, float]) -> float:
    """Calculate profit margin percentage"""
    try:
        if selling_price == 0:
            return 0.0
        return ((selling_price - cost_price) / selling_price) * 100
    except (TypeError, ZeroDivisionError):
        return 0.0

def safe_divide(numerator: Union[int, float], denominator: Union[int, float]) -> float:
    """Safe division that handles zero denominators"""
    try:
        if denominator == 0:
            return 0.0
        return numerator / denominator
    except (TypeError, ValueError):
        return 0.0

def format_date(date_value: Union[str, date, datetime]) -> str:
    """Format date for display"""
    try:
        if isinstance(date_value, str):
            date_obj = datetime.strptime(date_value.split('T')[0], '%Y-%m-%d').date()
        elif isinstance(date_value, datetime):
            date_obj = date_value.date()
        else:
            date_obj = date_value
        return date_obj.strftime('%B %d, %Y')
    except (ValueError, AttributeError):
        return str(date_value)

def get_date_range_label(start_date: date, end_date: date) -> str:
    """Generate friendly label for date range"""
    try:
        if start_date == end_date:
            return format_date(start_date)
        return f"{format_date(start_date)} - {format_date(end_date)}"
    except AttributeError:
        return f"{start_date} - {end_date}"

def validate_positive_number(value: Union[int, float, str], field_name: str = "Value") -> bool:
    """Validate that a value is a positive number"""
    try:
        num_value = float(value) if isinstance(value, str) else value
        return num_value > 0
    except (ValueError, TypeError):
        return False

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."