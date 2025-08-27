import requests, json, jmespath, os
from lxml import html


url = "https://www.imdb.com/list/ls060044601/?sort=release_date%2Cdesc"
#url = "https://www.imdb.com/list/ls040455003/?sort=release_date%2Cdesc"
#url = "https://www.imdb.com/pt/list/ls024863935/?sort=release_date%2Cdesc"
xpath = "props.pageProps.mainColumnData.list.titleListItemSearch."
headers={"User-Agent": "Mozilla/5.0"}

def get_html(url):
    # get page
    resp = requests.get(
        url, 
        headers={"User-Agent": "Mozilla/5.0"}
    )
    if resp.status_code != 200:
        print("Error fetching: %s" % (resp.status_code))
        exit(1)
    tree = html.fromstring(resp.content)
    script = tree.xpath('//script[@id="__NEXT_DATA__"]/text()')
    return json.loads(script[0])


def process_json(raw_json):
    # process output
    next_page = jmespath.search(f"{xpath}pageInfo.hasNextPage", raw_json)    
    processed_json = jmespath.search(xpath + "edges[].listItem.{id: id, title: titleText.text}", raw_json)

    return next_page, processed_json

def update_list(movies,processed_json):
    # add items to movies list
    for item in processed_json:
        imdb_id = item['id']
        title = item['title']
        movies.append({
            "title": title,
            "imdb_id": imdb_id
        })
    return movies

# get initial page
raw_json = get_html(url)
total = jmespath.search(f"{xpath}total", raw_json) # how many items on the list?

# process the first page
next_page, processed_json = process_json(raw_json)

# add to movies list and continue for all pages
movies = []
while next_page:
    print(len(movies), "of", total)
    movies = update_list(movies,processed_json)
        
    raw_json = get_html(url+f"&page={len(movies)//250+1}")
    next_page, processed_json = process_json(raw_json)

# one more time for the last page
movies = update_list(movies,processed_json)

print(total)


# convert list to json
json_dumps = json.dumps(movies, indent=2, ensure_ascii=False)

print(json_dumps)
print(movies.__len__())
#with open('./data/list_1001_movies_before_die.json', 'w', encoding='utf-8') as file:
#    json.dump(movies_sorted, file, indent=2)
