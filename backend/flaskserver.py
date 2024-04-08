"""
This module serves as a Flask server that exposes an endpoint to fetch the number of available parking spots.
"""

from flask import Flask, jsonify
import logging

try:
    from database import fetch_available_spots
except ImportError:
    print("Module 'database' not found. Please ensure it is in the same directory or installed.")

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/free_spots', methods=['GET'])
def get_free_spots():
    """
    This function fetches the number of available parking spots and returns it as a JSON response.
    """
    try:
        spots = fetch_available_spots()
        logging.info('Fetched available spots successfully: %s', spots)
        return jsonify(free_spots=spots)
    except Exception as e:
        logging.error('Error fetching available spots %s', e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
