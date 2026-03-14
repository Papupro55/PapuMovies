from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OMDB_API_KEY = 'b9bb2dc3'


@app.route('/rating/<imdb_id>', methods=['GET'])
def get_rating(imdb_id):
    """Get IMDB rating information for a movie"""
    try:
        endpoint = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        response = requests.get(endpoint)
        data = response.json()
        
        if data.get("Response") == "False":
            return jsonify({'error': data.get('Error')}), 404
        
        # Extract Rotten Tomatoes rating if available
        rotten_rating = None
        for rating in data.get('Ratings', []):
            if rating.get('Source') == 'Rotten Tomatoes':
                rotten_rating = rating.get('Value')
                break
        
        return jsonify({
            'rating': data.get('imdbRating', 'N/A'),
            'votes': data.get('imdbVotes', 'N/A'),
            'rotten': rotten_rating if rotten_rating else 'N/A',
            'metascore': data.get('Metascore', 'N/A'),
            'type': data.get('Type', ''),
            'title': data.get('Title', ''),
            'year': data.get('Year', '')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5002)
