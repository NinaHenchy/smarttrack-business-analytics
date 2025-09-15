## 🚨 Troubleshooting
### Common Issues and Solutions

### 1. Port Already in Use
### Error: "Port 8000 is already in use"
Find process using port
lsof -i :8000   # macOS/Linux
netstat -ano | findstr :8000  # Windows

Kill process or change port in docker-compose.yml

### 2. Docker Not Running
### Error: "Cannot connect to Docker daemon"
Start Docker Desktop application
Or start Docker service (Linux):
sudo systemctl start docker

### 3. Services Won't Start
### Check logs for errors
### docker-compose logs

### Common fixes:

docker-compose down
docker system prune -f
docker-compose up --build -d

### 4. Database Connection Failed
Check MySQL container logs
docker-compose logs mysql

Reset database container
docker-compose down -v
docker-compose up mysql -d

Wait 60 seconds, then start other services
docker-compose up backend frontend -d

### 5. Frontend Shows Connection Error
Verify backend is running
curl http://localhost:8000/health

Check frontend logs
docker-compose logs frontend

Restart frontend with fresh container
docker-compose restart frontend

### 6. Sample Data Missing
Reload sample data
docker-compose exec mysql mysql -u smarttrack_user -p smarttrack_db < database/sample_data.sql


### Performance Optimization
### Docker Settings
Increase Docker Desktop memory allocation to 4GB+
In Docker Desktop: Settings → Resources → Memory


### Database Optimization
sql-- Connect to database and optimize
docker-compose exec mysql mysql -u smarttrack_user -p smarttrack_db

-- Optimize tables
OPTIMIZE TABLE products, sales, expenses, sale_items;

-- Check index usage
SHOW INDEX FROM products;
