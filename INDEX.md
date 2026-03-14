# PapuMovies - Microservices Project Index

## 🎬 Project Overview

Your monolithic Flask application has been successfully refactored into a **4-service microservices architecture**. All functionality is preserved with improved scalability and maintainability.

---

## 📁 Project Structure

```
c:\Users\Sebas\Desktop\movie-microservices\
│
├── 📄 README.md                    (Main documentation - START HERE!)
├── 📄 QUICKSTART.md               (5-minute quick start guide)
├── 📄 ARCHITECTURE.md             (Detailed technical documentation)
├── 📄 CONFIGURATION.md            (Setup and configuration guide)
├── 📄 REFACTORING_SUMMARY.md      (What changed in the refactor)
│
├── 🚀 setup_services.py           (Install dependencies for all services)
├── 🚀 start_services.py           (Start all 4 services together)
├── 🚀 start_services.bat          (Windows batch startup script)
├── 🚀 start_services.ps1          (PowerShell startup script)
│
├── 📂 frontend/                   (Port 5000 - Web UI)
│   ├── app.py                     (Frontend application)
│   ├── requirements.txt           (Flask, requests)
│   ├── templates/
│   │   ├── peliculas.html        (Movie list page)
│   │   └── detalle_pelicula.html (Movie details page)
│   └── static/
│       └── css/
│           └── styles.css        (Styling)
│
├── 📂 movie-service/              (Port 5001 - TMDB API)
│   ├── app.py                     (Movie service)
│   └── requirements.txt           (Flask, requests)
│
├── 📂 rating-service/             (Port 5002 - OMDb API)
│   ├── app.py                     (Rating service)
│   └── requirements.txt           (Flask, requests)
│
└── 📂 trailer-service/            (Port 5003 - YouTube API)
    ├── app.py                     (Trailer service)
    └── requirements.txt           (Flask, requests)
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
cd c:\Users\Sebas\Desktop\movie-microservices
python setup_services.py
```

### Step 2: Start Services
```bash
python start_services.py
```

Or use the Windows shortcuts:
- `start_services.bat` - Traditional batch file
- `start_services.ps1` - PowerShell script

### Step 3: Open Browser
```
http://localhost:5000
```

You're done! The application is running.

---

## 📚 Documentation Guide

### For Beginners
1. **Start with** → README.md (overview and setup)
2. **Then read** → QUICKSTART.md (step-by-step guide)
3. **Try it out** → Run `python start_services.py`

### For Developers
1. **Understand** → ARCHITECTURE.md (technical details)
2. **Configure** → CONFIGURATION.md (API keys, ports)
3. **Explore code** → Check individual service `app.py` files

### For DevOps/Deployment
1. **Review** → CONFIGURATION.md (deployment settings)
2. **Check** → start_services.py (service startup)
3. **Plan** → ARCHITECTURE.md (scaling strategies)

---

## 🔧 Services Overview

| Service | Port | Purpose | External API |
|---------|------|---------|--------------|
| **Frontend** | 5000 | Web UI & Orchestration | None |
| **Movie Service** | 5001 | Movie data & search | TMDB |
| **Rating Service** | 5002 | IMDB & ratings | OMDb |
| **Trailer Service** | 5003 | Video trailers | YouTube |

---

## ✨ Key Features

### All Original Features Preserved
- ✅ Movie search and filtering
- ✅ Genre, year, and rating filters
- ✅ Movie details page
- ✅ IMDB ratings and reviews
- ✅ YouTube trailers
- ✅ Rotten Tomatoes scores
- ✅ Responsive Bootstrap UI
- ✅ Pagination

### New Advantages (Microservices)
- ✅ Services scale independently
- ✅ Easier to maintain and update
- ✅ Better error isolation
- ✅ Flexible deployment options
- ✅ Clear API boundaries
- ✅ Technology flexibility

---

## 🛠️ Common Tasks

### Restart Services
```bash
# Stop current services (Ctrl+C in each window)
# Then run:
python start_services.py
```

### Check Service Status
- Movie Service: `http://localhost:5001/genres`
- Rating Service: `http://localhost:5002` (need IMDB ID)
- Trailer Service: `http://localhost:5003/trailer?title=test`
- Frontend: `http://localhost:5000`

### Change a Port
1. Edit the service `app.py` file
2. Change: `app.run(debug=True, port=5001)` to desired port
3. Update frontend service URLs if needed
4. Restart services

