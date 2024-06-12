#!/usr/bin/python3

"""
Create a Flask App
"""

from flask import Flask, jsonify
from models import storage  # Assuming models.py defines storage functionality
from api.v1.views import app_views  # Blueprint for v1 views

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()  # Close storage connection on teardown

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404  # Return JSON with error message

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
