#!/usr/bin/python3
"""
This module contains the CRUD for the State API endpoints
"""

from flask import Flask, jsonify, request
from models import storage, State

@app.route('/states', methods=['GET', 'POST'])
def all_states():
    if request.method == 'GET':
        return jsonify([state.to_dict() for state in storage.all(State).values()])
    else:
        # Create a new State object
        new_state = State(**request.get_json())
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201  # Created

@app.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def state_by_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404  # Not Found

    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'PUT':
        # Update State object (ignore id, created_at, updated_at)
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400  # Bad Request
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.updated_at = datetime.utcnow()
        storage.save()
        return jsonify(state.to_dict())
    else:
        storage.delete(state)
        storage.save()
        return {}, 200  # No content

