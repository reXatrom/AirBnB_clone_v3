#!/usr/bin/python3
"""route for handling State objects and operations"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage

from models.city import City


@app_views.route("/states/<state_id>/cities")
def all_cities(state_id):
    '''retrieves all City objects from a specific state
    :return: json of all cities in a state or 404 on error'''

    # Check that the state_id actually exists
    if not storage.get("State", state_id):
        abort(404)

    city_list = []
    cities = storage.get("State", state_id).cities
    for city in cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<city_id>")
def city(city_id):
    '''gets a specific City object by ID
    :param city_id: city object id
    :return: city obj with the specified id or error'''

    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    '''deletes City by id
    :param city_id: city object id
    :return: empty dict with 200 or 404 if not found'''

    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    '''create city route
    param: state_id - state id
    :return: newly created city obj'''


    # Check that the state with that id exists
    if not storage.get("State", state_id):
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    city = City()
    city.name = request.get_json().get('name')
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    '''Updates the city with the id passed'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, val in request.get_json().items():
        if key == "id" or key == "created_at" or key == "updated_at" \
           or key == "state_id":
            continue
        else:
            setattr(city, key, val)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
