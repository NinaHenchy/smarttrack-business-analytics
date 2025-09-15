import requests
import logging
from datetime import date
from typing import Optional, List, Dict, Any
import os

logger = logging.getLogger(__name__)


class APIClient:
    """SmartTrack API Client"""

    def __init__(self, base_url: str = None):
        if base_url is None:
            base_url = os.getenv("BACKEND_URL", "http://localhost:8000")

        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.timeout = 30

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[Any, Any]]:
        """Make HTTP request with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout: {method} {endpoint}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error: {method} {endpoint}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {method} {endpoint} - {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {method} {endpoint} - {str(e)}")
            return None

    # Health check
    def health_check(self) -> Optional[Dict[Any, Any]]:
        return self._make_request('GET', '/health')

    # Dashboard
    def get_dashboard_summary(self) -> Optional[Dict[Any, Any]]:
        return self._make_request('GET', '/api/v1/analytics/dashboard/summary')

    # Products
    def get_products(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> Optional[List[Dict]]:
        params = {'skip': skip, 'limit': limit, 'active_only': active_only}
        return self._make_request('GET', '/api/v1/products/', params=params)

    def create_product(self, product_data: Dict[Any, Any]) -> Optional[Dict[Any, Any]]:
        return self._make_request('POST', '/api/v1/products/', json=product_data)

    def get_categories(self, category_type: Optional[str] = None) -> Optional[List[Dict]]:
        params = {}
        if category_type:
            params['category_type'] = category_type
        return self._make_request('GET', '/api/v1/products/categories/', params=params)

    def create_category(self, category_data: Dict[Any, Any]) -> Optional[Dict[Any, Any]]:
        return self._make_request('POST', '/api/v1/products/categories/', json=category_data)

    # Sales
    def get_sales(self, skip: int = 0, limit: int = 100,
                  start_date: Optional[date] = None, end_date: Optional[date] = None) -> Optional[List[Dict]]:
        params = {'skip': skip, 'limit': limit}
        if start_date:
            params['start_date'] = str(start_date)
        if end_date:
            params['end_date'] = str(end_date)
        return self._make_request('GET', '/api/v1/sales/', params=params)

    def create_sale(self, sale_data: Dict[Any, Any]) -> Optional[Dict[Any, Any]]:
        return self._make_request('POST', '/api/v1/sales/', json=sale_data)

    # Expenses
    def get_expenses(self, skip: int = 0, limit: int = 100,
                     start_date: Optional[date] = None, end_date: Optional[date] = None) -> Optional[List[Dict]]:
        params = {'skip': skip, 'limit': limit}
        if start_date:
            params['start_date'] = str(start_date)
        if end_date:
            params['end_date'] = str(end_date)
        return self._make_request('GET', '/api/v1/expenses/', params=params)

    def create_expense(self, expense_data: Dict[Any, Any]) -> Optional[Dict[Any, Any]]:
        return self._make_request('POST', '/api/v1/expenses/', json=expense_data)

    # Analytics
    def get_product_profit_analysis(self) -> Optional[Dict[Any, Any]]:
        return self._make_request('GET', '/api/v1/analytics/products/profit')