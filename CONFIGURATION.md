# PapuMovies - Configuration Guide

## API Keys

This application uses three external APIs. You need to obtain API keys from each:

### 1. The Movie Database (TMDB)
- **Website:** https://www.themoviedb.org/settings/api
- **Current Key:** ecf95bb8db8142bf24c1b2556ab6b9da
- **File:** `movie-service/app.py`
- **Line:** `TMDB_API_KEY = 'ecf95bb8db8142bf24c1b2556ab6b9da'`

### 2. OMDb API (IMDB Ratings)
- **Website:** http://www.omdbapi.com/apikey.aspx
- **Current Key:** b9bb2dc3
- **File:** `rating-service/app.py`
- **Line:** `OMDB_API_KEY = 'b9bb2dc3'`

### 3. YouTube Data API v3
- **Website:** https://developers.google.com/youtube/v3/getting-started
- **Current Key:** AIzaSyCgL-vywjWKVAQnu6Q5IezIPp-fY9x7nW4
- **File:** `trailer-service/app.py`
- **Line:** `YOUTUBE_API_KEY = 'AIzaSyCgL-vywjWKVAQnu6Q5IezIPp-fY9x7nW4'`

## Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 5000 | Main web application |
| Movie Service | 5001 | TMDB API wrapper |
| Rating Service | 5002 | OMDb API wrapper |
| Trailer Service | 5003 | YouTube API wrapper |

## Changing Ports

If any of the default ports are already in use, you can change them:

1. **Frontend:** Edit `frontend/app.py`, change `app.run(debug=True, port=5000)`
2. **Movie Service:** Edit `movie-service/app.py`, change `app.run(debug=True, port=5001)`
3. **Rating Service:** Edit `rating-service/app.py`, change `app.run(debug=True, port=5002)`
4. **Trailer Service:** Edit `trailer-service/app.py`, change `app.run(debug=True, port=5003)`
5. **Update Frontend URLs:** Edit `frontend/app.py` and update the service URLs:
   ```python
   MOVIE_SERVICE_URL = 'http://localhost:5001'  # Change 5001 if needed
   RATING_SERVICE_URL = 'http://localhost:5002'  # Change 5002 if needed
   TRAILER_SERVICE_URL = 'http://localhost:5003'  # Change 5003 if needed
   ```

## Environment Configuration (Optional - For Production)

For better security in production, use environment variables instead of hardcoding API keys:

### Template Environment File (.env)
```
# Movie Service
TMDB_API_KEY=ecf95bb8db8142bf24c1b2556ab6b9da

# Rating Service
OMDB_API_KEY=b9bb2dc3

# Trailer Service
YOUTUBE_API_KEY=AIzaSyCgL-vywjWKVAQnu6Q5IezIPp-fY9x7nW4

# Service Ports
MOVIE_SERVICE_PORT=5001
RATING_SERVICE_PORT=5002
TRAILER_SERVICE_PORT=5003
FRONTEND_PORT=5000

# Service URLs
MOVIE_SERVICE_URL=http://localhost:5001
RATING_SERVICE_URL=http://localhost:5002
TRAILER_SERVICE_URL=http://localhost:5003
```

### Using Environment Variables in Code (Example)
```python
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'default_key')
OMDB_API_KEY = os.getenv('OMDB_API_KEY', 'default_key')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'default_key')
```

Install python-dotenv:
```bash
pip install python-dotenv
```

## API Limits

- **TMDB:** 40 requests per 10 seconds
- **OMDb:** Free tier limited requests, paid tier available
- **YouTube:** 10,000 quota units per day

## Troubleshooting Configuration Issues

### API Keys Not Working
- Verify keys are correctly copied without extra spaces
- Check API key expiration date on respective websites
- Ensure API is enabled in accounts

### Service Communication Fails
- Confirm all services are running
- Check firewall allowing localhost connections
- Verify service URLs in frontend/app.py match actual ports

### Port Conflicts
Use command to find what's using a port:
```bash
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Mac/Linux
```

## Security Recommendations

For production deployment:

1. **Move API keys to environment variables**
2. **Use API Gateway for rate limiting**
3. **Implement CORS properly**
4. **Add authentication/authorization**
5. **Use HTTPS instead of HTTP**
6. **Implement request validation**
7. **Add error handling and logging**
8. **Use Docker for containerization**
9. **Implement secrets management**
