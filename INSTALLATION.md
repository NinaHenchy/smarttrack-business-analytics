---

## 📋 INSTALLATION.md
```markdown
# 🛠️ SmartTrack Business Analytics - Installation Guide

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **RAM**: 4GB (8GB recommended)
- **Storage**: 10GB free space
- **Docker**: Docker Desktop 4.0 or later
- **Internet**: Required for initial setup

### Supported Platforms
- ✅ **Windows 10/11** (with WSL2 enabled)
- ✅ **macOS** (Intel & Apple Silicon)
- ✅ **Linux** (Ubuntu, Debian, CentOS, RHEL)

---

## 🐳 Docker Installation Method

### Step 1: Install Docker Desktop

#### Windows
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run installer and restart when prompted
3. Enable WSL2 integration in Docker Desktop settings
4. Verify installation: `docker --version`

#### macOS
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Drag Docker to Applications folder
3. Launch Docker Desktop and complete setup
4. Verify installation: `docker --version`

#### Linux (Ubuntu)
```bash
# Update package index
sudo apt update

# Install dependencies
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again, then verify
docker --version

Step 2: Clone SmartTrack Repository
bash# Clone the repository
git clone https://github.com/your-username/smarttrack-business-analytics.git

# Navigate to project directory
cd smarttrack-business-analytics

# Verify project structure
ls -la
Expected structure:
smarttrack-business-analytics/
├── backend/
├── frontend/
├── database/
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
Step 3: Configure Environment (Optional)
bash# Copy environment template
cp .env.example .env

# Edit configuration if needed
nano .env
Default configuration works out-of-the-box for development.
Step 4: Launch SmartTrack
bash# Build and start all services
docker-compose up --build -d

# This command will:
# ✅ Build backend API container
# ✅ Build frontend dashboard container  
# ✅ Start MySQL database with sample data
# ✅ Configure networking between services
# ✅ Set up persistent data volumes
Step 5: Monitor Startup Process
bash# Watch service logs (wait ~60 seconds for complete startup)
docker-compose logs -f

# Look for these success indicators:
# mysql     | [Server] ready for connections
# backend   | Uvicorn running on http://0.0.0.0:8000  
# frontend  | External URL: http://localhost:8501
Press Ctrl+C to stop viewing logs (services continue running).
Step 6: Access SmartTrack
Open your web browser and navigate to:

🖥️ Main Dashboard: http://localhost:8501
🔧 API Documentation: http://localhost:8000/docs
❤️ Health Check: http://localhost:8000/health


✅ Installation Verification
Check Service Status
bash# Verify all containers are running
docker-compose ps

# Expected output:
# smarttrack-mysql     Up (healthy)
# smarttrack-backend   Up (healthy)
# smarttrack-frontend  Up

Test Backend API
bash# Test health endpoint
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-01-15T...",
  "version": "1.0.0",
  "service": "SmartTrack Backend"
}

# Test products endpoint
curl http://localhost:8000/api/v1/products/
Test Frontend Dashboard

Open browser: Navigate to http://localhost:8501
Check dashboard: Should display "SmartTrack Business Analytics"
Verify data: Should show sample business metrics
Test navigation: Click through different sections in sidebar

Test Database Connection
bash# Connect to MySQL database
docker-compose exec mysql mysql -u smarttrack_user -p
# Password: SmartTrack2024Pass!

# Verify sample data
USE smarttrack_db;
SHOW TABLES;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM sales;
SELECT COUNT(*) FROM expenses;

# Exit MySQL
EXIT;

🔧 Configuration Options
Environment Variables
Edit .env file to customize:
env# Database credentials
DATABASE_URL=mysql+pymysql://smarttrack_user:YourPassword@mysql:3306/smarttrack_db

# Security keys (CHANGE IN PRODUCTION!)
SECRET_KEY=your-super-secure-secret-key-here

# Application settings
LOG_LEVEL=INFO
DEBUG=False

# CORS origins
CORS_ORIGINS=http://localhost:8501,https://yourdomain.com
Port Configuration
To change default ports, edit docker-compose.yml:
yamlservices:
  backend:
    ports:
      - "8080:8000"  # Change 8080 to your preferred port
  
  frontend:
    ports:
      - "8502:8501"  # Change 8502 to your preferred port
  
  mysql:
    ports:
      - "3307:3306"  # Change 3307 to your preferred port
Memory and Resource Limits
Add resource limits to docker-compose.yml:
yamlservices:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

🔄 Management Operations
Start/Stop Services
bash# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart backend

# View service logs
docker-compose logs -f backend
Update SmartTrack
bash# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
Backup Data
bash# Create database backup
docker-compose exec mysql mysqldump -u smarttrack_user -p smarttrack_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup with compression
docker-compose exec mysql mysqldump -u smarttrack_user -p smarttrack_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Reset Everything
bash# WARNING: This deletes ALL data including database
docker-compose down -v
docker system prune -a
docker-compose up --build -d