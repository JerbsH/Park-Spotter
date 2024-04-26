import logging
import subprocess
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

try:
    from database import fetch_available_free_spots, fetch_available_handicap_spots, save_token
except ImportError:
    print("Module 'database' not found. Please ensure it is in the same directory or installed.")

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """
    Renders the index.html template.
    """
    return render_template('index.html')

@app.route('/run-opencv')
def run_opencv():
    """
    Executes the opencv.py script.
    """
    try:
        # Execute the opencv.py script
        subprocess.run(['python', 'opencv.py'], check=True)
        return 'Success', 200
    except Exception as e:
        return str(e), 500

logging.basicConfig(level=logging.INFO)
@app.route('/register', methods=['POST'])
def register_device():
    """
    This function registers a device for push notifications.
    It expects a JSON payload with a 'token' key.
    """
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'Token is missing'}), 400
        save_token(token)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        logging.exception("Error registering device: %s", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/free_spots', methods=['GET'])
def get_free_spots():
    """
    This function fetches the number of available parking spots and returns it as a JSON response.
    """
    try:
        free_spots = fetch_available_free_spots()
        if not isinstance(free_spots, int) or free_spots < 0:
            raise ValueError("Invalid number of free spots")
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
        if not isinstance(free_handicap_spots, int) or free_handicap_spots < 0:
            raise ValueError("Invalid number of free handicap spots")
        return jsonify({'free_handicap_spots': free_handicap_spots}), 200
    except Exception as e:
        logging.exception("Error fetching free handicap spots: %s", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
