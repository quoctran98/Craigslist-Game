import random
from flask import Blueprint, jsonify, request
from server.helper import settings, listings, CL_CATEGORY_NAMES

api = Blueprint("api", __name__)

@api.route("/api/random_listing", methods=["GET"])
def get_random_listing():
    if "category" in request.args:
        category = request.args["category"]
    else:
        category = random.choice(list(listings.keys()))

    if "n" in request.args:
        n = int(request.args["n"])
    else:
        n = 1

    this_category = listings[category]
    this_listing = random.sample(this_category, k=n)
    return(jsonify(this_listing))

@api.route("/api/categories", methods=["GET"])
def get_categories():
    return(jsonify(CL_CATEGORY_NAMES))