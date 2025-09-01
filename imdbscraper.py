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
            #"title": item['title'],
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
        paged_url = f"{base_url}&page={page_num}"
        raw_json = get_html(paged_url)
        next_page, processed_json = process_json(raw_json)

    movies = update_list(movies, processed_json)

    return jsonify(movies)
    
    
def get_movies(list_id):
    moviesjson = get_list(list_id)
    return moviesjson

if __name__ == '__main__':
    # do nothing
    print("hello world")
