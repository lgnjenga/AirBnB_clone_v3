#!/usr/bin/python3
"""
City endpoints
"""

from flask import Flask, jsonify, request
from models import storage, State, City

@app.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def all_cities_by_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities.values()]
        return jsonify(cities)
    else:
        # Create a new City object
        new_city = City(state_id=state_id, **request.get_json())
        if not new_city.name:
            return jsonify({'error': 'Missing name'}), 400
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201  # Created

@app.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def city_by_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'PUT':
        # Update City object (ignore id, state_id, created_at, updated_at)
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.updated_at = datetime.utcnow()
        storage.save()
        return jsonify(city.to_dict())
    else:
        storage.delete(city)
        storage.save()
        return {}, 200  # No content
