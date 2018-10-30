from flask import Blueprint, jsonify, request
from main.api.models import FoodType

food_types_blueprint = Blueprint('foodtypes', __name__)

# GET visible foodtype table contents
@food_types_blueprint.route('/api/food/types', methods=['GET'])
def get_food_types():
    if len(request.args.getlist('category_id')) > 1:
        response_object = {
            'errors': ['Too many arguments. Only one category_id is allowed.']
        }
        return jsonify(response_object), 400

    catid = request.args.get('category_id')
    if catid:
        response_object = {
            'types': [type.to_json() for type in FoodType.query.filter_by(isvisible=True, catid=catid)]
        }
        return jsonify(response_object), 200

    response_object = {
        'types': [type.to_json() for type in FoodType.query.filter_by(isvisible=True)]
    }
    return jsonify(response_object), 200