# frontend/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
import logging
from utils.api_client import APIClient
from utils.helpers import format_currency, calculate_profit_margin

logger = logging.getLogger(__name__)

# Configure page
st.set_page_config(
    page_title="SmartTrack Business Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        transition: transform 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }

    .success-card {
        border-left-color: #10b981;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    }
    .warning-card {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    }
    .danger-card {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
    }
    .info-card {
        border-left-color: #3b82f6;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    }

    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border-radius: 10px;
        padding: 1rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
    }

    .quick-action-btn {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .quick-action-btn:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_api_client():
    """
    Environment-aware API client.

    Docker:
      docker-compose sets BACKEND_URL=http://backend:8000, so the frontend uses
      the real FastAPI backend and MySQL sample data.

    Streamlit Cloud / no Docker:
      BACKEND_URL is not available, health check fails safely, and the app uses
      demo portfolio data instead of crashing.
    """
    try:
        client = APIClient()
        if client.health_check():
            return client
        return None
    except Exception as e:
        logger.warning(f"Backend unavailable, switching to demo mode: {e}")
        return None


def main():
    """Main application controller"""
    st.markdown('<div class="main-header">📊 SmartTrack Business Analytics</div>', unsafe_allow_html=True)

    st.sidebar.markdown("### 🧭 Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        [
            "📊 Dashboard",
            "💰 Sales Management",
            "💸 Expense Tracking",
            "📦 Product Management",
            "📈 Analytics & Reports"
        ],
        index=0
    )

    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "💰 Sales Management":
        show_sales_management()
    elif page == "💸 Expense Tracking":
        show_expense_tracking()
    elif page == "📦 Product Management":
        show_product_management()
    elif page == "📈 Analytics & Reports":
        show_analytics_reports()

    show_footer()


def safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default


def ensure_numeric_df(df: pd.DataFrame, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)


def backend_unavailable_message():
    st.warning(
        "Portfolio demo mode: backend API is not connected. "
        "Run the project with Docker to use the full FastAPI and MySQL system."
    )


def demo_dashboard_data():
    return {
        "metrics": {
            "today": {
                "total_sales": 185000,
                "total_expenses": 97000,
                "net_profit": 88000,
                "profit_margin": 47.6,
            },
            "this_month": {
                "total_sales": 4250000,
                "total_expenses": 2860000,
                "net_profit": 1390000,
                "profit_margin": 32.7,
            },
        },
        "alerts": {
            "low_stock_products": 4,
            "recent_sales_count": 28,
        },
    }


def demo_sales():
    return [
        {"sale_date": "2026-05-01", "total_amount": 120000, "payment_method": "Cash", "customer_name": "Client A", "discount_amount": 0},
        {"sale_date": "2026-05-02", "total_amount": 85000, "payment_method": "Card", "customer_name": "Client B", "discount_amount": 5000},
        {"sale_date": "2026-05-03", "total_amount": 200000, "payment_method": "Bank Transfer", "customer_name": "Client C", "discount_amount": 0},
    ]


def demo_expenses():
    return [
        {"expense_date": "2026-05-01", "description": "Fuel logistics", "amount": 40000, "vendor_name": "Supplier A"},
        {"expense_date": "2026-05-02", "description": "Equipment maintenance", "amount": 25000, "vendor_name": "Supplier B"},
        {"expense_date": "2026-05-03", "description": "HSE supplies", "amount": 18000, "vendor_name": "Supplier C"},
    ]


def demo_products():
    return [
        {"id": 1, "name": "Diesel Fuel", "selling_price": 120000, "cost_price": 90000, "current_stock": 15},
        {"id": 2, "name": "Maintenance Kit", "selling_price": 85000, "cost_price": 60000, "current_stock": 8},
        {"id": 3, "name": "Safety Equipment", "selling_price": 50000, "cost_price": 35000, "current_stock": 20},
    ]


def demo_categories():
    return [
        {"id": 1, "name": "Operations"},
        {"id": 2, "name": "Maintenance"},
        {"id": 3, "name": "HSE"},
        {"id": 4, "name": "Logistics"},
    ]


def get_sales_data(api_client, **kwargs):
    if api_client:
        try:
            data = api_client.get_sales(**kwargs)
            if data:
                return data
        except Exception as e:
            logger.warning(f"Sales API fallback: {e}")
    return demo_sales()


def get_expenses_data(api_client, **kwargs):
    if api_client:
        try:
            data = api_client.get_expenses(**kwargs)
            if data:
                return data
        except Exception as e:
            logger.warning(f"Expenses API fallback: {e}")
    return demo_expenses()


def get_products_data(api_client):
    if api_client:
        try:
            data = api_client.get_products()
            if data:
                return data
        except Exception as e:
            logger.warning(f"Products API fallback: {e}")
    return demo_products()


def get_categories_data(api_client):
    if api_client:
        try:
            data = api_client.get_categories(category_type="expense")
            if isinstance(data, list):
                return data
        except Exception as e:
            logger.warning(f"Categories API fallback: {e}")
    return demo_categories()


def render_dashboard_from_data(dashboard_data, demo_mode=False):
    if demo_mode:
        st.info("Portfolio demo mode: showing sample SmartTrack business analytics data.")

    metrics = dashboard_data.get('metrics', {}) or {}
    alerts = dashboard_data.get('alerts', {}) or {}

    st.subheader("🎯 Today's Performance")

    col1, col2, col3, col4 = st.columns(4)
    today_metrics = metrics.get('today', {}) or {}

    with col1:
        sales_today = safe_float(today_metrics.get('total_sales', 0))
        st.markdown(f"""
        <div class="metric-card success-card">
            <h4>💰 Sales</h4>
            <h2>{format_currency(sales_today)}</h2>
            <small>Today's total sales</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        expenses_today = safe_float(today_metrics.get('total_expenses', 0))
        st.markdown(f"""
        <div class="metric-card warning-card">
            <h4>💸 Expenses</h4>
            <h2>{format_currency(expenses_today)}</h2>
            <small>Today's total expenses</small>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        profit_today = safe_float(today_metrics.get('net_profit', 0))
        profit_class = "success-card" if profit_today >= 0 else "danger-card"
        profit_icon = "📈" if profit_today >= 0 else "📉"
        st.markdown(f"""
        <div class="metric-card {profit_class}">
            <h4>{profit_icon} Profit</h4>
            <h2>{format_currency(profit_today)}</h2>
            <small>Today's net profit</small>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        margin_today = safe_float(today_metrics.get('profit_margin', 0))
        margin_class = "success-card" if margin_today > 10 else "warning-card" if margin_today > 0 else "danger-card"
        st.markdown(f"""
        <div class="metric-card {margin_class}">
            <h4>📊 Margin</h4>
            <h2>{margin_today:.1f}%</h2>
            <small>Today's profit margin</small>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📅 Monthly Overview")

    month_metrics = metrics.get('this_month', {}) or {}
    col1, col2 = st.columns(2)

    with col1:
        monthly_sales = safe_float(month_metrics.get('total_sales', 0))
        monthly_expenses = safe_float(month_metrics.get('total_expenses', 0))
        st.markdown(f"""
        <div class="metric-card info-card">
            <h3>💰 Revenue Overview</h3>
            <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                <div>
                    <strong>Total Sales:</strong><br>
                    <span style="font-size: 1.5rem; color: #10b981;">{format_currency(monthly_sales)}</span>
                </div>
                <div>
                    <strong>Total Expenses:</strong><br>
                    <span style="font-size: 1.5rem; color: #f59e0b;">{format_currency(monthly_expenses)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        monthly_profit = safe_float(month_metrics.get('net_profit', 0))
        monthly_margin = safe_float(month_metrics.get('profit_margin', 0))
        profit_trend_class = "success-card" if monthly_profit >= 0 else "danger-card"

        st.markdown(f"""
        <div class="metric-card {profit_trend_class}">
            <h3>📊 Profitability Analysis</h3>
            <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                <div>
                    <strong>Net Profit:</strong><br>
                    <span style="font-size: 1.5rem; color: {'#10b981' if monthly_profit >= 0 else '#ef4444'};">{format_currency(monthly_profit)}</span>
                </div>
                <div>
                    <strong>Profit Margin:</strong><br>
                    <span style="font-size: 1.5rem; color: {'#10b981' if monthly_margin >= 10 else '#f59e0b' if monthly_margin >= 0 else '#ef4444'};">{monthly_margin:.1f}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🔔 Business Intelligence")

    col1, col2, col3 = st.columns(3)

    with col1:
        low_stock = int(alerts.get('low_stock_products', 0) or 0)
        card = "warning-card" if low_stock > 0 else "success-card"
        title = "⚠️ Stock Alert" if low_stock > 0 else "✅ Stock Status"
        value = low_stock if low_stock > 0 else "All Good"
        desc = "Products need restocking" if low_stock > 0 else "Adequate stock levels"
        st.markdown(f"""
        <div class="metric-card {card}">
            <h4>{title}</h4>
            <h2>{value}</h2>
            <small>{desc}</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        recent_sales = int(alerts.get('recent_sales_count', 0) or 0)
        st.markdown(f"""
        <div class="metric-card info-card">
            <h4>🛒 Today's Activity</h4>
            <h2>{recent_sales}</h2>
            <small>Transactions recorded</small>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        monthly_profit = safe_float(month_metrics.get('net_profit', 0))
        monthly_margin = safe_float(month_metrics.get('profit_margin', 0))

        if monthly_profit < 0:
            health_status = "🚨 Needs Attention"
            health_desc = "Monthly loss detected"
            health_class = "danger-card"
        elif monthly_margin < 10:
            health_status = "⚡ Room for Growth"
            health_desc = "Low profit margins"
            health_class = "warning-card"
        else:
            health_status = "🎯 Performing Well"
            health_desc = "Healthy business metrics"
            health_class = "success-card"

        st.markdown(f"""
        <div class="metric-card {health_class}">
            <h4>📊 Business Health</h4>
            <h3>{health_status}</h3>
            <small>{health_desc}</small>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📈 Monthly Trend")

    trend_df = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Sales": [1200000, 1350000, 1500000, 1420000, 1680000, 1850000],
        "Expenses": [750000, 820000, 900000, 870000, 940000, 970000],
    })
    trend_df["Profit"] = trend_df["Sales"] - trend_df["Expenses"]

    fig = px.line(
        trend_df,
        x="Month",
        y=["Sales", "Expenses", "Profit"],
        markers=True,
        title="SmartTrack Monthly Business Performance"
    )
    st.plotly_chart(fig, use_container_width=True)


def show_dashboard():
    st.header("📊 Business Dashboard")

    api_client = get_api_client()
    demo_mode = api_client is None

    if api_client:
        try:
            dashboard_data = api_client.get_dashboard_summary()
            if not dashboard_data:
                dashboard_data = demo_dashboard_data()
                demo_mode = True
        except Exception as e:
            logger.warning(f"Dashboard API fallback: {e}")
            dashboard_data = demo_dashboard_data()
            demo_mode = True
    else:
        dashboard_data = demo_dashboard_data()

    render_dashboard_from_data(dashboard_data, demo_mode=demo_mode)

    st.subheader("⚡ Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🛒 Record Sale", use_container_width=True):
            st.session_state.page = "💰 Sales Management"
            st.rerun()

    with col2:
        if st.button("💸 Add Expense", use_container_width=True):
            st.session_state.page = "💸 Expense Tracking"
            st.rerun()

    with col3:
        if st.button("📦 Add Product", use_container_width=True):
            st.session_state.page = "📦 Product Management"
            st.rerun()

    with col4:
        if st.button("📈 View Reports", use_container_width=True):
            st.session_state.page = "📈 Analytics & Reports"
            st.rerun()

    st.subheader("📋 Recent Activity Preview")

    tab1, tab2 = st.tabs(["Recent Sales", "Recent Expenses"])

    with tab1:
        recent_sales_data = get_sales_data(api_client, limit=5)
        sales_df = pd.DataFrame(recent_sales_data)
        ensure_numeric_df(sales_df, ["total_amount", "discount_amount"])

        if "sale_date" in sales_df.columns:
            sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"]).dt.strftime("%Y-%m-%d")

        required_cols = ["sale_date", "total_amount", "payment_method", "customer_name"]
        available_cols = [c for c in required_cols if c in sales_df.columns]

        st.dataframe(
            sales_df[available_cols].fillna("-"),
            use_container_width=True,
            column_config={
                "sale_date": "Date",
                "total_amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                "payment_method": "Payment",
                "customer_name": "Customer",
            },
        )

    with tab2:
        recent_expenses_data = get_expenses_data(api_client, limit=5)
        expenses_df = pd.DataFrame(recent_expenses_data)
        ensure_numeric_df(expenses_df, ["amount"])

        if "expense_date" in expenses_df.columns:
            expenses_df["expense_date"] = pd.to_datetime(expenses_df["expense_date"]).dt.strftime("%Y-%m-%d")

        required_cols = ["expense_date", "description", "amount", "vendor_name"]
        available_cols = [c for c in required_cols if c in expenses_df.columns]

        st.dataframe(
            expenses_df[available_cols].fillna("-"),
            use_container_width=True,
            column_config={
                "expense_date": "Date",
                "description": "Description",
                "amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                "vendor_name": "Vendor",
            },
        )


def show_sales_management():
    st.header("💰 Sales Management")

    tab1, tab2, tab3 = st.tabs(["📝 Record Sale", "📋 Sales History", "📊 Sales Analytics"])

    with tab1:
        show_record_sale_form()

    with tab2:
        show_sales_history()

    with tab3:
        show_sales_analytics()


def show_record_sale_form():
    st.subheader("Record New Sale")

    api_client = get_api_client()
    products = get_products_data(api_client)

    if api_client is None:
        st.info("Portfolio demo mode: form previews are enabled, but records are not saved.")

    if not products:
        st.warning("⚠️ No products available.")
        return

    def prod_label(p):
        sp = safe_float(p.get('selling_price', 0))
        stock = int(p.get('current_stock', 0) or 0)
        return f"📦 {p.get('name','')} - ₦{sp:.2f} (Stock: {stock})"

    with st.form("new_sale_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            sale_date = st.date_input("📅 Sale Date", value=date.today())
            payment_method = st.selectbox(
                "💳 Payment Method",
                ["cash", "card", "bank_transfer", "mobile_money"],
                format_func=lambda x: {
                    "cash": "💵 Cash",
                    "card": "💳 Card",
                    "bank_transfer": "🏦 Bank Transfer",
                    "mobile_money": "📱 Mobile Money"
                }[x]
            )

        with col2:
            customer_name = st.text_input("👤 Customer Name (Optional)")
            discount = safe_float(st.number_input("💰 Discount Amount (₦)", min_value=0.0, value=0.0, step=0.01))

        st.markdown("---")
        st.subheader("🛒 Sale Items")

        if 'sale_items' not in st.session_state:
            st.session_state.sale_items = []

        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            selected_product = st.selectbox(
                "Select Product",
                options=products,
                format_func=prod_label,
                key="product_selector"
            )

        with col2:
            quantity = int(st.number_input("Qty", min_value=1, value=1, key="qty_input"))

        with col3:
            unit_price = 0.0
            if selected_product:
                unit_price = safe_float(st.number_input(
                    "Unit Price",
                    min_value=0.01,
                    value=safe_float(selected_product.get('selling_price', 0)),
                    step=0.01,
                    key="price_input"
                ))

        with col4:
            add_item_btn = st.form_submit_button("➕ Add")

        if add_item_btn and selected_product:
            current_stock = int(selected_product.get('current_stock', 0) or 0)
            if quantity <= current_stock:
                item = {
                    'product_id': selected_product.get('id'),
                    'product_name': selected_product.get('name'),
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'cost_price': safe_float(selected_product.get('cost_price', 0)),
                    'total_price': float(quantity) * float(unit_price)
                }
                st.session_state.sale_items.append(item)
                st.success(f"✅ Added {quantity} x {selected_product.get('name')}")
                st.rerun()
            else:
                st.error(f"❌ Insufficient stock! Available: {current_stock}")

        if st.session_state.sale_items:
            st.markdown("### 🧾 Current Sale Items")

            items_df = pd.DataFrame(st.session_state.sale_items)
            ensure_numeric_df(items_df, ['unit_price', 'total_price', 'quantity'])

            col1, col2 = st.columns([4, 1])
            with col1:
                st.dataframe(
                    items_df[['product_name', 'quantity', 'unit_price', 'total_price']],
                    use_container_width=True,
                    column_config={
                        "product_name": "Product",
                        "quantity": "Qty",
                        "unit_price": st.column_config.NumberColumn("Unit Price", format="₦%.2f"),
                        "total_price": st.column_config.NumberColumn("Total", format="₦%.2f")
                    }
                )

            with col2:
                if st.form_submit_button("🗑️ Clear All Items"):
                    st.session_state.sale_items = []
                    st.rerun()

            subtotal = float(items_df['total_price'].sum())
            final_total = subtotal - safe_float(discount)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Subtotal", format_currency(subtotal))
            with col2:
                st.metric("Discount", f"-{format_currency(discount)}")
            with col3:
                st.metric("Final Total", format_currency(final_total))

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            submit_sale = st.form_submit_button("💰 Complete Sale", type="primary")

        with col2:
            reset_form = st.form_submit_button("🔄 Reset Form")

        if submit_sale:
            if not st.session_state.sale_items:
                st.warning("⚠️ Please add at least one item to complete the sale")
            elif api_client is None:
                st.success("Demo sale preview generated. No record was saved because backend is not connected.")
            else:
                try:
                    sale_data = {
                        'sale_date': str(sale_date),
                        'payment_method': payment_method,
                        'customer_name': customer_name or None,
                        'discount_amount': float(discount),
                        'tax_amount': 0.0,
                        'items': [
                            {
                                'product_id': item['product_id'],
                                'quantity': int(item['quantity']),
                                'unit_price': float(item['unit_price']),
                                'cost_price': float(item['cost_price'])
                            }
                            for item in st.session_state.sale_items
                        ]
                    }

                    result = api_client.create_sale(sale_data)
                    if result:
                        st.success("🎉 Sale recorded successfully!")
                        st.balloons()
                        st.session_state.sale_items = []
                        st.rerun()
                    else:
                        st.error("❌ Failed to record sale. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error recording sale: {str(e)}")

        if reset_form:
            st.session_state.sale_items = []
            st.rerun()


def show_sales_history():
    st.subheader("📋 Sales History")

    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input("📅 From Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("📅 To Date", value=date.today())
    with col3:
        limit = st.number_input("📊 Records to Show", min_value=10, max_value=500, value=50)

    if st.button("📊 Load Sales History", type="primary"):
        api_client = get_api_client()
        sales = get_sales_data(api_client, start_date=start_date, end_date=end_date, limit=limit)

        sales_df = pd.DataFrame(sales)
        ensure_numeric_df(sales_df, ["total_amount", "discount_amount"])

        if "sale_date" in sales_df.columns:
            sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date']).dt.strftime('%Y-%m-%d')

        required_cols = ['sale_date', 'total_amount', 'payment_method', 'customer_name', 'discount_amount']
        available_cols = [c for c in required_cols if c in sales_df.columns]

        st.dataframe(
            sales_df[available_cols].fillna('-'),
            use_container_width=True,
            column_config={
                "sale_date": "Date",
                "total_amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                "payment_method": "Payment Method",
                "customer_name": "Customer",
                "discount_amount": st.column_config.NumberColumn("Discount", format="₦%.2f")
            }
        )

        st.markdown("### 📊 Sales Summary")
        col1, col2, col3, col4 = st.columns(4)

        total_sales = float(sales_df['total_amount'].sum()) if "total_amount" in sales_df.columns else 0.0
        transaction_count = len(sales_df)
        avg_sale = float(sales_df['total_amount'].mean()) if transaction_count > 0 and "total_amount" in sales_df.columns else 0.0
        total_discount = float(sales_df['discount_amount'].sum()) if "discount_amount" in sales_df.columns else 0.0

        with col1:
            st.metric("💰 Total Sales", format_currency(total_sales))
        with col2:
            st.metric("🛒 Transactions", transaction_count)
        with col3:
            st.metric("📊 Average Sale", format_currency(avg_sale))
        with col4:
            st.metric("🏷️ Total Discounts", format_currency(total_discount))


def show_sales_analytics():
    st.subheader("📊 Sales Analytics")

    api_client = get_api_client()
    sales = get_sales_data(api_client, limit=100)
    sales_df = pd.DataFrame(sales)
    ensure_numeric_df(sales_df, ["total_amount"])

    if "sale_date" in sales_df.columns:
        sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"])

        fig = px.bar(
            sales_df,
            x="sale_date",
            y="total_amount",
            color="payment_method" if "payment_method" in sales_df.columns else None,
            title="Sales Analytics Preview"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sales analytics will be available once sales data includes sale dates.")


def show_expense_tracking():
    st.header("💸 Expense Tracking")

    tab1, tab2 = st.tabs(["📝 Record Expense", "📋 Expense History"])

    with tab1:
        show_record_expense_form()

    with tab2:
        show_expense_history()


def show_record_expense_form():
    st.subheader("Record New Expense")

    api_client = get_api_client()
    categories = get_categories_data(api_client)

    if api_client is None:
        st.info("Portfolio demo mode: form previews are enabled, but records are not saved.")

    with st.form("expense_form"):
        col1, col2 = st.columns(2)

        with col1:
            description = st.text_input("📝 Expense Description*", max_chars=500)
            amount = safe_float(st.number_input("💰 Amount (₦)*", min_value=0.01, step=0.01, value=1.00))
            expense_date = st.date_input("📅 Date*", value=date.today())

        with col2:
            category_options = [{"id": None, "name": "No Category"}] + categories
            selected_category = st.selectbox(
                "📂 Category",
                options=category_options,
                format_func=lambda x: x["name"]
            )

            payment_method = st.selectbox(
                "💳 Payment Method",
                ["cash", "card", "bank_transfer", "check"],
                format_func=lambda x: {
                    "cash": "💵 Cash",
                    "card": "💳 Card",
                    "bank_transfer": "🏦 Bank Transfer",
                    "check": "📝 Check"
                }[x]
            )

            vendor_name = st.text_input("🏪 Vendor/Supplier Name")

        col1, col2 = st.columns(2)
        with col1:
            receipt_number = st.text_input("🧾 Receipt Number")
        with col2:
            notes = st.text_area("📝 Additional Notes")

        submitted = st.form_submit_button("💸 Record Expense", type="primary")
        if submitted:
            if not description or amount <= 0:
                st.warning("⚠️ Please provide a valid description and amount")
            elif api_client is None:
                st.success(f"Demo expense preview: {description} - {format_currency(amount)}. No record was saved.")
            else:
                try:
                    expense_data = {
                        'description': description,
                        'amount': float(amount),
                        'category_id': selected_category['id'] if selected_category and selected_category.get('id') else None,
                        'expense_date': str(expense_date),
                        'payment_method': payment_method,
                        'vendor_name': vendor_name or None,
                        'receipt_number': receipt_number or None,
                        'notes': notes or None
                    }

                    result = api_client.create_expense(expense_data)
                    if result:
                        st.success("✅ Expense recorded successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to record expense")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


def show_expense_history():
    st.subheader("📋 Expense History")

    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("📅 From Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("📅 To Date", value=date.today())
    with col3:
        limit = st.number_input("📊 Records to Show", min_value=10, max_value=500, value=50)

    if st.button("📊 Load Expense History", type="primary"):
        api_client = get_api_client()
        expenses = get_expenses_data(api_client, start_date=start_date, end_date=end_date, limit=limit)

        expenses_df = pd.DataFrame(expenses)
        ensure_numeric_df(expenses_df, ["amount"])

        if "expense_date" in expenses_df.columns:
            expenses_df['expense_date'] = pd.to_datetime(expenses_df['expense_date']).dt.strftime('%Y-%m-%d')

        required_cols = ['expense_date', 'description', 'amount', 'vendor_name']
        available_cols = [c for c in required_cols if c in expenses_df.columns]

        st.dataframe(
            expenses_df[available_cols].fillna('-'),
            use_container_width=True,
            column_config={
                "expense_date": "Date",
                "description": "Description",
                "amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                "vendor_name": "Vendor"
            }
        )

        st.markdown("### 📊 Expense Summary")
        col1, col2 = st.columns(2)

        total_expenses = float(expenses_df['amount'].sum()) if "amount" in expenses_df.columns else 0.0
        transaction_count = len(expenses_df)

        with col1:
            st.metric("💸 Total Expenses", format_currency(total_expenses))
        with col2:
            st.metric("📝 Transactions", transaction_count)


def show_product_management():
    st.header("📦 Product Management")

    api_client = get_api_client()
    products = get_products_data(api_client)

    if api_client is None:
        st.info("Portfolio demo mode: showing sample product data.")

    st.dataframe(pd.DataFrame(products), use_container_width=True)


def show_analytics_reports():
    st.header("📈 Analytics & Reports")

    trend_df = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Sales": [1200000, 1350000, 1500000, 1420000, 1680000, 1850000],
        "Expenses": [750000, 820000, 900000, 870000, 940000, 970000],
    })

    trend_df["Profit"] = trend_df["Sales"] - trend_df["Expenses"]

    fig = px.line(
        trend_df,
        x="Month",
        y=["Sales", "Expenses", "Profit"],
        markers=True,
        title="SmartTrack Monthly Business Performance"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(trend_df, use_container_width=True)


def show_footer():
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 0.9rem; color: gray;'>"
        "🚀 SmartTrack Business Analytics - Full Docker + Portfolio Demo Version<br>"
        f"&copy; {datetime.now().year} SmartTrack. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )


def show_connection_error():
    st.error("❌ Could not connect to backend API. Please ensure the backend service is running.")


def show_troubleshooting_tips():
    st.warning("""
    ### 🛠️ Troubleshooting Tips
    - Ensure backend container is running and healthy (`docker-compose ps`)
    - Check your network connection
    - Look at backend logs for API errors (`docker-compose logs backend`)
    """)


if __name__ == "__main__":
    main()
