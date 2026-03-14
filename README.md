# PapuMovies - Microservices Architecture

This is a refactored version of the original monolithic Flask application, now split into independent microservices.

## Architecture Overview

### Services

1. **Frontend Service** (Port 5000)
   - Renders HTML templates
   - Calls the three backend services
   - File: `frontend/app.py`

2. **Movie Service** (Port 5001)
   - Handles TMDB API interactions
   - Provides movie search, filters, and details
   - File: `movie-service/app.py`
   - Endpoints:
     - `GET /movies` - Get popular movies or filtered movies
     - `GET /movies/search` - Search for movies
     - `GET /movie/<id>` - Get movie details
     - `GET /genres` - Get available genres

3. **Rating Service** (Port 5002)
   - Handles OMDb API interactions
   - Provides IMDB ratings and reviews
   - File: `rating-service/app.py`
   - Endpoints:
     - `GET /rating/<imdb_id>` - Get IMDB ratings for a movie

4. **Trailer Service** (Port 5003)
   - Handles YouTube API interactions
   - Provides movie trailers
   - File: `trailer-service/app.py`
   - Endpoints:
     - `GET /trailer?title=<title>&year=<year>` - Get YouTube trailer

## Project Structure

```
movie-microservices/
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   │   ├── peliculas.html
│   │   └── detalle_pelicula.html
│   └── static/
│       └── css/
│           └── styles.css
├── movie-service/
│   ├── app.py
│   └── requirements.txt
├── rating-service/
│   ├── app.py
│   └── requirements.txt
├── trailer-service/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Navigate to each service directory and install dependencies:

```bash
# Frontend Service
cd frontend
pip install -r requirements.txt

# Movie Service
cd ../movie-service
pip install -r requirements.txt

# Rating Service
cd ../rating-service
pip install -r requirements.txt

# Trailer Service
cd ../trailer-service
pip install -r requirements.txt
```

## Running the Services

You need to run **four terminal sessions**, one for each service. Start the services in the following order:

### Terminal 1 - Movie Service (Port 5001)
```bash
cd movie-service
python app.py
```

### Terminal 2 - Rating Service (Port 5002)
```bash
cd rating-service
python app.py
```

### Terminal 3 - Trailer Service (Port 5003)
```bash
cd trailer-service
python app.py
```

### Terminal 4 - Frontend Service (Port 5000)
```bash
cd frontend
python app.py
```

## Accessing the Application

Once all services are running, open your web browser and navigate to:

```
http://localhost:5000
```

## API Documentation

### Frontend Service (Port 5000)

#### Home Page
- **URL:** `GET http://localhost:5000/`
- **Query Parameters:**
  - `pagina` - Page number (default: 1)
  - `busqueda` - Search query
  - `genero` - Genre ID
  - `año` - Release year
  - `clasificacion` - Rating (G, PG, PG-13, R)

#### Movie Details
- **URL:** `GET http://localhost:5000/pelicula/<movie_id>`
- **Response:** HTML with movie details, ratings, and trailer

### Movie Service (Port 5001)

#### Get Movies
- **URL:** `GET http://localhost:5001/movies`
- **Query Parameters:**
  - `page` - Page number
  - `query` - Search query
  - `genre` - Genre ID
  - `year` - Release year
  - `rating` - Movie rating

#### Get Movie Details
- **URL:** `GET http://localhost:5001/movie/<movie_id>`
- **Response:** JSON with complete movie information

#### Get Genres
- **URL:** `GET http://localhost:5001/genres`
- **Response:** JSON with all available genres

### Rating Service (Port 5002)

#### Get IMDB Rating
- **URL:** `GET http://localhost:5002/rating/<imdb_id>`
- **Response:** JSON with IMDB ratings and reviews

### Trailer Service (Port 5003)

#### Get Trailer
- **URL:** `GET http://localhost:5003/trailer?title=<title>&year=<year>`
- **Response:** JSON with YouTube trailer embed URL

## Features

✅ Independent microservices architecture
✅ Service isolation and separation of concerns
✅ Scalable - each service can be scaled independently
✅ Loosely coupled - services communicate via HTTP/REST
✅ Easy to maintain - each service has its own codebase
✅ Multiple API integrations (TMDB, OMDb, YouTube)
✅ Movie search and filtering
✅ Movie details with ratings and trailers
✅ Responsive Bootstrap UI

## Troubleshooting

### Service Connection Errors
- Ensure all services are running on their respective ports
- Check that no other services are using ports 5000-5003
- Verify firewall settings allow local connections

### API Errors
- Verify API keys are correct in each service
- Check internet connection for external API calls
- Services may timeout if APIs are slow

### Port Already in Use
If a port is already in use, modify the port number in the respective `app.py` file and update the service URLs in `frontend/app.py`

## Future Improvements

- Add service discovery (Consul, Eureka)
- Implement API Gateway
- Add authentication/authorization
- Implement circuit breaker pattern
- Add caching layers
- Implement load balancing
- Add Docker containerization
- Add comprehensive logging and monitoring
- Implement message queues for async operations
