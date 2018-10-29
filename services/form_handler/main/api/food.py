from flask import Blueprint, jsonify
from main.api.models import Food

food_blueprint = Blueprint('food', __name__)

# GET visible food table contents (TODO filter on isvisible)
@food_blueprint.route('/food', methods=['GET'])
def get_food():
    response_object = {
        'food': [food.to_json() for food in Food.query.all()]
    }
    return jsonify(response_object), 200