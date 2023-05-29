#!/usr/bin/python3
"""this file gets the places"""
from flask import jsonify, abort, request
from datetime import datetime
import uuid

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


def get_object_by_id(model_cls, object_id):
    """Helper function to retrieve an object by its ID"""
    obj = storage.get(model_cls, object_id)
    if not obj:
        abort(404)
    return obj


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    """Retrieves a list of all Place objects in a city"""
    city = get_object_by_id(City, city_id)
    list_places = [place.to_dict() for place in city.places]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = get_object_by_id(Place, place_id)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = get_object_by_id(Place, place_id)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    city = get_object_by_id(City, city_id)
    user = get_object_by_id(User, data['user_id'])
    new_place = Place(name=data['name'], user_id=data['user_id'], city_id=city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    """Updates a Place object"""
    place = get_object_by_id(Place, place_id)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key == 'name' or key == 'description' or key == 'number_rooms' \
                or key == 'number_bathrooms' or key == 'max_guest' \
                or key == 'price_by_night' or key == 'latitude' or key == 'longitude':
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
