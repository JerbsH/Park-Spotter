import logging
from flask import Flask, jsonify

try:
    from database import fetch_available_spots  # Adjust the import statement
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
        free_spots = fetch_available_spots()
        return jsonify({'free_spots': free_spots}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
