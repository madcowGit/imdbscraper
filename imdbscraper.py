
from flask import Flask, request, jsonify, current_app
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

def get_tvshows(list_id, api_key):
    listitems = get_list(list_id)
    tvshows_filtered = [item for item in listitems if item.get("type").lower() in ['tv series', 'tv mini series', 'tv episode', 'tv special']]
    
    def get_tvdb_token(api_key):
        url = "https://api4.thetvdb.com/v4/login"
        payload = {"apikey": api_key}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["data"]["token"]


    jwt_token = get_tvdb_token(api_key)
    
    def testToken(token):
        url = "https://api4.thetvdb.com/v4/user"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        # Check if the token is valid
        if response.status_code == 200:
            print("✅ Token is valid.") 
            if current_app.debug:
                print(response.json())
        else:                     
            if current_app.debug:
                print(response.status_code)
                print(response.text)
            print(f"❌ Token is invalid or expired. Status code: {response.status_code}")

    #testToken(jwt_token)    

    def get_tvdb_id(imdb_id, token=None):
        
        if current_app.debug:
            print(imdb_id)
            print(token)
            
        url = f"https://api4.thetvdb.com/v4/search/remoteid/{imdb_id}"
        headers = {"Authorization": f"Bearer {token}"}        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if current_app.debug:
            print(data)                
        
        if data["data"]:
            if set(data["data"][0].keys()) == {"series"}:
                return data["data"][0]["series"]["id"]
            elif set(data["data"][0].keys()) == {"movie"}:
                return data["data"][0]["movie"]["id"]
            else:
                print(data["data"][0].keys())    # Should show: dict_keys(['---something-----'])

            
        else:
            return None


    tvshows_tvdb = []
    for show in tvshows_filtered:
        imdb_id = show.get('imdb_id')
        if imdb_id:
            tvdb_id = get_tvdb_id(imdb_id, jwt_token)
            tvshows_tvdb.append({
                'imdb_id': imdb_id,
                'tvdbId': tvdb_id
            })

    return jsonify(tvshows_tvdb)

if __name__ == '__main__':
    print("hello world")
