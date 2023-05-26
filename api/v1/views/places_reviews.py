#!/usr/bin/python3
"""route for handling Review objects and operations"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews")
def all_reviews(place_id):
    '''retrieves all Review objects by place
    :return: json of all reviews'''

    # Check if place exists
    if not storage.get("Place", place_id):
        abort(404)

    review_list = []
    for review in storage.all("Review").values():
        if review.place_id == place_id:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>")
def review(review_id):
    '''Returns an instance of the specified object'''
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_review(review_id):
    '''deletes Review by id
    :param : Review object id
    :return: empty dict with 200 or 404 if not found'''

    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    '''create review route
    :return: newly created Review obj'''

    if not storage.get("Place", place_id):
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    user_id = request.get_json().get('user_id')
    if not user_id:
        abort(400, description="Missing user_id")

    if not storage.get("User", user_id):
        abort(404)

    if not request.get_json().get('text'):
        abort(400, description="Missing text")

    review = Review()
    review.text = request.get_json()['text']
    review.place_id = place_id
    review.user_id = user_id
    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def update_review(review_id):
    '''updates specific Review object by ID
    :param review_id: Review object ID
    :return: Review object and 200 on success, or 400 or 404 on failure'''

    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, val in request.get_json().items():
        if key == "id" or key == "created_at" or key == "updated_at" \
           or key == "user_id" or key == "place_id":
            continue
        else:
            setattr(review, key, val)

    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
