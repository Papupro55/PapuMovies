# PapuMovies Architecture Documentation

## Overview

This document provides a comprehensive overview of the PapuMovies microservices architecture, explaining how the monolithic application has been refactored into independent, scalable services.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT BROWSER                           │
│                    http://localhost:5000                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                   ┌─────────▼──────────┐
                   │   Frontend Service │
                   │    (Port 5000)     │
                   │   - Templates      │
                   │   - Routing        │
                   │   - Orchestration  │
                   └────┬──────┬──────┬─┘
        ┌──────────────┐ │      │      │ ┌──────────────────┐
        │              │ │      │      │ │                  │
   ┌────▼──────┐  ┌───▼──┐ ┌──▼──┐ ┌─▼───┐         │
   │   Movie    │  │      │ │    │ │     │         │
   │  Service   │  │      │ │    │ │     │         │
   │ (Port 5001)│  │      │ │    │ │     │         │
   │            │  │      │ │    │ │     │         │
   │ - Search   │  │      │ │    │ │     │         │
   │ - Filter   │  │      │ │    │ │     │         │
   │ - Details  │  │      │ │    │ │     │         │
   └──────┬─────┘  │      │ │    │ │     │         │
          │        │      │ │    │ │     │         │
          │   ┌────▼───┐ ┌▼──┐ ┌┴──┐     │
          │   │ Rating │ │   │ │   │     │
          │   │Service │ │   │ │   │     │
          │   │(5002)  │ │   │ │   │     │
          │   │        │ │   │ │   │     │
          │   │- IMDB  │ │   │ │   │     │
          │   │- RT    │ │   │ │   │     │
          │   └────┬───┘ │   │ │   │     │
          │        │     │   │ │   │     │
          │   ┌────▼────────┐ │ │   │     │
          │   │  Trailer    │ │ │   │     │
          │   │  Service    │ │ │   │     │
          │   │  (Port 5003)│ │ │   │     │
          │   │             │ │ │   │     │
          │   │ - YouTube   │ │ │   │     │
          │   │   Trailers  │ │ │   │     │
          │   └──────┬──────┘ │ │   │     │
          │          │        │ │   │     │
          └─→ TMDB   │        │ │   │     │
             API     │        │ │   │     │
                     └──→ OMDb│ │   │     │
                         API │ │   │     │
                             └─→ YouTube
                                 API
```

## Service Breakdown

### 1. Frontend Service (Port 5000)

**Responsibility:** User Interface and Request Orchestration

**Key Features:**
- Renders HTML templates
- Handles user requests
- Communicates with backend services
- Manages pagination and filters
- Error handling and fallbacks

**Routes:**
```
GET  /                    - Movie listing with filters
GET  /pelicula/<id>       - Movie details page
```

**Dependencies:**
- Flask 2.3.3
- Requests 2.31.0

**Data Flow:**
1. User accesses `/` endpoint
2. Frontend calls Movie Service for movies
3. Frontend calls Movie Service for genres
4. Returns rendered HTML template

For movie details:
1. User clicks on movie
2. Frontend calls Movie Service for movie details
3. Frontend calls Rating Service for IMDB ratings
4. Frontend calls Trailer Service for YouTube trailer
5. Returns rendered details page

---

### 2. Movie Service (Port 5001)

**Responsibility:** TMDB API Integration and Movie Data Management

**Key Features:**
- Interfaces with The Movie Database API
- Searches and filters movies
- Returns movie details
- Manages genre information
- Caches genre data at startup

**Endpoints:**
```
GET  /movies              - Get popular/filtered movies
GET  /movies/search       - Search for movies by query
GET  /movie/<id>          - Get detailed movie information
GET  /genres              - Get all available genres
```

**Query Parameters:**
- `/movies`: `page`, `query`, `genre`, `year`, `rating`
- `/movies/search`: `query`, `page`
- `/genres`: None

**Response Format (JSON):**
```json
{
  "movies": [
    {
      "id": 550,
      "title": "Fight Club",
      "release_date": "1999",
      "poster_path": "/path",
      "vote_average": 8.8,
      "overview": "...",
      "genre_ids": ["Drama", "Thriller"],
      "imdb_id": "tt0137523"
    }
  ],
  "current_page": 1,
  "total_pages": 500
}
```

**External API:** The Movie Database (TMDB)
- Base URL: `https://api.themoviedb.org/3`
- API Key: Required
- Rate Limit: 40 requests per 10 seconds

