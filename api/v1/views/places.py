#!/usr/bin/python3
"""
Place endpoints
"""

from flask import Flask, jsonify, request
from models import storage, City, User, Place

@app.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def all_places_by_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        # Get all Place objects associated with the City
        places = [place.to_dict() for place in city.places.values()]
        return jsonify(places)
    else:
        # Create a new Place object for the City
        new_place_data = request.get_json()
        if not new_place_data or 'user_id' not in new_place_data or 'name' not in new_place_data:
            return jsonify({'error': 'Missing user_id or name'}), 400

        user = storage.get(User, new_place_data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        new_place = Place(city_id=city_id, **new_place_data)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201  # Created

@app.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def place_by_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'PUT':
        # Update Place object (ignore id, user_id, city_id, created_at, updated_at)
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.updated_at = datetime.utcnow()
        storage.save()
        return jsonify(place.to_dict())
    else:
        storage.delete(place)
        storage.save()
        return {}, 200  # No content
