from flask import Flask, request, jsonify
import requests
from urllib.parse import quote
import os

app = Flask(__name__)

YOUTUBE_API_KEY = 'AIzaSyCgL-vywjWKVAQnu6Q5IezIPp-fY9x7nW4'


@app.route('/trailer', methods=['GET'])
def get_trailer():
    """Get YouTube trailer for a movie"""
    try:
        movie_title = request.args.get('title', '')
        year = request.args.get('year', '')
        
        if not movie_title:
            return jsonify({'error': 'Title parameter is required'}), 400
        
        search_query = f"{movie_title} {year} official trailer"
        endpoint = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={quote(search_query)}&key={YOUTUBE_API_KEY}&maxResults=1"
        
        response = requests.get(endpoint)
        data = response.json()
        
        if data.get('items'):
            video_id = data['items'][0]['id']['videoId']
            return jsonify({
                'trailer_url': f"https://www.youtube.com/embed/{video_id}",
                'video_id': video_id,
                'title': data['items'][0]['snippet']['title']
            })
        else:
            return jsonify({'error': 'No trailer found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    app.run(host="0.0.0.0", port=port)
