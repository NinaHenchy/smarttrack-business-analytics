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


# Initialize API client
@st.cache_resource
def get_api_client():
    return APIClient("http://backend:8000")


def main():
    """Main application controller"""

    # Header
    st.markdown('<div class="main-header">📊 SmartTrack Business Analytics</div>', unsafe_allow_html=True)

    # Sidebar navigation
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

    # Route to appropriate page
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

    # Footer
    show_footer()


def safe_float(x, default=0.0):
    """Coerce value to float safely."""
    try:
        return float(x)
    except Exception:
        return default


def ensure_numeric_df(df: pd.DataFrame, cols):
    """Convert columns in DataFrame to numeric in place (safe)."""
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)


def show_dashboard():
    """Main business dashboard"""
    st.header("📊 Business Dashboard")

    api_client = get_api_client()

    try:
        # Fetch dashboard data
        dashboard_data = api_client.get_dashboard_summary()

        if dashboard_data:
            metrics = dashboard_data.get('metrics', {}) or {}
            alerts = dashboard_data.get('alerts', {}) or {}

            # Today's Performance Section
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

            # Monthly Overview Section
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

            # Business Alerts Section
            st.subheader("🔔 Business Intelligence")

            col1, col2, col3 = st.columns(3)

            with col1:
                low_stock = int(alerts.get('low_stock_products', 0) or 0)
                if low_stock > 0:
                    st.markdown(f"""
                    <div class="metric-card warning-card">
                        <h4>⚠️ Stock Alert</h4>
                        <h2>{low_stock}</h2>
                        <small>Products need restocking</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="metric-card success-card">
                        <h4>✅ Stock Status</h4>
                        <h2>All Good</h2>
                        <small>Adequate stock levels</small>
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
                # Business health indicator
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

            # Quick Actions Section
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

            # Recent Activity Preview
            st.subheader("📋 Recent Activity Preview")

            tab1, tab2 = st.tabs(["Recent Sales", "Recent Expenses"])

            with tab1:
                try:
                    recent_sales_data = api_client.get_sales(limit=5)
                    if recent_sales_data:
                        sales_df = pd.DataFrame(recent_sales_data)
                        # Ensure numeric columns are numeric
                        ensure_numeric_df(sales_df, ["total_amount", "discount_amount"])
                        sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date']).dt.strftime('%Y-%m-%d')

                        st.dataframe(
                            sales_df[['sale_date', 'total_amount', 'payment_method', 'customer_name']].fillna('-'),
                            use_container_width=True,
                            column_config={
                                "sale_date": "Date",
                                "total_amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                                "payment_method": "Payment",
                                "customer_name": "Customer"
                            }
                        )
                    else:
                        st.info("No recent sales to display")
                except Exception as e:
                    st.error("Error loading recent sales")

            with tab2:
                try:
                    recent_expenses_data = api_client.get_expenses(limit=5)
                    if recent_expenses_data:
                        expenses_df = pd.DataFrame(recent_expenses_data)
                        ensure_numeric_df(expenses_df, ["amount"])
                        expenses_df['expense_date'] = pd.to_datetime(expenses_df['expense_date']).dt.strftime('%Y-%m-%d')

                        st.dataframe(
                            expenses_df[['expense_date', 'description', 'amount', 'vendor_name']].fillna('-'),
                            use_container_width=True,
                            column_config={
                                "expense_date": "Date",
                                "description": "Description",
                                "amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                                "vendor_name": "Vendor"
                            }
                        )
                    else:
                        st.info("No recent expenses to display")
                except Exception as e:
                    st.error("Error loading recent expenses")

        else:
            show_connection_error()

    except Exception as e:
        st.error(f"⚠️ Dashboard error: {str(e)}")
        show_troubleshooting_tips()


def show_sales_management():
    """Sales management interface"""
    st.header("💰 Sales Management")

    tab1, tab2, tab3 = st.tabs(["📝 Record Sale", "📋 Sales History", "📊 Sales Analytics"])

    with tab1:
        show_record_sale_form()

    with tab2:
        show_sales_history()

    with tab3:
        show_sales_analytics()


def show_record_sale_form():
    """Form to record new sales"""
    st.subheader("Record New Sale")

    api_client = get_api_client()

    try:
        products = api_client.get_products() or []
        if not products:
            st.warning("⚠️ No products available. Please add products first.")
            if st.button("➕ Add Products Now"):
                st.session_state.page = "📦 Product Management"
                st.rerun()
            return

        # Ensure numeric fields inside product dicts for safety in format_func
        def prod_label(p):
            sp = safe_float(p.get('selling_price', 0))
            stock = int(p.get('current_stock', 0) or 0)
            return f"📦 {p.get('name','')} - ₦{sp:.2f} (Stock: {stock})"

        with st.form("new_sale_form", clear_on_submit=False):
            # Sale details
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
                # Immediately coerce to float so formatting later is safe
                discount = safe_float(st.number_input("💰 Discount Amount (₦)", min_value=0.0, value=0.0, step=0.01))

            st.markdown("---")
            st.subheader("🛒 Sale Items")

            # Initialize session state for sale items
            if 'sale_items' not in st.session_state:
                st.session_state.sale_items = []

            # Product selection interface
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

            # Add item logic
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

            # Display current sale items
            if st.session_state.sale_items:
                st.markdown("### 🧾 Current Sale Items")

                # Create DataFrame for display
                items_df = pd.DataFrame(st.session_state.sale_items)

                # Ensure numeric columns
                ensure_numeric_df(items_df, ['unit_price', 'total_price', 'quantity'])

                # Add remove functionality
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
                    if st.button("🗑️ Clear All Items"):
                        st.session_state.sale_items = []
                        st.rerun()

                # Sale summary
                subtotal = float(items_df['total_price'].sum())
                final_total = subtotal - safe_float(discount)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Subtotal", format_currency(subtotal))
                with col2:
                    st.metric("Discount", f"-{format_currency(discount)}")
                with col3:
                    st.metric("Final Total", format_currency(final_total))

            # Form submission
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                submit_sale = st.form_submit_button("💰 Complete Sale", type="primary")

                if submit_sale:
                    if st.session_state.sale_items:
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
                    else:
                        st.warning("⚠️ Please add at least one item to complete the sale")

            with col2:
                if st.form_submit_button("🔄 Reset Form"):
                    st.session_state.sale_items = []
                    st.rerun()

    except Exception as e:
        st.error(f"Error loading sales form: {str(e)}")


def show_sales_history():
    """Display sales history with filtering"""
    st.subheader("📋 Sales History")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input("📅 From Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("📅 To Date", value=date.today())
    with col3:
        limit = st.number_input("📊 Records to Show", min_value=10, max_value=500, value=50)

    if st.button("📊 Load Sales History", type="primary"):
        try:
            api_client = get_api_client()
            sales = api_client.get_sales(start_date=start_date, end_date=end_date, limit=limit)

            if sales:
                sales_df = pd.DataFrame(sales)
                # Ensure numeric columns
                ensure_numeric_df(sales_df, ["total_amount", "discount_amount"])
                sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date']).dt.strftime('%Y-%m-%d')

                # Display sales table
                st.dataframe(
                    sales_df[['sale_date', 'total_amount', 'payment_method', 'customer_name', 'discount_amount']].fillna(
                        '-'),
                    use_container_width=True,
                    column_config={
                        "sale_date": "Date",
                        "total_amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                        "payment_method": "Payment Method",
                        "customer_name": "Customer",
                        "discount_amount": st.column_config.NumberColumn("Discount", format="₦%.2f")
                    }
                )

                # Summary metrics
                st.markdown("### 📊 Sales Summary")
                col1, col2, col3, col4 = st.columns(4)

                total_sales = float(sales_df['total_amount'].sum())
                transaction_count = len(sales_df)
                avg_sale = float(sales_df['total_amount'].mean()) if transaction_count > 0 else 0.0
                total_discount = float(sales_df['discount_amount'].sum())

                with col1:
                    st.metric("💰 Total Sales", format_currency(total_sales))
                with col2:
                    st.metric("🛒 Transactions", transaction_count)
                with col3:
                    st.metric("📊 Average Sale", format_currency(avg_sale))
                with col4:
                    st.metric("🏷️ Total Discounts", format_currency(total_discount))

            else:
                st.info("📭 No sales found for the selected period")

        except Exception as e:
            st.error(f"Error loading sales: {str(e)}")


def show_sales_analytics():
    """Display sales analytics and trends"""
    st.subheader("📊 Sales Analytics")

    try:
        api_client = get_api_client()

        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            days = st.slider("📅 Analysis Period (days)", 7, 90, 30)
        with col2:
            chart_type = st.selectbox("📈 Chart Type", ["Line Chart", "Bar Chart", "Area Chart"])

        # Note: This would require additional API endpoints for trends
        st.info("📊 Sales trends analysis will be available once additional API endpoints are implemented.")

        # Placeholder for now
        st.markdown("### 🔮 Coming Soon")
        st.markdown("""
        - 📈 Daily sales trends
        - 📊 Payment method analysis
        - 👥 Customer analytics
        - 🎯 Performance insights
        """)

    except Exception as e:
        st.error(f"Error loading sales analytics: {str(e)}")


def show_expense_tracking():
    """Expense tracking interface"""
    st.header("💸 Expense Tracking")

    tab1, tab2 = st.tabs(["📝 Record Expense", "📋 Expense History"])

    with tab1:
        show_record_expense_form()

    with tab2:
        show_expense_history()


def show_record_expense_form():
    """Form to record new expenses"""
    st.subheader("Record New Expense")

    api_client = get_api_client()

    try:
        categories = api_client.get_categories(category_type="expense") or []

        with st.form("expense_form"):
            # Main expense details
            col1, col2 = st.columns(2)

            with col1:
                description = st.text_input("📝 Expense Description*", max_chars=500)
                amount = safe_float(st.number_input("💰 Amount (₦)*", min_value=0.01, step=0.01, value=1.00))
                expense_date = st.date_input("📅 Date*", value=date.today())

            with col2:
                # Category selection
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

            # Additional details
            col1, col2 = st.columns(2)
            with col1:
                receipt_number = st.text_input("🧾 Receipt Number")
            with col2:
                notes = st.text_area("📝 Additional Notes")

            # Form submission
            submitted = st.form_submit_button("💸 Record Expense", type="primary")
            if submitted:
                if description and amount > 0:
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
                else:
                    st.warning("⚠️ Please provide a valid description and amount")
    except Exception as e:
        st.error(f"Error loading expense form: {str(e)}")


def show_expense_history():
    """Display expense history with filtering"""
    st.subheader("📋 Expense History")

    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("📅 From Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("📅 To Date", value=date.today())
    with col3:
        limit = st.number_input("📊 Records to Show", min_value=10, max_value=500, value=50)

    if st.button("📊 Load Expense History", type="primary"):
        try:
            api_client = get_api_client()
            expenses = api_client.get_expenses(start_date=start_date, end_date=end_date, limit=limit)

            if expenses:
                expenses_df = pd.DataFrame(expenses)
                ensure_numeric_df(expenses_df, ["amount"])
                expenses_df['expense_date'] = pd.to_datetime(expenses_df['expense_date']).dt.strftime('%Y-%m-%d')

                st.dataframe(
                    expenses_df[['expense_date', 'description', 'amount', 'vendor_name']].fillna('-'),
                    use_container_width=True,
                    column_config={
                        "expense_date": "Date",
                        "description": "Description",
                        "amount": st.column_config.NumberColumn("Amount", format="₦%.2f"),
                        "vendor_name": "Vendor"
                    }
                )

                # Summary metrics
                st.markdown("### 📊 Expense Summary")
                col1, col2 = st.columns(2)

                total_expenses = float(expenses_df['amount'].sum())
                transaction_count = len(expenses_df)

                with col1:
                    st.metric("💸 Total Expenses", format_currency(total_expenses))
                with col2:
                    st.metric("📝 Transactions", transaction_count)
            else:
                st.info("📭 No expenses found for the selected period")
        except Exception as e:
            st.error(f"Error loading expenses: {str(e)}")


def show_product_management():
    """Product management interface"""
    st.header("📦 Product Management")
    st.info("⚙️ Product management features (add, edit, restock) will be implemented here.")
    # You can extend with product forms + API calls similar to sales & expenses


def show_analytics_reports():
    """Analytics & Reports interface"""
    st.header("📈 Analytics & Reports")
    st.info("📊 Advanced reports and analytics will be added here (profitability, category analysis, trends).")


def show_footer():
    """Footer section"""
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 0.9rem; color: gray;'>"
        "🚀 SmartTrack Business Analytics - Complete Production Version<br>"
        f"&copy; {datetime.now().year} SmartTrack. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )


def show_connection_error():
    """Helper to display API connection error"""
    st.error("❌ Could not connect to backend API. Please ensure the backend service is running.")


def show_troubleshooting_tips():
    """Helper to guide user when things go wrong"""
    st.warning("""
    ### 🛠️ Troubleshooting Tips
    - Ensure backend container is running and healthy (`docker-compose ps`)
    - Check your network connection
    - Look at backend logs for API errors (`docker-compose logs backend`)
    """)


if __name__ == "__main__":
    main()
