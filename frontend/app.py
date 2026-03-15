from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Service URLs
MOVIE_SERVICE_URL = 'https://movie-service-pcuu.onrender.com'
RATING_SERVICE_URL = 'https://rating-service-sk4h.onrender.com'
TRAILER_SERVICE_URL = 'https://trailer-service.onrender.com'


def get_genres():
    """Get all genres from movie service"""
    try:
        response = requests.get(f'{MOVIE_SERVICE_URL}/genres', timeout=5)
        return response.json().get('genres', {})
    except Exception as e:
        print(f"Error getting genres: {e}")
        return {}


@app.route('/')
def index():
    """Display movies with search and filter options"""
    try:
        page = request.args.get('pagina', 1, type=int)
        query = request.args.get('busqueda')
        genre = request.args.get('genero')
        year = request.args.get('año')
        rating = request.args.get('clasificacion')
        
        # Build parameters for movie service
        params = {
            'page': page
        }
        
        if query:
            params['query'] = query
        if genre:
            params['genre'] = genre
        if year:
            params['year'] = year
        if rating:
            params['rating'] = rating
        
        # Call movie service
        response = requests.get(f'{MOVIE_SERVICE_URL}/movies', params=params, timeout=5)
        data = response.json()
        
        genres_dict = get_genres()
        
        return render_template(
            'peliculas.html',
            peliculas=data.get('movies', []),
            pagina_actual=data.get('current_page', 1),
            total_paginas=data.get('total_pages', 1),
            generos_disponibles=genres_dict,
            filtros_actuales={
                'busqueda': query,
                'genero': genre,
                'año': year,
                'clasificacion': rating
            }
        )
    
    except Exception as e:
        print(f"Error in index: {e}")
        return render_template(
            'peliculas.html',
            peliculas=[],
            pagina_actual=1,
            total_paginas=1,
            generos_disponibles=get_genres(),
            filtros_actuales={
                'busqueda': None,
                'genero': None,
                'año': None,
                'clasificacion': None
            }
        )


@app.route('/pelicula/<int:movie_id>')
def detalle_pelicula(movie_id):
    """Display detailed information about a movie"""
    try:
        # Get movie details from movie service
        movie_response = requests.get(f'{MOVIE_SERVICE_URL}/movie/{movie_id}', timeout=5)
        movie_data = movie_response.json()
        
        if 'error' in movie_data:
            return "There was an error papu, no data Found for this movie :c", 404
        
        # Get IMDB rating if imdb_id exists
        imdb_data = None
        imdb_id = movie_data.get('imdb_id', '')
        if imdb_id:
            try:
                rating_response = requests.get(
                    f'{RATING_SERVICE_URL}/rating/{imdb_id}',
                    timeout=5
                )
                imdb_data = rating_response.json()
                if 'error' in imdb_data:
                    imdb_data = None
            except Exception as e:
                print(f"Error getting IMDB rating: {e}")
                imdb_data = None
        
        # Get trailer from trailer service
        trailer = None
        try:
            trailer_params = {
                'title': movie_data.get('title', ''),
                'year': movie_data.get('release_date', '')[:4]
            }
            trailer_response = requests.get(
                f'{TRAILER_SERVICE_URL}/trailer',
                params=trailer_params,
                timeout=5
            )
            trailer_data = trailer_response.json()
            if 'trailer_url' in trailer_data:
                trailer = trailer_data['trailer_url']
        except Exception as e:
            print(f"Error getting trailer: {e}")
            trailer = None
        
        # Extract genre names
        genre_names = [genre.get('name', '') for genre in movie_data.get('genres', [])]
        
        return render_template(
            'detalle_pelicula.html',
            pelicula=movie_data,
            imdb=imdb_data,
            trailer=trailer,
            generos=genre_names
        )
    
    except Exception as e:
        print(f"Error in detalle_pelicula: {e}")
        return "There was an error papu, no data Found for this movie :c", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)