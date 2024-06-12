#!/usr/bin/python3
"""
Amenity endpoints
"""

from flask import Flask, jsonify, request
from models import storage, Amenity

@app.route('/amenities', methods=['GET', 'POST'])
def all_amenities():
    if request.method == 'GET':
        return jsonify([amenity.to_dict() for amenity in storage.all(Amenity).values()])
    else:
        # Create a new Amenity object
        new_amenity = Amenity(**request.get_json())
        if not new_amenity.name:
            return jsonify({'error': 'Missing name'}), 400
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201  # Created

@app.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenity_by_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'PUT':
        # Update Amenity object (ignore id, created_at, updated_at)
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.updated_at = datetime.utcnow()
        storage.save()
        return jsonify(amenity.to_dict())
    else:
        storage.delete(amenity)
        storage.save()
        return {}, 200  # No content
