"""The code connects to a MySQL database
and fetches all the rows from a table."""

import os
import mysql.connector
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

def connect_to_db():
    try:
        cnx = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        logging.info('Connected to the database successfully')
        return cnx
    except Exception as e:
        logging.error('Error connecting to the database %s', e)



def fetch_available_spots():
    cnx = connect_to_db()
    try:
        cursor = cnx.cursor()
        query = "SELECT PARKSPOTS FROM AVAILABLE_SPOTS"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            print(f"Fetched {result[0]} available spots")  # Debugging print statement
            return result[0]
        else:
            print("No available spots found")
            return 0
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()

def store_free_spots(free_spots):
    cnx = connect_to_db()
    try:
        cursor = cnx.cursor()
        query = "UPDATE AVAILABLE_SPOTS SET PARKSPOTS = %s WHERE id = %s"
        cursor.execute(query, (free_spots, 1))  # Provide the id parameter
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        cnx.close()
