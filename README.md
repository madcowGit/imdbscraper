# Description
This is a docker container flask app that scrapes an IMDB list and returns them in StevenLu Custom format (for use in e.g. Radarr) and works for lists consisting of multiple pages

# Output
Output is formatted so that Radarr will accept it as a StevenLu Custom list.
It is a JSON containing only imdb_ids

```
[
  {
    "imdb_id": "tt16744566"
  },
  {
    "imdb_id": "tt32243339"
  }
]
```

# Deploy
`http://<your-url:port>/scrape?list_id=<imdblistid>`

## Example docker-compose

```
version: "3.9"
services:
 imdbscraper:
  container_name: imdblistscraper
  image: ghcr.io/madcowgit/imdbscraper:latest
  ports:
    - "10000:10000"
  restart: unless-stopped
```
## usage example:
### Radarr
choose StevenLu Custom list
point URL to `http://<your-url:port>/scrape?list_id=ls040455003`
### curl
`curl http://<your-url:port>/scrape?list_id=ls040455003`
