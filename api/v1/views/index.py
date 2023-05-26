#!/usr/bin/python3
""" index api v1 view """

from api.v1.views import app_views
from flask import jsonify

# api route for status


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ return status """
    return jsonify({"status": "OK"}), 200
