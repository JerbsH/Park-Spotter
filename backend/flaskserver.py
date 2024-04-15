import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request


try:
    from database import fetch_available_spots, fetch_available_handicap_spots
except ImportError:
    print("Module 'database' not found. Please ensure it is in the same directory or installed.")

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

@app.route('/register', methods=['POST'])
def register_device():
    token = request.json.get('token')
    if token:
        # Save the token in your database
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': 'Token is missing'}), 400

@app.route('/free_spots', methods=['GET'])
def get_free_spots():
    """
    This function fetches the number of available parking spots and returns it as a JSON response.
    """
    try:
        free_spots = fetch_available_spots()
        return jsonify({'free_spots': free_spots}), 200
    except Exception as e:
        logging.exception("Error fetching free spots: %s", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/free_handicap_spots', methods=['GET'])
def get_free_handicap_spots():
    """
    This function fetches the number of available handicap parking spots and returns it as a JSON response.
    """
    try:
        free_handicap_spots = fetch_available_handicap_spots()
        return jsonify({'free_handicap_spots': free_handicap_spots}), 200
    except Exception as e:
        logging.exception("Error fetching free handicap spots: %s", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
