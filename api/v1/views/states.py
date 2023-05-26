#!/usr/bin/python3
""" route for handling State objects and operations."""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route("/states")
def all_states():
    '''retrieves all State objects
    :return: json of all states'''

    state_list = []
    for state in storage.all("State").values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>")
def state(state_id):
    '''Returns an instance of the specified object'''
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    '''deletes State by id
    :param state_id: state object id
    :return: empty dict with 200 or 404 if not found'''

    state = storage.get("State", state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"])
def create_state():
    '''create state route
    :return: newly created state obj'''

    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    state = State()
    state.name = request.get_json()['name']
    state.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    '''updates specific State object by ID
    :param state_id: state object ID
    :return: state object and 200 on success, or 400 or 404 on failure'''

    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, val in request.get_json().items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(state, key, val)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
