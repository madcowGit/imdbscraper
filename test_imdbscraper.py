
import unittest
from unittest.mock import patch, MagicMock
from app import app
import imdbscraper
import os
import json

print("test full flask app")
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
        print(response.status_code)
        print(response.get_json())
        self.assertEqual(json.loads(return_value.get_data()), json.loads(response.get_data(as_text=True)))
        self.assertEqual(response.status_code, 200)
    
    def test_scrape_movies_watchlist_route(self):   
        # only check if response is ok
        return_value = app.response_class(
            response='[{"imdb_id":0000},{"imdb_id":0000}]',
            status=200,
            mimetype='application/json'
        )
        response = self.app.get('/scrape_tvshows?list_id=ur18834365')
        self.assertEqual(response.status_code, 200)    

if __name__ == '__main__':
    unittest.main()