---

### 3. Rating Service (Port 5002)

**Responsibility:** OMDb API Integration and Rating Information

**Key Features:**
- Interfaces with OMDb API
- Retrieves IMDB ratings and votes
- Fetches Rotten Tomatoes scores
- Returns multiple rating sources

**Endpoints:**
```
GET  /rating/<imdb_id>    - Get ratings for a movie
```

**Response Format (JSON):**
```json
{
  "rating": "8.8",
  "votes": "2,000,000",
  "rotten": "67%",
  "metascore": "67",
  "type": "movie",
  "title": "Fight Club",
  "year": "1999"
}
```

**External API:** OMDb API
- Base URL: `http://www.omdbapi.com/`
- API Key: Required
- Rate Limit: Depends on tier (free has limitations)

---

### 4. Trailer Service (Port 5003)

**Responsibility:** YouTube API Integration and Trailer Discovery

**Key Features:**
- Searches YouTube Data API
- Finds official movie trailers
- Returns embeddable video URLs
- Handles search query formatting

**Endpoints:**
```
GET  /trailer?title=<title>&year=<year>  - Get YouTube trailer
```

**Query Parameters:**
- `title`: Movie title (required)
- `year`: Release year (optional)

**Response Format (JSON):**
```json
{
  "trailer_url": "https://www.youtube.com/embed/6JnN232i2b0",
  "video_id": "6JnN232i2b0",
  "title": "The Matrix Official Trailer"
}
```

**External API:** YouTube Data API v3
- Base URL: `https://www.googleapis.com/youtube/v3/`
- API Key: Required
- Quota: 10,000 units per day

---

## Technology Stack

### Backend Framework
- **Flask 2.3.3**
  - Lightweight web framework
  - Easy service creation
  - Built-in development server

### Communication
- **HTTP/REST**
  - Standard protocol
  - Requests library for inter-service communication
  - JSON for data exchange

### External APIs
- **TMDB API**: Movie data, genres, ratings
- **OMDb API**: IMDB ratings, reviews
- **YouTube API v3**: Trailer search and retrieval

### Frontend
- **HTML/Bootstrap 5.3.0**: Responsive UI
- **Jinja2**: Template rendering
- **Bootstrap Icons**: UI icons

---

## Communication Flow

### Scenario 1: User Views Movie List

```
1. Browser → Frontend: GET /
2. Frontend → Movie Service: GET /movies?page=1
3. Movie Service → TMDB API: Request popular movies
4. TMDB API → Movie Service: Return movies JSON
5. Frontend → Movie Service: GET /genres
6. Movie Service → Frontend: Return genres
7. Frontend → Browser: Render HTML with movies
```

### Scenario 2: User Views Movie Details

```
1. Browser → Frontend: GET /pelicula/550
2. Frontend → Movie Service: GET /movie/550
3. Movie Service → TMDB API: Request movie details
4. TMDB API → Movie Service: Return movie details
5. Movie Service → Frontend: Return JSON
6. Frontend → Rating Service: GET /rating/tt0137523
7. Rating Service → OMDb API: Request ratings
8. OMDb API → Rating Service: Return ratings
9. Rating Service → Frontend: Return JSON
10. Frontend → Trailer Service: GET /trailer?title=Fight%20Club&year=1999
11. Trailer Service → YouTube API: Search trailer
12. YouTube API → Trailer Service: Return video ID
13. Trailer Service → Frontend: Return embed URL
14. Frontend → Browser: Render HTML with all details
```

---

## Data Models

### Movie Object (from TMDB)
```python
{
    'id': int,                    # Movie ID
    'title': str,                 # Movie title
    'release_date': str,          # YYYY-MM-DD format
    'poster_path': str,           # Image path (partial URL)
    'backdrop_path': str,         # Background image
    'overview': str,              # Movie description
    'genre_ids': [int],           # Genre IDs
    'vote_average': float,        # TMDB rating
    'vote_count': int,            # Number of votes
    'runtime': int,               # Duration in minutes
    'budget': int,                # Budget in dollars
    'revenue': int,               # Revenue in dollars
    'imdb_id': str,               # IMDB ID (tt+7 digits)
    'tagline': str                # Movie tagline
}
```

