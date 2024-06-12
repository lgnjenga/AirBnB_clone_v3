#!/usr/bin/python3
"""
User endpoints
"""

from flask import Flask, jsonify, request
from models import storage, User
from werkzeug.security import generate_password_hash

@app.route('/users', methods=['GET', 'POST'])
def all_users():
    if request.method == 'GET':
        return jsonify([user.to_dict() for user in storage.all(User).values()])
    else:
        # Create a new User object
        user_data = request.get_json()
        if not user_data or 'email' not in user_data or 'password' not in user_data:
            return jsonify({'error': 'Missing email or password'}), 400
        user_data['password'] = generate_password_hash(user_data['password'])
        new_user = User(**user_data)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201  # Created

@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        # Update User object (ignore id, email, created_at, updated_at)
        user_data = request.get_json()
        if user_data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in user_data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        storage.save()
        return jsonify(user.to_dict())
    else:
        storage.delete(user)
        storage.save()
        return {}, 200  # No content
