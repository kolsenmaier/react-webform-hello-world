from flask import Blueprint, jsonify
from main.api.models import FoodType

food_types_blueprint = Blueprint('foodtypes', __name__)

# GET visible foodtype table contents
@food_types_blueprint.route('/api/food/types', methods=['GET'])
def get_food_types():
    response_object = {
        'types': [type.to_json() for type in FoodType.query.filter_by(isvisible=True)]
    }
    return jsonify(response_object), 200