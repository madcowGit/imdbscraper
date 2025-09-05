from flask import Flask, request, jsonify
from imdbscraper import get_movies, get_tvshows 
import os
import requests

app = Flask(__name__)
#app.debug = True

# Load TVDB API key from Docker secrets file
secrets_file_path = os.environ.get("TVDBAPISECRETSFILE")
if secrets_file_path and os.path.exists(secrets_file_path):
    with open(secrets_file_path, "r") as f:
        tvdbapikey = f.read().strip()
else:
    tvdbapikey = None

    
@app.route('/scrape_movies', methods=['GET'])    
def scrape_movies():
    # only use list_id as input
    list_id = request.args.get('list_id')
    if not list_id:
        return jsonify({"error": "Missing 'list' parameter"}), 400

    movies = get_movies(list_id)

    return jsonify(movies)

@app.route('/scrape_tvshows', methods=['GET'])    
def scrape_tvshows():
    # only use list_id as input
    list_id = request.args.get('list_id')
    if not list_id:
        return jsonify({"error": "Missing 'list_id' parameter"}), 400
    if not tvdbapikey:
        print("TVDB API key not configured")
        return jsonify({"error": "TVDB API key not configured"}), 500

    tvshows = get_tvshows(list_id,tvdbapikey)

    return jsonify(tvshows)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
