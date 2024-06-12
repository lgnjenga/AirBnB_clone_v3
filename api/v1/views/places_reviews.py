#!/usr/bin/python3
"""
Review endpoints
"""

from flask import Flask, jsonify, request
from models import storage, Place, User, Review

@app.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def all_reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        # Get all Review objects associated with the Place
        reviews = [review.to_dict() for review in place.reviews.values()]
        return jsonify(reviews)
    else:
        # Create a new Review object for the Place
        new_review_data = request.get_json()
        if not new_review_data or 'user_id' not in new_review_data or 'text' not in new_review_data:
            return jsonify({'error': 'Missing user_id or text'}), 400

        user = storage.get(User, new_review_data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        new_review = Review(place_id=place_id, **new_review_data)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201  # Created

@app.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review_by_id(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'PUT':
        # Update Review object (ignore id, user_id, place_id, created_at, updated_at)
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(review, key, value)
        review.updated_at = datetime.utcnow()
        storage.save()
        return jsonify(review.to_dict())
    else:
        storage.delete(review)
        storage.save()
        return {}, 200  # No content
