
from flask import Flask, request, jsonify
import requests, json, jmespath
from lxml import html

xpath = "props.pageProps.mainColumnData.list.titleListItemSearch."

def get_html(url):
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        return None
    tree = html.fromstring(resp.content)
    script = tree.xpath('//script[@id="__NEXT_DATA__"]/text()')
    return json.loads(script[0])

def process_json(raw_json):
    next_page = jmespath.search(f"{xpath}pageInfo.hasNextPage", raw_json)
    processed_json = jmespath.search(xpath + "edges[].listItem.{id: id, title: titleText.text, type: titleType.text}", raw_json)
    return next_page, processed_json

def update_list(movies, processed_json):
    for item in processed_json:
        movies.append({
            "imdb_id": item['id'],
            "type": item.get('type', '') 
        })
    return movies

def get_list(list_id):
    base_url = f"https://www.imdb.com/list/{list_id}/?sort=release_date,desc"
    raw_json = get_html(base_url)
    if not raw_json:
        return jsonify({"error": "Failed to fetch IMDb page"}), 500

    total = jmespath.search(f"{xpath}total", raw_json)
    next_page, processed_json = process_json(raw_json)

    movies = []
    page_num = 1
    while next_page:
        movies = update_list(movies, processed_json)
        page_num += 1
        paged_url = f"{base_url}&amp;page={page_num}"
        raw_json = get_html(paged_url)
        next_page, processed_json = process_json(raw_json)

    movies = update_list(movies, processed_json)
    return movies

def get_movies(list_id):
    listitems = get_list(list_id)
    movies_filtered = [item for item in listitems if item.get("type").lower() in ['movie', 'tv movie']]
    return jsonify(movies_filtered)

def get_tvshows(list_id, jwt_token):
    listitems = get_list(list_id)
    tvshows_filtered = [item for item in listitems if item.get("type").lower() in ['tv series', 'tv mini series', 'tv episode', 'tv special']]

    def get_tvdb_id(imdb_id, token=None):
        if token is None:
            raise Exception("TVDb JWT token not provided.")
        url = f"https://api4.thetvdb.com/v4/search?imdbId={imdb_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if "data" in data and data["data"]:
            return data["data"][0].get("tvdb_id") or data["data"][0].get("id")
        return None

    tvshows_tvdb = []
    for show in tvshows_filtered:
        imdb_id = show.get('imdb_id')
        if imdb_id:
            tvdb_id = get_tvdb_id(imdb_id, token=jwt_token)
            tvshows_tvdb.append({
                'imdb_id': imdb_id,
                'tvdbId': tvdb_id
            })

    return jsonify(tvshows_tvdb)

if __name__ == '__main__':
    print("hello world")