### Rating Object (from OMDb)
```python
{
    'rating': str,                # IMDB rating (e.g., "8.8")
    'votes': str,                 # Number of votes
    'rotten': str,                # Rotten Tomatoes % (e.g., "67%")
    'metascore': str,             # Metascore (e.g., "67")
    'type': str,                  # Type (movie, series, etc)
    'title': str,                 # Movie title
    'year': str                   # Release year
}
```

### Trailer Object (from YouTube)
```python
{
    'trailer_url': str,           # Embed URL
    'video_id': str,              # YouTube video ID
    'title': str                  # Video title
}
```

---

## Error Handling

### Frontend Service
- Returns 404 if movie not found
- Returns 500 for server errors
- Falls back gracefully if services unavailable
- Timeout handling (5 seconds per service)

### Movie Service
- Returns 400 for invalid parameters
- Returns 404 if movie not found
- Returns 500 for TMDB API errors
- Limits results to 20 per page

### Rating Service
- Returns 404 if IMDB ID not found
- Returns error message from OMDb API
- Returns N/A for missing data fields

### Trailer Service
- Returns 400 if title parameter missing
- Returns 404 if no trailer found
- Handles YouTube API errors gracefully

---

## Performance Considerations

### Caching
- **Genres cached at startup** (Movie Service)
  - Reduces API calls significantly
  - Updated on service restart

### Rate Limiting
- **TMDB:** 40 requests per 10 seconds
- **OMDb:** Depends on API tier
- **YouTube:** 10,000 quota units per day

### Response Times
- **Movie Service:** ~200-500ms (depends on TMDB)
- **Rating Service:** ~100-300ms (depends on OMDb)
- **Trailer Service:** ~300-800ms (depends on YouTube)
- **Frontend:** ~500ms-1.5s (depends on all services)

---

## Scalability

### Horizontal Scaling
Each service can be scaled independently:
```
Frontend: Multiple instances behind load balancer
Movie Service: Cache results, add Redis layer
Rating Service: Implement caching for IMDB IDs
Trailer Service: Cache trailer URLs by movie title
```

### Vertical Scaling
- Increase service memory/CPU allocation
- Implement caching layers
- Optimize database queries

---

## Monitoring & Logging

Recommended additions:
1. **Logging**
   - Log all API calls
   - Track response times
   - Monitor errors

2. **Health Checks**
   - `/health` endpoint on each service
   - Monitor service availability

3. **Metrics**
   - Request counts
   - Error rates
   - Response times

4. **Alerting**
   - Service down alerts
   - API quota warnings
   - Performance degradation

---

## Deployment

### Development
- Run 4 services locally on different ports
- Use Python development server

### Production
1. **Containerization**
   - Docker for each service
   - Docker Compose for orchestration

2. **Infrastructure**
   - Kubernetes for orchestration
   - Load balancer for frontend

3. **Security**
   - Use environment variables for API keys
   - HTTPS for all communications
   - API gateway with rate limiting
   - Authentication/authorization

4. **Monitoring**
   - ELK Stack for logging
   - Prometheus for metrics
   - Grafana for dashboards

---

## Future Enhancements

1. **Database Layer**
   - Cache frequently accessed movies
   - Store user watchlists
   - Save user preferences

2. **Authentication**
   - User registration/login
   - JWT tokens
   - Role-based access control

3. **Features**
   - User reviews and ratings
   - Favorites/watchlist
   - Recommendations engine
   - Social sharing

4. **Advanced Caching**
   - Redis for distributed caching
   - Cache invalidation strategies
   - Content delivery network (CDN)

5. **API Gateway**
   - Request routing
   - Rate limiting
   - Request/response transformation
   - API versioning

---

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [TMDB API](https://www.themoviedb.org/settings/api)
- [OMDb API](http://www.omdbapi.com/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Microservices Architecture Best Practices](https://microservices.io/)
