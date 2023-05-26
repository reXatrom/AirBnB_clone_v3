#!/usr/bin/python3
"""route for handling Place objects and operations"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places")
def all_places(city_id):
    '''Returns a list of all the places'''

    # Check if city exists
    if not storage.get("City", city_id):
        abort(404)

    places_list = []
    for place in storage.all("Place").values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>")
def place(place_id):
    '''gets a specific Place object by ID
    :param place_id: place object id
    :return: place obj with the specified id or error'''

    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'])
def delete_place(place_id):
    '''deletes Place by id
    :param place_id: Place object id
    :return: empty dict with 200 or 404 if not found'''

    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    '''create place route
    :return: newly created Place obj'''

    # Check if city exists
    if not storage.get("City", city_id):
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    user_id = request.get_json().get('user_id')
    if not user_id:
        abort(400, description="Missing user_id")

    if not storage.get("User", user_id):
        abort(404)

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    place = Place()
    place.name = request.get_json()['name']
    place.city_id = city_id
    place.user_id = user_id
    place.save()
#    storage.new(place)
#    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'])
def update_place(place_id):
    '''updates specific Place object by ID
    :param place_id: Place object ID
    :return: Place object and 200 on success, or 400 or 404 on failure'''

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, val in request.get_json().items():
        if key == "id" or key == "created_at" or key == "updated_at" \
           or key == "user_id" or key == "city_id":
            continue
        else:
            setattr(place, key, val)

    storage.save()

    return make_response(jsonify(place.to_dict()), 200)
