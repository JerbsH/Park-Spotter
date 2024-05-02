"""The code connects to a MySQL database
and fetches all the rows from a table."""

import os
import logging
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

def connect_to_db():
    """Connects to the database and returns the connection object."""
    try:
        cnx = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        return cnx
    except mysql.connector.Error as err:
        logging.error('Error connecting to the database %s', err)
        return None

def fetch_token():
    """Fetches token from the database."""
    cnx = connect_to_db()
    if cnx is None:
        return 0

    try:
        cursor = cnx.cursor()
        query = "SELECT TOKEN FROM DEVICE_TOKEN"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            print(f"Fetched token:{result[0]}")  # Debugging print statement
            return result[0]
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()

    print("No available tokens found")
    return 0

def save_token(token):
    """save token to the database."""
    cnx = connect_to_db()
    if cnx is None:
        return 0

    try:
        cursor = cnx.cursor()
        query = "INSERT INTO DEVICE_TOKEN (ID, TOKEN) VALUES (%s, %s) ON DUPLICATE KEY UPDATE TOKEN = %s"
        cursor.execute(query, (1, token, token))
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        print("No available tokens found")
    finally:
        cnx.close()

    print("Token saved successfully")
    return 0

def fetch_available_free_spots():
    """Fetches the available parking spots from the database."""
    cnx = connect_to_db()
    if cnx is None:
        return 0

    try:
        cursor = cnx.cursor()
        query = "SELECT PARKSPOTS FROM AVAILABLE_SPOTS"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            print(f"Fetched {result[0]} available spots")  # Debugging print statement
            return result[0]
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        return {"error": str(err)}
    finally:
        cnx.close()

    print("No available spots found")
    return 0

def save_available_free_spots(free_spots):
    """Stores the number of free parking spots in the database."""
    cnx = connect_to_db()
    if cnx is None:
        return

    try:
        cursor = cnx.cursor()
        query = "UPDATE AVAILABLE_SPOTS SET PARKSPOTS = %s WHERE id = %s"
        cursor.execute(query, (free_spots, 1))
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()

def fetch_available_handicap_spots():
    """Fetches the available handicap parking spots from the database."""
    cnx = connect_to_db()
    if cnx is None:
        return 0

    try:
        cursor = cnx.cursor()
        query = "SELECT HANDICAPSPOTS FROM AVAILABLE_SPOTS"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            print(f"Fetched {result[0]} available handicap spots")  # Debugging print statement
            return result[0]
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()

    print("No available handicap spots found")
    return 0

def save_available_handicap_spots(free_handicap_spots):
    """Stores the number of free handicap parking spots in the database."""
    cnx = connect_to_db()
    if cnx is None:
        return

    try:
        cursor = cnx.cursor()
        query = "UPDATE AVAILABLE_SPOTS SET HANDICAPSPOTS = %s WHERE id = %s"
        cursor.execute(query, (free_handicap_spots, 1))
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()


def fetch_total_handicap_spots():
    """Fetches the total handicap parking spots from the database."""
    cnx = connect_to_db()
    if cnx is None:
        return 0

    try:
        cursor = cnx.cursor()
        query = "SELECT TOTALHANDICAPSPOTS FROM AVAILABLE_SPOTS"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            print(f"Fetched total handicap spots:{result[0]}")  # Debugging print statement
            return result[0]
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()

    print("No total handicap spots found")
    return 0

def save_total_handicap_spots(total_handicap_spots):
    """Saves the total handicap parking spots to the database."""
    if not isinstance(total_handicap_spots, int):
        print(f"Invalid data type for total_handicap_spots: {type(total_handicap_spots)}")
        return

    cnx = connect_to_db()
    if cnx is None:
        return

    try:
        cursor = cnx.cursor()
        query = "UPDATE AVAILABLE_SPOTS SET TOTALHANDICAPSPOTS = %s WHERE id = %s"
        cursor.execute(query, (total_handicap_spots, 1))
        cnx.commit()
        print(f"Updated total handicap spots to {total_handicap_spots}")
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()


def fetch_total_spots():
    """Fetches the total parking spots from the database."""
    cnx = connect_to_db()
    if cnx is None:
        return 0

    try:
        cursor = cnx.cursor()
        query = "SELECT TOTALSPOTS FROM AVAILABLE_SPOTS"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            print(f"Fetched total spots:{result[0]}")  # Debugging print statement
            return result[0]
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()

    print("No total spots found")
    return 0

def save_total_spots(total_spots):
    """Saves the total parking spots to the database."""
    if not isinstance(total_spots, int):
        print(f"Invalid data type for total_spots: {type(total_spots)}")
        return

    cnx = connect_to_db()
    if cnx is None:
        return

    try:
        cursor = cnx.cursor()
        query = "UPDATE AVAILABLE_SPOTS SET TOTALSPOTS = %s WHERE id = %s"
        cursor.execute(query, (total_spots, 1))
        cnx.commit()
        print(f"Updated total spots to {total_spots}")
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()

def fetch_image():
    """Fetches the image path from the database."""
    cnx = connect_to_db()
    if cnx is None:
        return 0

    try:
        cursor = cnx.cursor()
        query = "SELECT IMAGE FROM AVAILABLE_SPOTS"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            print(f"Fetched image path:{result[0]}")  # Debugging print statement
            return result[0]
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()

    print("No image path found")
    return 0

def save_image(image_path):
    """Saves the image path to the database."""
    cnx = connect_to_db()
    if cnx is None:
        return

    try:
        cursor = cnx.cursor()
        query = "UPDATE AVAILABLE_SPOTS SET IMAGE = %s WHERE id = %s"
        cursor.execute(query, (image_path, 1))
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()