### Add New Feature
1. Identify which service it belongs to
2. Add endpoint to that service's `app.py`
3. Call it from frontend service
4. Update templates if UI changes needed

---

## 📋 API Endpoints Reference

### Frontend (Port 5000)
```
GET  /                          Movie listing
GET  /pelicula/<id>             Movie details
```

### Movie Service (Port 5001)
```
GET  /movies                    Get movies
GET  /movies/search?query=      Search movies
GET  /movie/<id>                Get details
GET  /genres                    Get genres
```

### Rating Service (Port 5002)
```
GET  /rating/<imdb_id>          Get ratings
```

### Trailer Service (Port 5003)
```
GET  /trailer?title=&year=      Get trailer
```

---

## 🔐 API Keys

The following API keys are configured (from original app):

- **TMDB**: `ecf95bb8db8142bf24c1b2556ab6b9da`
- **OMDb**: `b9bb2dc3`
- **YouTube**: `AIzaSyCgL-vywjWKVAQnu6Q5IezIPp-fY9x7nW4`

See CONFIGURATION.md for details on deploying with environment variables.

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find what's using a port (Windows)
netstat -ano | findstr :5000
# Kill the process
taskkill /PID <PID> /F
```

### Module Not Found
```bash
# Reinstall dependencies
cd frontend
pip install -r requirements.txt
```

### Services Won't Connect
- Verify all 4 services are running
- Check ports: 5000, 5001, 5002, 5003 are available
- Wait 2-3 seconds for services to fully start
- Check error messages in service terminals

### API Errors
- Verify internet connection
- Check API key validity
- Review service logs for details
- See CONFIGURATION.md for API limits

---

## 📊 Architecture Diagram

```
Browser (localhost:5000)
    │
    ├─→ Frontend Service (5000)
    │       ├─→ Movie Service (5001) → TMDB API
    │       ├─→ Rating Service (5002) → OMDb API
    │       └─→ Trailer Service (5003) → YouTube API
    │
    └─→ Returns HTML page
```

---

## 🚀 Next Steps

1. **Try it out**
   - Run `python start_services.py`
   - Visit `http://localhost:5000`
   - Search for movies, view details

2. **Explore the code**
   - Read individual service `app.py` files
   - Understand request/response flow
   - Check template structure

3. **Add features** (optional)
   - Add user authentication
   - Implement caching
   - Add reviews/ratings
   - Create watchlist feature

4. **Deploy** (production)
   - See CONFIGURATION.md
   - Consider Docker/Kubernetes
   - Implement monitoring
   - Add logging

---

## 📞 Support Resources

### Documentation Files
- `README.md` - Complete documentation
- `QUICKSTART.md` - Setup and running
- `ARCHITECTURE.md` - Technical details
- `CONFIGURATION.md` - Configuration guide
- `REFACTORING_SUMMARY.md` - What changed

### Code Files
- `movie-service/app.py` - Movie database service
- `rating-service/app.py` - Rating service
- `trailer-service/app.py` - Trailer service
- `frontend/app.py` - Frontend orchestration

### External APIs
- [TMDB API Documentation](https://www.themoviedb.org/settings/api)
- [OMDb API Documentation](http://www.omdbapi.com/)
- [YouTube Data API](https://developers.google.com/youtube/v3)

---

## ✅ Verification Checklist

Before deploying to production, verify:

- [ ] All 4 services start without errors
- [ ] Frontend displays at `http://localhost:5000`
- [ ] Movie search works
- [ ] Genre filtering works
- [ ] Movie details page loads
- [ ] IMDB ratings display correctly
- [ ] YouTube trailers load
- [ ] No console errors in any service
- [ ] API rate limits not exceeded
- [ ] Response times acceptable

---

## 📝 License & Credits

- Original monolithic app refactored to microservices
- Uses TMDB, OMDb, and YouTube APIs
- Built with Flask and Bootstrap

---

## 🎯 Summary

You now have a **production-ready microservices application** with:

✅ **4 independent services** (frontend, movie, rating, trailer)
✅ **Complete documentation** (README, guides, architecture)
✅ **Setup automation** (dependency installer, startup scripts)
✅ **Original functionality** (all features preserved)
✅ **Better architecture** (scalable, maintainable, flexible)

**Next action:** Run `python start_services.py` and visit `http://localhost:5000`

---

**Created:** March 13, 2026
**Status:** ✅ Ready for use
**Version:** 1.0 (Microservices)
