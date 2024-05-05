"""
Flask server module
"""
import logging
import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

try:
    from database import (
        fetch_available_free_spots,
        fetch_available_handicap_spots,
        save_token,
        save_total_spots,
        save_total_handicap_spots,
        save_image,
    )
except ImportError:
    print("Module 'database' not found. Please ensure it is in the same directory or installed.")

logging.basicConfig(level=logging.INFO)
app = Flask(__name__ , template_folder='Website/')
CORS(app)

@app.route('/')
def index():
    """
    Renders the index.html template.
    """
    return render_template('index.html')


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
    except KeyError as e:
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
    except ValueError as e:
        logging.exception("Error fetching free spots: %s", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/free_handicap_spots', methods=['GET'])
def get_free_handicap_spots():
    """
    Fetches the number of available handicap parking spots and returns it as a JSON response.
    """
    try:
        free_handicap_spots = fetch_available_handicap_spots()
        if not isinstance(free_handicap_spots, int) or free_handicap_spots < 0:
            raise ValueError("Invalid number of free handicap spots")
        return jsonify({'free_handicap_spots': free_handicap_spots}), 200
    except ValueError as e:
        logging.exception("Error fetching free handicap spots: %s", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/save_spots', methods=['PUT'])
def save_spots():
    """
    Save the total spots and total handicap spots along with the image.
    """
    try:
        parking = int(request.form.get('parking'))
        acc_park = int(request.form.get('accPark'))
        image = request.files.get('image')
        if not image:
            return jsonify({'error': 'Missing image in request'}), 400

        directory = '../source'
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_path = os.path.join(directory, image.filename)
        image.save(image_path)

        # Save the image path to the database
        save_image(image_path)
        logging.info("Received data: parking=%s, acc_park=%s", parking, acc_park)

        save_total_spots(parking)
        save_total_handicap_spots(acc_park)

        return jsonify({'status': 'success'}), 200
    except (ValueError, FileNotFoundError) as e:
        logging.exception("Error saving parking spots: %s", str(e))
        return jsonify({'error': 'An error occurred while saving parking spots'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
