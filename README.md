![GitHub last commit](https://img.shields.io/github/last-commit/madcowGit/imdbscraper?style=for-the-badge&logo=github)
![GitHub issues](https://img.shields.io/github/issues/madcowGit/imdbscraper?style=for-the-badge&logo=github)
![GitHub stars](https://img.shields.io/github/stars/madcowGit/imdbscraper?style=for-the-badge&logo=github)
![GitHub release](https://img.shields.io/github/v/release/madcowGit/imdbscraper?style=for-the-badge&logo=github)
![Docker](https://img.shields.io/badge/Docker-ready-blue?style=for-the-badge&logo=docker)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)

# Description
This is a docker container flask app that scrapes an IMDB list (and works for lists consisting of multiple pages) and returns a list for Radarr or Sonarr. Supports watchlists (ur######) and other lists (ls#########)

## Radarr
a list is returned in StevenLu Custom format (for use in e.g. Radarr) 
`[{"imdb_id": "tt16744566"},{"imdb_id": "tt32243339"}]`

see: [https://wiki.servarr.com/radarr/supported#stevenlu2import](https://wiki.servarr.com/radarr/supported#stevenlu2import)
## Sonarr
an imdb list is read and filtered to get all tvshows. Then the tvdb api is used to lookup the tvdbId. This list is returned in Sonarr Custom format 
`[{ "tvdbId": "75837" }, { "tvdbId": "77847" }, { "tvdbId": "78299" }, { "tvdbId": "72756" } ]`

note that this format is not documenten in [https://wiki.servarr.com/sonarr/supported#lists](https://wiki.servarr.com/sonarr/supported#lists)

# Deploy
Endpoint for movies on list:
`http://<your-url:port>/scrape_movies?list_id=<imdblistid>`

Endpoint for tv shows on list:
`http://<your-url:port>/scrape_tvshows?list_id=<imdblistid>`

## Example docker-compose
use a secrets file to store the api key from tvdb
```
version: "3.9"
services:
 imdbscraper:
  image: ghcr.io/madcowgit/imdbscraper:latest
  ports:
    - "10001:10000"
  environment:
    - TVDBAPISECRETSFILE=/run/secrets/tvdbapikeyfile
  restart: unless-stopped
  secrets:
    - tvdbapikeyfile

secrets:
  tvdbapikeyfile:
    file: ./tvdbapikey
```

use for ghcr.io/madcowgit/imdbscraper:latest for working releases. I use ghcr.io/madcowgit/imdbscraper:devel to try out new stuff so that often does not work

## usage example:
### Radarr
choose StevenLu Custom list
point URL to `http://<your-url:port>/scrape_movies?list_id=ur196653258`
### Sonarr
choose Advanced Custom list
point URL to `http://<your-url:port>/scrape_tvshows?list_id=ls505433927`
