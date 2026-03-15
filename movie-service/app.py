from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TMDB_API_KEY = 'ecf95bb8db8142bf24c1b2556ab6b9da'
BASE_URL = 'https://api.themoviedb.org/3'
LANGUAGE = 'en-US'

# Get genres at startup
response = requests.get(f'{BASE_URL}/genre/movie/list?api_key={TMDB_API_KEY}&language={LANGUAGE}')
GENRES = {g['id']: g['name'] for g in response.json().get('genres', [])}


@app.route('/movies', methods=['GET'])
def get_movies():
    """Get popular or filtered movies"""
    try:
        page = request.args.get('page', 1, type=int)
        query = request.args.get('query')
        genre = request.args.get('genre')
        year = request.args.get('year')
        rating = request.args.get('rating')
        
        params = {
            'api_key': TMDB_API_KEY,
            'language': LANGUAGE,
            'page': page,
            'region': 'US'
        }
        
        if query:
            endpoint = f'{BASE_URL}/search/movie'
            params['query'] = query
        elif genre or year or rating:
            endpoint = f'{BASE_URL}/discover/movie'
            if genre:
                params['with_genres'] = genre
            if year:
                params['primary_release_year'] = year
            if rating:
                params['certification_country'] = 'US'
                params['certification'] = rating
        else:
            endpoint = f'{BASE_URL}/movie/popular'
        
        response = requests.get(endpoint, params=params)
        data = response.json()
        
        movies = []
        for movie in data.get('results', []):
            movies.append({
                'id': movie.get('id'),
                'title': movie.get('title'),
                'release_date': movie.get('release_date', '')[:4],
                'poster_path': movie.get('poster_path'),
                'vote_average': movie.get('vote_average'),
                'overview': movie.get('overview'),
                'genre_ids': [GENRES.get(gid, '') for gid in movie.get('genre_ids', [])],
                'imdb_id': movie.get('imdb_id', '')
            })
        
        return jsonify({
            'movies': movies[:20],
            'current_page': data.get('page', 1),
            'total_pages': min(data.get('total_pages', 1), 500)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/movies/search', methods=['GET'])
def search_movies():
    """Search for movies by query"""
    try:
        query = request.args.get('query', '')
        page = request.args.get('page', 1, type=int)
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        params = {
            'api_key': TMDB_API_KEY,
            'language': LANGUAGE,
            'query': query,
            'page': page
        }
        
        response = requests.get(f'{BASE_URL}/search/movie', params=params)
        data = response.json()
        
        movies = []
        for movie in data.get('results', []):
            movies.append({
                'id': movie.get('id'),
                'title': movie.get('title'),
                'release_date': movie.get('release_date', '')[:4],
                'poster_path': movie.get('poster_path'),
                'vote_average': movie.get('vote_average'),
                'overview': movie.get('overview'),
                'genre_ids': [GENRES.get(gid, '') for gid in movie.get('genre_ids', [])],
            })
        
        return jsonify({
            'movies': movies[:20],
            'current_page': data.get('page', 1),
            'total_pages': min(data.get('total_pages', 1), 500)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    """Get detailed information about a movie"""
    try:
        endpoint = f'{BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language={LANGUAGE}&append_to_response=videos'
        response = requests.get(endpoint)
        movie_data = response.json()
        
        return jsonify({
            'id': movie_data.get('id'),
            'title': movie_data.get('title'),
            'overview': movie_data.get('overview'),
            'release_date': movie_data.get('release_date'),
            'poster_path': movie_data.get('poster_path'),
            'backdrop_path': movie_data.get('backdrop_path'),
            'vote_average': movie_data.get('vote_average'),
            'vote_count': movie_data.get('vote_count'),
            'runtime': movie_data.get('runtime'),
            'tagline': movie_data.get('tagline'),
            'imdb_id': movie_data.get('imdb_id'),
            'genres': [{'id': g['id'], 'name': g['name']} for g in movie_data.get('genres', [])],
            'budget': movie_data.get('budget'),
            'revenue': movie_data.get('revenue'),
            'production_companies': movie_data.get('production_companies', [])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/genres', methods=['GET'])
def get_genres():
    """Get all available genres"""
    return jsonify({'genres': GENRES})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)