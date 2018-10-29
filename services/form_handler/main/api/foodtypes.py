from flask import Blueprint, jsonify
from main.api.models import FoodType

food_types_blueprint = Blueprint('foodtypes', __name__)

# GET visible foodtype table contents (TODO filter on isvisible)
@food_types_blueprint.route('/food/types', methods=['GET'])
def get_food_types():
    response_object = {
        'types': [type.to_json() for type in FoodType.query.all()]
    }
    return jsonify(response_object), 200