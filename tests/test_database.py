"""
This module contains unit tests for the database module.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock
import mysql.connector

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database import fetch_available_spots, store_free_spots


class TestDatabase(unittest.TestCase):
    """
    This class contains unit tests for the database module.
    """

    def test_fetch_available_spots_with_result(self):
        """
        Test case for fetch_available_spots when the database returns a result.
        """
        # Create mock objects for the database connection and cursor
        mock_cursor = MagicMock()
        # Simulate a database response of 5 available parking spots
        mock_cursor.fetchone.return_value = (5,)
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        # Replace the actual database connection with the mock connection
        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_available_spots()

        # Assert that the function correctly interpreted the mock database response
        self.assertEqual(result, 5)
        # Assert that the function made the correct database query
        mock_cursor.execute.assert_called_once_with("SELECT PARKSPOTS FROM AVAILABLE_SPOTS")
        # Assert that the function correctly closed the database connection
        mock_cnx.close.assert_called_once()

    def test_fetch_available_spots_with_no_result(self):
        """
        Test case for fetch_available_spots when the database returns no result.
        """
        # Create mock objects for the database connection and cursor
        mock_cursor = MagicMock()
        # Simulate a database response of no available parking spots
        mock_cursor.fetchone.return_value = None
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        # Replace the actual database connection with the mock connection
        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_available_spots()

        # Assert that the function correctly interpreted the mock database response
        self.assertEqual(result, 0)
        # Assert that the function made the correct database query
        mock_cursor.execute.assert_called_once_with("SELECT PARKSPOTS FROM AVAILABLE_SPOTS")
        # Assert that the function correctly closed the database connection
        mock_cnx.close.assert_called_once()

    def test_fetch_available_spots_with_error(self):
        """
        Test case for fetch_available_spots when the database throws an error.
        """
        # Create mock objects for the database connection and cursor
        mock_cursor = MagicMock()
        # Simulate a database error when executing the query
        mock_cursor.execute.side_effect = mysql.connector.Error
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        # Replace the actual database connection with the mock connection
        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            result = fetch_available_spots()

        # Assert that the function correctly handled the database error
        self.assertIsNone(result)
        # Assert that the function attempted to make the correct database query
        mock_cursor.execute.assert_called_once_with("SELECT PARKSPOTS FROM AVAILABLE_SPOTS")
        # Assert that the function correctly closed the database connection
        mock_cnx.close.assert_called_once()

    def test_store_free_spots(self):
        """
        Test case for store_free_spots.
        """
        # Create mock objects for the database connection and cursor
        mock_cursor = MagicMock()
        mock_cnx = MagicMock()
        mock_cnx.cursor.return_value = mock_cursor

        # Replace the actual database connection with the mock connection
        with unittest.mock.patch('backend.database.connect_to_db', return_value=mock_cnx):
            store_free_spots(5)

        # Assert that the function made the correct database query
        query = "UPDATE AVAILABLE_SPOTS SET PARKSPOTS = %s WHERE id = %s"
        mock_cursor.execute.assert_called_once_with(query, (5, 1))
        # Assert that the function correctly committed the database transaction
        mock_cnx.commit.assert_called_once()
        # Assert that the function correctly closed the database connection
        mock_cnx.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
