
import unittest
from unittest.mock import patch, MagicMock
from app import app
import imdbscraper
import os

# Load TVDB API key from GithubActions secrets file
tvdbapikey = os.environ.get("TVDBAPIKEY")
    
class TestIMDBScraper(unittest.TestCase):
    def test_get_movies(self):
        return_value = [{"imdb_id":"tt11655566","type":"Movie"},{"imdb_id":"tt33130902","type":"TV Special"},{"imdb_id":"tt31908384","type":"TV Movie"},{"imdb_id":"tt1118511","type":"Short"}]
        response = imdbscraper.get_movies('ls569954785')
        self.assertIn(return_value, json.dumps(response))

    def test_get_tvshows(self):
        return_value = [{"tvdbId":'350984'},{"tvdbId":'251645'}]
        response = imdbscraper.get_tvshows('ls569954785', tvdbapikey)
        self.assertIn(return_value, json.dumps(response))

class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_scrape_movies_route(self):   
        return_value = app.response_class(
            response='[{"imdb_id":"tt11655566","type":"Movie"},{"imdb_id":"tt33130902","type":"TV Special"},{"imdb_id":"tt31908384","type":"TV Movie"},{"imdb_id":"tt1118511","type":"Short"}]',
            status=200,
            mimetype='application/json'
        )
        response = self.app.get('/scrape_movies?list_id=ls569954785')
        self.assertEqual(response.status_code, 200)

    def test_scrape_tvshows_route(self):   
        return_value = app.response_class(
            response='[{"tvdbId":350984},{"tvdbId":251645}]',
            status=200,
            mimetype='application/json'
        )
        response = self.app.get('/scrape_tvshows?list_id=ls569954785')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
