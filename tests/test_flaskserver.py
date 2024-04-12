"""
Module for testing the Flask server.
"""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.flaskserver import app


class FlaskServerTestCase(unittest.TestCase):
    """
    Test case for the Flask server.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.app = app.test_client()

    def test_get_free_spots_negative(self):
        """
        Test getting free spots with a negative number.
        """
        with patch('backend.database.fetch_available_spots', return_value=-1):
            response = self.app.get('/free_spots')
            self.assertEqual(response.status_code, 500)

    def test_get_free_spots_non_integer(self):
        """
        Test getting free spots with a non-integer value.
        """
        with patch('backend.database.fetch_available_spots', return_value='ten'):
            response = self.app.get('/free_spots')
            self.assertEqual(response.status_code, 500)

    def test_get_free_spots_none(self):
        """
        Test getting free spots with a None value.
        """
        with patch('backend.database.fetch_available_spots', return_value=None):
            response = self.app.get('/free_spots')
            self.assertEqual(response.status_code, 500)

    def test_get_free_spots_exception(self):
        """
        Test getting free spots when an exception is raised.
        """
        with patch(
            'backend.database.fetch_available_spots',
            side_effect=Exception('Database error')
        ):
            response = self.app.get('/free_spots')
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.get_json())

    def test_get_free_handicap_spots_negative(self):
        """
        Test getting free handicap spots with a negative number.
        """
        with patch('backend.database.fetch_available_handicap_spots', return_value=-1):
            response = self.app.get('/free_handicap_spots')
            self.assertEqual(response.status_code, 500)

    def test_get_free_handicap_spots_non_integer(self):
        """
        Test getting free handicap spots with a non-integer value.
        """
        with patch('backend.database.fetch_available_handicap_spots', return_value='ten'):
            response = self.app.get('/free_handicap_spots')
            self.assertEqual(response.status_code, 500)

    def test_get_free_handicap_spots_none(self):
        """
        Test getting free handicap spots with a None value.
        """
        with patch('backend.database.fetch_available_handicap_spots', return_value=None):
            response = self.app.get('/free_handicap_spots')
            self.assertEqual(response.status_code, 500)

    def test_get_free_handicap_spots_exception(self):
        """
        Test getting free handicap spots when an exception is raised.
        """
        with patch(
            'backend.database.fetch_available_handicap_spots',
            side_effect=Exception('Database error')
        ):
            response = self.app.get('/free_handicap_spots')
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.get_json())


if __name__ == '__main__':
    unittest.main()
