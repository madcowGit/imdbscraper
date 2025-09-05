
import unittest
from unittest.mock import patch, MagicMock
from app import app
import imdbscraper

class TestIMDBScraper(unittest.TestCase):

    @patch('imdbscraper.get_list')
    def test_get_movies(self, mock_get_list):
        mock_get_list.return_value = [
            {'imdb_id': 'tt1234567', 'type': 'movie'},
            {'imdb_id': 'tt7654321', 'type': 'tv series'}
        ]
        response = imdbscraper.get_movies('ls123')
        self.assertEqual(response.status_code, 200)
        self.assertIn({'imdb_id': 'tt1234567', 'type': 'movie'}, response.json)

    @patch('imdbscraper.get_list')
    @patch('imdbscraper.get_tvdb_id')
    @patch('imdbscraper.get_tvdb_token')
    def test_get_tvshows(self, mock_token, mock_tvdb_id, mock_get_list):
        mock_token.return_value = 'fake_token'
        mock_tvdb_id.return_value = 12345
        mock_get_list.return_value = [
            {'imdb_id': 'tt1234567', 'type': 'tv series'},
            {'imdb_id': 'tt7654321', 'type': 'movie'}
        ]
        response = imdbscraper.get_tvshows('ls123', 'fake_api_key')
        self.assertEqual(response.status_code, 200)
        self.assertIn({'tvdbId': 12345}, response.json)

class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('imdbscraper.get_movies')
    def test_scrape_movies_route(self, mock_get_movies):
        mock_get_movies.return_value = app.response_class(
            response='[{"imdb_id": "tt1234567", "type": "movie"}]',
            status=200,
            mimetype='application/json'
        )
        response = self.app.get('/scrape_movies?list_id=ls123')
        self.assertEqual(response.status_code, 200)

    @patch('imdbscraper.get_tvshows')
    def test_scrape_tvshows_route(self, mock_get_tvshows):
        mock_get_tvshows.return_value = app.response_class(
            response='[{"tvdbId": 12345}]',
            status=200,
            mimetype='application/json'
        )
        with patch('app.tvdbapikey', 'fake_api_key'):
            response = self.app.get('/scrape_tvshows?list_id=ls123')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
