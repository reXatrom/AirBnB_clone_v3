#!/usr/bin/python3
"""route for handling User objects and operations"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route("/users")
def all_users():
    '''retrieves all User objects
    :return: json of all users'''

    user_list = []
    for user in storage.all("User").values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>")
def user(user_id):
    '''gets a specific User object by ID
    :param user_id: user object id
    :return: user obj with the specified id or error'''

    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    '''deletes User by id
    :param user_id: user object id
    :return: empty dict with 200 or 404 if not found'''

    user = storage.get("User", user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"])
def create_user():
    '''create user route
    :return: newly created user obj'''

    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('email'):
        abort(400, description="Missing email")

    if not request.get_json().get('password'):
        abort(400, description="Missing password")

    user = User()
    user.email = request.get_json()['email']
    user.password = request.get_json()['password']
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    '''updates specific User object by ID
    :param user_id: user object ID
    :return: user object and 200 on success, or 400 or 404 on failure'''

    user = storage.get("User", user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, val in request.get_json().items():
        if key == "id" or key == "created_at" or key == "updated_at" or key == "email":
            continue
        else:
            setattr(user, key, val)

    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
