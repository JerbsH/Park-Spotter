"""
This module contains unit tests for the database module.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock
import mysql.connector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# required functions from backend.database
from backend.database import (
    fetch_available_free_spots,
    fetch_available_handicap_spots,
    save_available_free_spots,
    save_available_handicap_spots,
    fetch_token,
    save_token,
    fetch_image,
    save_image,
    fetch_total_spots,
    save_total_spots
)

class TestDatabase(unittest.TestCase):
    """
    This class contains unit tests for the database module.
    """

    def test_fetch_token_with_result(self):
        """
        Test case for fetch_token when the database returns a result.
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("token123",)
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_token()

        self.assertEqual(result, "token123")
        mock_cursor.execute.assert_called_once_with("SELECT TOKEN FROM DEVICE_TOKEN")
        mock_cnx.close.assert_called_once()

    def test_fetch_token_with_no_result(self):
        """
        Test case for fetch_token when the database returns no result.
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_token()

        self.assertEqual(result, 0)
        mock_cursor.execute.assert_called_once_with("SELECT TOKEN FROM DEVICE_TOKEN")
        mock_cnx.close.assert_called_once()

    def test_fetch_token_with_error(self):
        """
        Test case for fetch_token when the database throws an error.
        """
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mysql.connector.Error
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_token()

        self.assertEqual(result, 0)
        mock_cursor.execute.assert_called_once_with("SELECT TOKEN FROM DEVICE_TOKEN")
        mock_cnx.close.assert_called_once()

    def test_save_token(self):
        """
        Test case for save_token.
        """
        mock_cursor = MagicMock()
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            save_token("token123")

        query = (
            "INSERT INTO DEVICE_TOKEN (ID, TOKEN) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE TOKEN = %s"
        )
        mock_cursor.execute.assert_called_once_with(query, (1, "token123", "token123"))
        mock_cnx.commit.assert_called_once()
        mock_cnx.close.assert_called_once()

    def test_save_token_with_error(self):
        """
        Test case for save_token when the database throws an error.
        """
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mysql.connector.Error
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = save_token("token123")

        self.assertEqual(result, 0)
        query = (
            "INSERT INTO DEVICE_TOKEN (ID, TOKEN) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE TOKEN = %s"
        )
        mock_cursor.execute.assert_called_once_with(query, (1, "token123", "token123"))
        mock_cnx.close.assert_called_once()

    def test_fetch_available_spots_with_result(self):
        """
        Test case for fetch_available_spots when the database returns a result.
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (5,)
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_available_free_spots()

        self.assertEqual(result, 5)
        mock_cursor.execute.assert_called_once_with("SELECT PARKSPOTS FROM AVAILABLE_SPOTS")
        mock_cnx.close.assert_called_once()

    def test_fetch_available_spots_with_no_result(self):
        """
        Test case for fetch_available_spots when the database returns no result.
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_available_free_spots()

        self.assertEqual(result, 0)
        mock_cursor.execute.assert_called_once_with("SELECT PARKSPOTS FROM AVAILABLE_SPOTS")
        mock_cnx.close.assert_called_once()

    def test_fetch_available_spots_with_error(self):
        """
        Test case for fetch_available_spots when the database throws an error.
        """
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mysql.connector.Error
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_available_free_spots()

        self.assertEqual(result, {'error': 'Unknown error'})
        mock_cursor.execute.assert_called_once_with("SELECT PARKSPOTS FROM AVAILABLE_SPOTS")
        mock_cnx.close.assert_called_once()

    def test_save_free_spots(self):
        """
        Test case for saving free spots.
        """
        mock_cursor = MagicMock()
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            save_available_free_spots(5)

        query = "UPDATE AVAILABLE_SPOTS SET PARKSPOTS = %s WHERE id = %s"
        mock_cursor.execute.assert_called_once_with(query, (5, 1))
        mock_cnx.commit.assert_called_once()
        mock_cnx.close.assert_called_once()

    def test_fetch_available_handicap_spots_with_result(self):
        """
        Test case for fetch_available_handicap_spots when the database returns a result.
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (3,)
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_available_handicap_spots()

        self.assertEqual(result, 3)
        mock_cursor.execute.assert_called_once_with("SELECT HANDICAPSPOTS FROM AVAILABLE_SPOTS")
        mock_cnx.close.assert_called_once()

    def test_save_free_handicap_spots(self):
        """
        Test case for saving free handicap spots.
        """
        mock_cursor = MagicMock()
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            save_available_handicap_spots(3)

        query = "UPDATE AVAILABLE_SPOTS SET HANDICAPSPOTS = %s WHERE id = %s"
        mock_cursor.execute.assert_called_once_with(query, (3, 1))
        mock_cnx.commit.assert_called_once()
        mock_cnx.close.assert_called_once()

    def test_fetch_image(self):
        """
        Test case for fetch_image.
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("image_path",)
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_image()

        self.assertEqual(result, "image_path")
        mock_cursor.execute.assert_called_once_with("SELECT IMAGE FROM AVAILABLE_SPOTS")
        mock_cnx.close.assert_called_once()

    def test_save_image(self):
        """
        Test case for save_image.
        """
        mock_cursor = MagicMock()
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            save_image("image_path")

        query = "UPDATE AVAILABLE_SPOTS SET IMAGE = %s WHERE id = %s"
        mock_cursor.execute.assert_called_once_with(query, ("image_path", 1))
        mock_cnx.commit.assert_called_once()
        mock_cnx.close.assert_called_once()

    def test_fetch_total_spots(self):
        """
        Test case for fetch_total_spots.
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (10,)
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_total_spots()

        self.assertEqual(result, 10)
        mock_cursor.execute.assert_called_once_with("SELECT TOTALSPOTS FROM AVAILABLE_SPOTS")
        mock_cnx.close.assert_called_once()

    def test_save_total_spots(self):
        """
        Test case for save_total_spots.
        """
        mock_cursor = MagicMock()
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            save_total_spots(10)

        query = "UPDATE AVAILABLE_SPOTS SET TOTALSPOTS = %s WHERE id = %s"
        mock_cursor.execute.assert_called_once_with(query, (10, 1))
        mock_cnx.commit.assert_called_once()
        mock_cnx.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
