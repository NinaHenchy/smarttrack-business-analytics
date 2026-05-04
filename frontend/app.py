# frontend/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta
import logging
from utils.api_client import APIClient
from utils.helpers import format_currency, calculate_profit_margin

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="SmartTrack Business Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    .success-card { border-left-color: #10b981; background: #ecfdf5; }
    .warning-card { border-left-color: #f59e0b; background: #fffbeb; }
    .danger-card { border-left-color: #ef4444; background: #fef2f2; }
    .info-card { border-left-color: #3b82f6; background: #eff6ff; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_api_client():
    try:
        api_url = st.secrets.get("API_BASE_URL", "http://backend:8000")
        return APIClient(api_url)
    except Exception as e:
        logger.warning(f"API client unavailable: {e}")
        return None


def safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default


def ensure_numeric_df(df: pd.DataFrame, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)


def load_demo_dashboard():
    return {
        "metrics": {
            "today": {
                "total_sales": 150000,
                "total_expenses": 90000,
                "net_profit": 60000,
                "profit_margin": 40.0
            },
            "this_month": {
                "total_sales": 4200000,
                "total_expenses": 2800000,
                "net_profit": 1400000,
                "profit_margin": 33.3
            }
        },
        "alerts": {
            "low_stock_products": 3,
            "recent_sales_count": 24
        }
    }


def load_demo_sales():
    return [
        {"sale_date": "2024-05-01", "total_amount": 120000, "payment_method": "cash", "customer_name": "Client A", "discount_amount": 0},
        {"sale_date": "2024-05-02", "total_amount": 85000, "payment_method": "card", "customer_name": "Client B", "discount_amount": 5000},
        {"sale_date": "2024-05-03", "total_amount": 200000, "payment_method": "bank_transfer", "customer_name": "Client C", "discount_amount": 0},
    ]


def load_demo_expenses():
    return [
        {"expense_date": "2024-05-01", "description": "Fuel logistics", "amount": 40000, "vendor_name": "Supplier A"},
        {"expense_date": "2024-05-02", "description": "Equipment maintenance", "amount": 25000, "vendor_name": "Supplier B"},
        {"expense_date": "2024-05-03", "description": "HSE supplies", "amount": 18000, "vendor_name": "Supplier C"},
    ]


def load_demo_products():
    return [
        {"id": 1, "name": "Diesel Fuel", "selling_price": 120000, "cost_price": 90000, "current_stock": 15},
        {"id": 2, "name": "Maintenance Kit", "selling_price": 85000, "cost_price": 60000, "current_stock": 8},
        {"id": 3, "name": "Safety Equipment", "selling_price": 50000, "cost_price": 35000, "current_stock": 20},
    ]


def main():
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


def show_dashboard():
    st.header("📊 Business Dashboard")
    api_client = get_api_client()

    try:
        dashboard_data = api_client.get_dashboard_summary() if api_client else load_demo_dashboard()
    except Exception:
        st.info("Demo mode: Backend API is not connected. Showing sample dashboard data.")
        dashboard_data = load_demo_dashboard()

    metrics = dashboard_data.get("metrics", {}) or {}
    alerts = dashboard_data.get("alerts", {}) or {}

    st.subheader("🎯 Today's Performance")
    today_metrics = metrics.get("today", {}) or {}

    sales_today = safe_float(today_metrics.get("total_sales", 0))
    expenses_today = safe_float(today_metrics.get("total_expenses", 0))
    profit_today = safe_float(today_metrics.get("net_profit", 0))
    margin_today = safe_float(today_metrics.get("profit_margin", 0))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card success-card">
            <h4>💰 Sales</h4>
            <h2>{format_currency(sales_today)}</h2>
            <small>Today's total sales</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card warning-card">
            <h4>💸 Expenses</h4>
            <h2>{format_currency(expenses_today)}</h2>
            <small>Today's total expenses</small>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        profit_class = "success-card" if profit_today >= 0 else "danger-card"
        st.markdown(f"""
        <div class="metric-card {profit_class}">
            <h4>📈 Profit</h4>
            <h2>{format_currency(profit_today)}</h2>
            <small>Today's net profit</small>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        margin_class = "success-card" if margin_today > 10 else "warning-card" if margin_today > 0 else "danger-card"
        st.markdown(f"""
        <div class="metric-card {margin_class}">
            <h4>📊 Margin</h4>
            <h2>{margin_today:.1f}%</h2>
            <small>Today's profit margin</small>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📅 Monthly Overview")
    month_metrics = metrics.get("this_month", {}) or {}

    monthly_sales = safe_float(month_metrics.get("total_sales", 0))
    monthly_expenses = safe_float(month_metrics.get("total_expenses", 0))
    monthly_profit = safe_float(month_metrics.get("net_profit", 0))
    monthly_margin = safe_float(month_metrics.get("profit_margin", 0))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card info-card">
            <h3>💰 Revenue Overview</h3>
            <strong>Total Sales:</strong><br>
            <span style="font-size: 1.5rem; color: #10b981;">{format_currency(monthly_sales)}</span><br><br>
            <strong>Total Expenses:</strong><br>
            <span style="font-size: 1.5rem; color: #f59e0b;">{format_currency(monthly_expenses)}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        profit_class = "success-card" if monthly_profit >= 0 else "danger-card"
        st.markdown(f"""
        <div class="metric-card {profit_class}">
            <h3>📊 Profitability Analysis</h3>
            <strong>Net Profit:</strong><br>
            <span style="font-size: 1.5rem;">{format_currency(monthly_profit)}</span><br><br>
            <strong>Profit Margin:</strong><br>
            <span style="font-size: 1.5rem;">{monthly_margin:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🔔 Business Intelligence")
    col1, col2, col3 = st.columns(3)

    low_stock = int(alerts.get("low_stock_products", 0) or 0)
    recent_sales = int(alerts.get("recent_sales_count", 0) or 0)

    with col1:
        st.markdown(f"""
        <div class="metric-card warning-card">
            <h4>⚠️ Stock Alert</h4>
            <h2>{low_stock}</h2>
            <small>Products need restocking</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card info-card">
            <h4>🛒 Today's Activity</h4>
            <h2>{recent_sales}</h2>
            <small>Transactions recorded</small>
        </div>
        """, unsafe_allow_html=True)

    with col3:
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

    st.subheader("📋 Recent Activity Preview")
    tab1, tab2 = st.tabs(["Recent Sales", "Recent Expenses"])

    with tab1:
        try:
            recent_sales_data = api_client.get_sales(limit=5) if api_client else load_demo_sales()
        except Exception:
            recent_sales_data = load_demo_sales()

        sales_df = pd.DataFrame(recent_sales_data)
        ensure_numeric_df(sales_df, ["total_amount", "discount_amount"])
        sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"]).dt.strftime("%Y-%m-%d")

        st.dataframe(
            sales_df[["sale_date", "total_amount", "payment_method", "customer_name"]].fillna("-"),
            use_container_width=True,
            column_config={
                "sale_date": "Date",
                "total_amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                "payment_method": "Payment",
                "customer_name": "Customer"
            }
        )

    with tab2:
        try:
            recent_expenses_data = api_client.get_expenses(limit=5) if api_client else load_demo_expenses()
        except Exception:
            recent_expenses_data = load_demo_expenses()

        expenses_df = pd.DataFrame(recent_expenses_data)
        ensure_numeric_df(expenses_df, ["amount"])
        expenses_df["expense_date"] = pd.to_datetime(expenses_df["expense_date"]).dt.strftime("%Y-%m-%d")

        st.dataframe(
            expenses_df[["expense_date", "description", "amount", "vendor_name"]].fillna("-"),
            use_container_width=True,
            column_config={
                "expense_date": "Date",
                "description": "Description",
                "amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                "vendor_name": "Vendor"
            }
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

    try:
        products = api_client.get_products() if api_client else load_demo_products()
    except Exception:
        st.info("Demo mode: Backend API unavailable. Showing sample products.")
        products = load_demo_products()

    if not api_client:
        st.warning("Demo mode: Sale submission is disabled on Streamlit Cloud. Run with Docker to submit real sales.")

    if not products:
        st.warning("⚠️ No products available.")
        return

    with st.form("new_sale_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            sale_date = st.date_input("📅 Sale Date", value=date.today())
            payment_method = st.selectbox(
                "💳 Payment Method",
                ["cash", "card", "bank_transfer", "mobile_money"]
            )

        with col2:
            customer_name = st.text_input("👤 Customer Name (Optional)")
            discount = safe_float(st.number_input("💰 Discount Amount (₦)", min_value=0.0, value=0.0, step=0.01))

        st.markdown("---")
        st.subheader("🛒 Sale Items")

        selected_product = st.selectbox(
            "Select Product",
            options=products,
            format_func=lambda p: f"{p.get('name')} - ₦{safe_float(p.get('selling_price', 0)):.2f} | Stock: {p.get('current_stock', 0)}"
        )

        quantity = int(st.number_input("Quantity", min_value=1, value=1))
        unit_price = safe_float(st.number_input(
            "Unit Price",
            min_value=0.01,
            value=safe_float(selected_product.get("selling_price", 0)),
            step=0.01
        ))

        submit_sale = st.form_submit_button("💰 Complete Sale", type="primary")

        if submit_sale:
            if not api_client:
                st.info("Demo mode: Sale preview generated, but not saved.")
                st.success(f"Sale preview: {quantity} x {selected_product.get('name')} = {format_currency(quantity * unit_price)}")
            else:
                try:
                    sale_data = {
                        "sale_date": str(sale_date),
                        "payment_method": payment_method,
                        "customer_name": customer_name or None,
                        "discount_amount": float(discount),
                        "tax_amount": 0.0,
                        "items": [
                            {
                                "product_id": selected_product.get("id"),
                                "quantity": quantity,
                                "unit_price": unit_price,
                                "cost_price": safe_float(selected_product.get("cost_price", 0))
                            }
                        ]
                    }
                    result = api_client.create_sale(sale_data)
                    if result:
                        st.success("🎉 Sale recorded successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to record sale.")
                except Exception as e:
                    st.error(f"❌ Error recording sale: {str(e)}")


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
        try:
            sales = api_client.get_sales(start_date=start_date, end_date=end_date, limit=limit) if api_client else load_demo_sales()
        except Exception:
            st.info("Demo mode: Showing sample sales history.")
            sales = load_demo_sales()

        sales_df = pd.DataFrame(sales)
        ensure_numeric_df(sales_df, ["total_amount", "discount_amount"])
        sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"]).dt.strftime("%Y-%m-%d")

        st.dataframe(sales_df.fillna("-"), use_container_width=True)

        st.markdown("### 📊 Sales Summary")
        total_sales = float(sales_df["total_amount"].sum())
        transaction_count = len(sales_df)
        avg_sale = float(sales_df["total_amount"].mean()) if transaction_count > 0 else 0.0

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Sales", format_currency(total_sales))
        col2.metric("🛒 Transactions", transaction_count)
        col3.metric("📊 Average Sale", format_currency(avg_sale))


def show_sales_analytics():
    st.subheader("📊 Sales Analytics")

    demo_df = pd.DataFrame(load_demo_sales())
    ensure_numeric_df(demo_df, ["total_amount"])
    demo_df["sale_date"] = pd.to_datetime(demo_df["sale_date"])

    fig = px.bar(
        demo_df,
        x="sale_date",
        y="total_amount",
        color="payment_method",
        title="Sales Analytics Preview"
    )
    st.plotly_chart(fig, use_container_width=True)


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

    try:
        categories = api_client.get_categories(category_type="expense") if api_client else []
    except Exception:
        categories = []

    if not api_client:
        st.warning("Demo mode: Expense submission is disabled on Streamlit Cloud. Run with Docker to save real expenses.")

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
                ["cash", "card", "bank_transfer", "check"]
            )

            vendor_name = st.text_input("🏪 Vendor/Supplier Name")

        receipt_number = st.text_input("🧾 Receipt Number")
        notes = st.text_area("📝 Additional Notes")

        submitted = st.form_submit_button("💸 Record Expense", type="primary")

        if submitted:
            if not description or amount <= 0:
                st.warning("⚠️ Please provide a valid description and amount.")
            elif not api_client:
                st.info("Demo mode: Expense preview generated, but not saved.")
                st.success(f"Expense preview: {description} - {format_currency(amount)}")
            else:
                try:
                    expense_data = {
                        "description": description,
                        "amount": float(amount),
                        "category_id": selected_category["id"] if selected_category and selected_category.get("id") else None,
                        "expense_date": str(expense_date),
                        "payment_method": payment_method,
                        "vendor_name": vendor_name or None,
                        "receipt_number": receipt_number or None,
                        "notes": notes or None
                    }

                    result = api_client.create_expense(expense_data)
                    if result:
                        st.success("✅ Expense recorded successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to record expense.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


def show_expense_history():
    st.subheader("📋 Expense History")

    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("📅 Expense From Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("📅 Expense To Date", value=date.today())
    with col3:
        limit = st.number_input("📊 Expense Records to Show", min_value=10, max_value=500, value=50)

    if st.button("📊 Load Expense History", type="primary"):
        api_client = get_api_client()

        try:
            expenses = api_client.get_expenses(start_date=start_date, end_date=end_date, limit=limit) if api_client else load_demo_expenses()
        except Exception:
            st.info("Demo mode: Showing sample expense history.")
            expenses = load_demo_expenses()

        expenses_df = pd.DataFrame(expenses)
        ensure_numeric_df(expenses_df, ["amount"])
        expenses_df["expense_date"] = pd.to_datetime(expenses_df["expense_date"]).dt.strftime("%Y-%m-%d")

        st.dataframe(expenses_df.fillna("-"), use_container_width=True)

        st.markdown("### 📊 Expense Summary")
        total_expenses = float(expenses_df["amount"].sum())
        transaction_count = len(expenses_df)

        col1, col2 = st.columns(2)
        col1.metric("💸 Total Expenses", format_currency(total_expenses))
        col2.metric("📝 Transactions", transaction_count)


def show_product_management():
    st.header("📦 Product Management")
    api_client = get_api_client()

    try:
        products = api_client.get_products() if api_client else load_demo_products()
    except Exception:
        st.info("Demo mode: Showing sample product data.")
        products = load_demo_products()

    st.dataframe(pd.DataFrame(products), use_container_width=True)


def show_analytics_reports():
    st.header("📈 Analytics & Reports")

    demo_df = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Sales": [1200000, 1350000, 1500000, 1420000, 1680000, 1800000],
        "Expenses": [750000, 820000, 900000, 870000, 940000, 990000],
    })

    demo_df["Profit"] = demo_df["Sales"] - demo_df["Expenses"]

    st.subheader("Monthly Sales, Expenses, and Profit")

    fig = px.line(
        demo_df,
        x="Month",
        y=["Sales", "Expenses", "Profit"],
        markers=True,
        title="SmartTrack Monthly Business Performance"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(demo_df, use_container_width=True)


def show_footer():
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 0.9rem; color: gray;'>"
        "🚀 SmartTrack Business Analytics - Full Demo Enabled Version<br>"
        f"&copy; {datetime.now().year} SmartTrack. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()