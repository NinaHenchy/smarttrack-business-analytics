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

## 🏗️ Architecture

```mermaid
graph TB
    A[Streamlit Frontend] --> B[FastAPI Backend]
    B --> C[MySQL Database]
    D[Docker Compose] --> A
    D --> B  
    D --> C

Tech Stack:

Frontend: Streamlit 1.29 (Interactive dashboards)
Backend: FastAPI 0.105 (High-performance API)
Database: MySQL 8.0 (Production-grade storage)
Deployment: Docker Compose (Container orchestration)

🚀 Quick Installation (5 Minutes)
Prerequisites

Docker Desktop 4.0+
4GB RAM, 10GB storage
Internet connection

Installation Steps

Clone Repository

bashgit clone https://github.com/your-username/smarttrack-business-analytics.git
cd smarttrack-business-analytics

Start Services

bashdocker-compose up --build -d

Wait for Setup (60 seconds)

bashdocker-compose logs -f

Access Applications


🖥️ Dashboard: http://localhost:8501
🔧 API Docs: http://localhost:8000/docs
❤️ Health Check: http://localhost:8000/health

✅ Verification
bash# Check all services
docker-compose ps

# Test backend
curl http://localhost:8000/health

# Expected response: {"status":"healthy",...}
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

🔧 Management Commands
Basic Operations
bash# Start services
docker-compose up -d

# View logs  
docker-compose logs -f [service_name]

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build -d
Database Management
bash# Access database directly
docker-compose exec mysql mysql -u smarttrack_user -p smarttrack_db

# Backup database
docker-compose exec mysql mysqldump -u smarttrack_user -p smarttrack_db > backup.sql

# Reset database (WARNING: Deletes all data)
docker-compose down -v && docker-compose up -d
Monitoring
bash# Check service health
docker-compose exec backend curl -f http://localhost:8000/health

# Monitor resource usage
docker stats

# View container details
docker-compose ps

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

📚 API Documentation
Complete API documentation is available at /docs when the backend is running:
Key Endpoints

GET /health - Service health check
GET /api/v1/products/ - List all products
POST /api/v1/sales/ - Record new sale
GET /api/v1/analytics/dashboard/summary - Dashboard metrics

Example API Usage
pythonimport requests

# Get dashboard summary
response = requests.get("http://localhost:8000/api/v1/analytics/dashboard/summary")
data = response.json()
print(f"Today's profit: ₦{data['metrics']['today']['net_profit']}")

🧪 Testing
bash# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_backend.py -v
pytest tests/test_integration.py -v -m integration

🤝 Contributing

Fork the repository
Create feature branch: git checkout -b feature/amazing-feature
Commit changes: git commit -m 'Add amazing feature'
Push to branch: git push origin feature/amazing-feature
Open Pull Request

📞 Support & Community

🐛 Bug Reports: GitHub Issues
💡 Feature Requests: GitHub Discussions
📖 Documentation: Project Wiki

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🎉 Acknowledgments

Built with ❤️ for small business owners worldwide
Powered by modern Python ecosystem
Designed for growth and scalability
Community-driven development


⭐ If SmartTrack helped your business, please star this repository!
Get Started Now | View Live Demo | API Documentation
