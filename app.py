from flask import Flask, request, jsonify
from imdbscraper import get_list

app = Flask(__name__)


@app.route('/scrape', methods=['GET'])
def scrape():
    # only use list_id as input
    list_id = request.args.get('list_id')
    if not list_id:
        return jsonify({"error": "Missing 'list' parameter"}), 400

    movies = get_list(list_id)

    return movies

@app.route('/getmovies', methods=['GET'])    
def getmovies():
    # only use list_id as input
    list_id = request.args.get('list_id')
    if not list_id:
        return jsonify({"error": "Missing 'list' parameter"}), 400

    movies = get_movies(list_id)

    return movies
    
def gettvshows():
    # only use list_id as input
    list_id = request.args.get('list_id')
    if not list_id:
        return jsonify({"error": "Missing 'list' parameter"}), 400

    movies = get_list(list_id)

    return movies

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
