# 🚀 SmartTrack Business Analytics

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.105-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)](https://streamlit.io)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://mysql.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

> **Comprehensive business analytics solution for small grocery stores with enterprise scalability**

## 🎯 Problem & Solution

**The Challenge**: Small grocery business owners struggle with fragmented expense tracking, lack of profit visibility, and manual calculations that lead to poor business decisions.

**SmartTrack Solution**:
- ✅ **Real-time Profit Tracking** - Instant visibility into business profitability
- ✅ **Automated Inventory Management** - Smart stock alerts and automatic updates
- ✅ **Comprehensive Analytics** - Visual reports and business insights
- ✅ **Scalable Architecture** - Grows from single store to enterprise chain
- ✅ **Modern Web Interface** - Responsive design for desktop and mobile

## Project Structure
smarttrack-business-analytics/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── routers/
│   └── requirements.txt
├── frontend/
├── database/
├── docker-compose.yml
└── Dockerfile.backend

## Database Setup
The application automatically creates the necessary database tables on first run.


## Technology Stack

Backend: FastAPI with Python 3.11
Database: MySQL 8.0 with SQLAlchemy 2.x
Frontend: Streamlit
Containerization: Docker & Docker Compose
Architecture: Microservices with REST APIs


## 🏗️ System Architecture

Frontend (Streamlit)
        |
        | HTTP Requests
        |
Backend API (FastAPI)
        |
        | SQL Queries
        |
Database (MySQL)


Components
User → Interacts through the Streamlit web interface

Frontend (Streamlit) → Provides dashboards and input forms

Backend (FastAPI) → Handles API requests, authentication, and business logic

Database (MySQL) → Stores users, products, sales, and expenses

Analytics Engine → Processes data and feeds insights back to the frontend

Docker & Docker Compose → Ensure portability, reproducibility, and easy deployment


## 🚀 Quick Installation (5 Minutes)
Prerequisites

Docker Desktop 4.0+
4GB RAM, 10GB storage
Internet connection

##  Installation Steps
Clone the repository:

git clone https://github.com/NinaHenchy/smarttrack-business-analytics.git
cd smarttrack-business-analytics

Start the application:

docker-compose up --build -d

Wait for Setup (60 seconds)

docker-compose logs -f


✅ Verification
## Check all services
docker-compose ps

## Test backend
curl http://localhost:8000/health
## Expected response: {"status":"healthy",...}


##  Access Applications:

🖥️ Dashboard: http://localhost:8501
🔧 API Docs: http://localhost:8000/docs
❤️ Health Check: http://localhost:8000/health


## 📚 API Endpoints
Complete API documentation is available at /docs when the backend is running:
Key Endpoints

GET /health - Service health check
GET /api/v1/products/ - List all products
POST /api/v1/sales/ - Record new sale
GET /api/v1/analytics/dashboard/summary - Dashboard metrics

Example API Usage
python import requests

## Get dashboard summary
response = requests.get("http://localhost:8000/api/v1/analytics/dashboard/summary")
data = response.json()
print(f"Today's profit: ₦{data['metrics']['today']['net_profit']}")


🔧 Management Commands
Basic Operations
bash# Start services
docker-compose up -d

## View logs  
docker-compose logs -f [service_name]

## Stop services
docker-compose down

## Rebuild after code changes
docker-compose up --build -d
Database Management

## Access database directly
docker-compose exec mysql mysql -u smarttrack_user -p smarttrack_db

## Backup database
docker-compose exec mysql mysqldump -u smarttrack_user -p smarttrack_db > backup.sql

## Reset database (WARNING: Deletes all data)
docker-compose down -v && docker-compose up -d

## Monitoring
## Check service health
docker-compose exec backend curl -f http://localhost:8000/health

## Monitor resource usage
docker stats

## View container details
docker-compose ps


📊 Features Overview
💼 Business Management

Sales Recording: Quick transaction entry with automatic inventory updates
Expense Tracking: Categorized expense management with receipt tracking
Product Management: Inventory control with profit margin calculations
Real-time Dashboard: Live business metrics and KPIs

📈 Analytics & Reporting

Profit Analysis: Daily, monthly, and yearly profitability reports
Product Performance: Best-selling and most profitable product insights
Expense Analytics: Category-wise expense breakdown and trends
Visual Charts: Interactive graphs powered by Plotly

🎯 Business Intelligence

Stock Alerts: Low inventory notifications
Performance Metrics: Revenue, profit margins, and growth trends
Decision Support: Data-driven business recommendations
Export Capabilities: Data export for external analysis


📱 Usage Guide
Recording Your First Sale

Navigate to Sales Management → Record Sale
Select products and quantities
Add customer information (optional)
Complete the transaction
View updated inventory and dashboard metrics

Managing Products

Go to Product Management → Add Product
Enter product details and pricing
Set stock levels and minimum thresholds
Monitor profit margins automatically

Tracking Expenses

Access Expense Tracking → Record Expense
Categorize expenses for better reporting
Add vendor and receipt information
View expense analytics and trends

Analyzing Performance

Visit Analytics & Reports
Review product profitability reports
Analyze sales trends and patterns
Make data-driven business decisions

🔒 Security & Production
Environment Configuration
bash# Copy and customize environment file
cp .env.example .env
nano .env
Production Checklist

 Change default database passwords
 Update SECRET_KEY to secure random string
 Configure SSL/HTTPS certificates
 Set up database backups
 Configure firewall rules
 Enable access logging
 Set up monitoring alerts

Sample Production Environment
envDATABASE_URL=mysql+pymysql://prod_user:SecurePass123!@mysql:3306/smarttrack_prod
SECRET_KEY=your-super-secure-random-key-here
LOG_LEVEL=WARNING
DEBUG=False


🧪 Testing
bash# Install test dependencies
pip install pytest pytest-asyncio httpx

## Run all tests
pytest tests/ -v

## Run specific test categories
pytest tests/test_backend.py -v
pytest tests/test_integration.py -v -m integration


🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request


📄 License
This project is licensed under the MIT License.

🎉 Acknowledgments
Built with ❤️ for small business owners worldwide
Powered by modern Python ecosystem
Designed for growth and scalability.

📞 Contact
Nina Henchy - GitHub: @NinaHenchy
Project Link: https://github.com/NinaHenchy/smarttrack-business-analytics


⭐ If SmartTrack helped your business, please star this repository!

