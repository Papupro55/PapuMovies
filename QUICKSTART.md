# Quick Start Guide - PapuMovies Microservices

## 1. Initial Setup (One-Time)

### Step 1: Install Python Dependencies

Run in each service directory:

```bash
# Frontend Service
cd frontend
pip install -r requirements.txt

# Return to root and go to next service
cd ..

# Movie Service
cd movie-service
pip install -r requirements.txt
cd ..

# Rating Service
cd rating-service
pip install -r requirements.txt
cd ..

# Trailer Service
cd trailer-service
pip install -r requirements.txt
cd ..
```

Or use the provided setup script:
```bash
# Windows
python setup_services.py

# Or manually for each service
pip install Flask==2.3.3 requests==2.31.0
```

## 2. Running the Application

### Option A: Using Batch Script (Windows)
```bash
start_services.bat
```

### Option B: Using PowerShell Script (Windows)
```powershell
.\start_services.ps1
```

### Option C: Manual Startup - Open 4 Terminal Windows

**Terminal 1 - Movie Service:**
```bash
cd movie-service
python app.py
# Output: Running on http://127.0.0.1:5001
```

**Terminal 2 - Rating Service:**
```bash
cd rating-service
python app.py
# Output: Running on http://127.0.0.1:5002
```

**Terminal 3 - Trailer Service:**
```bash
cd trailer-service
python app.py
# Output: Running on http://127.0.0.1:5003
```

**Terminal 4 - Frontend Service:**
```bash
cd frontend
python app.py
# Output: Running on http://127.0.0.1:5000
```

## 3. Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## 4. Verify Everything is Working

### Check Service Health:
- Movie Service: http://localhost:5001/genres
- Rating Service: http://localhost:5002 (any endpoint with valid IMDB ID)
- Trailer Service: http://localhost:5003/trailer?title=Matrix&year=1999
- Frontend: http://localhost:5000

### Log Output Should Show:
```
* Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
* Running on http://127.0.0.1:5001 (Press CTRL+C to quit)
* Running on http://127.0.0.1:5002 (Press CTRL+C to quit)
* Running on http://127.0.0.1:5003 (Press CTRL+C to quit)
```

## 5. Common Issues & Solutions

### Port Already in Use
```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (Windows)
taskkill /PID <PID> /F
```

### Module Not Found Error
```bash
# Make sure you're in the correct directory
# and installed dependencies
pip install -r requirements.txt
```

### Connection Refused
- Ensure all 4 services are running
- Check that services are on correct ports
- Wait a moment for services to fully start

### API Key Errors
- Verify API keys in configuration files
- Check API key limits haven't been exceeded
- Ensure internet connection is working

## 6. Testing Individual Services

### Test Movie Service
```bash
curl http://localhost:5001/movies
curl http://localhost:5001/genres
curl http://localhost:5001/movie/550
```

### Test Rating Service
```bash
# Need valid IMDB ID
curl http://localhost:5002/rating/tt0137523
```

### Test Trailer Service
```bash
curl "http://localhost:5003/trailer?title=The%20Matrix&year=1999"
```

### Test Frontend
```bash
curl http://localhost:5000/
```

## 7. Stopping Services

### Using Batch/PowerShell
- Close the terminal windows opened by the scripts

### Manual Terminals
- Press `CTRL+C` in each terminal window

## 8. Project Structure Reference

```
movie-microservices/
├── frontend/                    # Port 5000 - Web UI
│   ├── app.py                  # Main frontend application
│   ├── requirements.txt        # Dependencies
│   ├── templates/              # HTML files
│   │   ├── peliculas.html     # Movie list page
│   │   └── detalle_pelicula.html  # Movie detail page
│   └── static/                 # Static files
│       └── css/
│           └── styles.css
├── movie-service/              # Port 5001 - TMDB API
│   ├── app.py                  # Movie service
│   └── requirements.txt        # Dependencies
├── rating-service/             # Port 5002 - OMDb API
│   ├── app.py                  # Rating service
│   └── requirements.txt        # Dependencies
├── trailer-service/            # Port 5003 - YouTube API
│   ├── app.py                  # Trailer service
│   └── requirements.txt        # Dependencies
├── README.md                   # Full documentation
├── CONFIGURATION.md            # Configuration guide
├── QUICKSTART.md              # This file
├── start_services.bat         # Windows batch starter
└── start_services.ps1         # PowerShell starter
```

## 9. Next Steps

Once everything is working:
1. Explore the application - search for movies, add filters
2. Check each endpoint in the README.md
3. Review the code in each service
4. Consider adding features:
   - User authentication
   - Favorites/watchlist
   - Reviews/comments
   - Caching
   - Rate limiting

## 10. Production Deployment

For deploying to production:
1. Use environment variables for API keys
2. Enable HTTPS
3. Add authentication
4. Use Docker containers
5. Set up API Gateway
6. Implement logging and monitoring
7. Add error handling
8. Use a database for caching
9. Implement circuit breakers

See CONFIGURATION.md for security recommendations.

---

**Need Help?**
- Check README.md for full documentation
- Review CONFIGURATION.md for setup details
- Check service logs for error messages
