#!/usr/bin/python3

"""
api/v1/views/index.py
"""

from api.v1.views import app_views
from models import storage  # Assuming models.py defines classes and count()

@app_views.route('/status')
def status():
    return jsonify({'status': 'OK'})  # Return JSON with status message

@app_views.route('/stats')
def stats():
    class_counts = {cls.__name__: storage.count(cls) for cls in storage.all().values()}
    return jsonify(class_counts)  # Return JSON with object counts by type

