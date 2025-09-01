from flask import Flask, request, jsonify
from imdbscraper import get_movies, get_tvshows

app = Flask(__name__)

@app.route('/scrape_movies', methods=['GET'])    
def scrape_movies():
    # only use list_id as input
    list_id = request.args.get('list_id')
    if not list_id:
        return jsonify({"error": "Missing 'list' parameter"}), 400

    movies = get_movies(list_id)

    return movies

@app.route('/scrape_tvshows', methods=['GET'])    
def scrape_tvshows():
    # only use list_id as input
    list_id = request.args.get('list_id')
    if not list_id:
        return jsonify({"error": "Missing 'list' parameter"}), 400

    tvshows = get_tvshows(list_id)

    return tvshows

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
