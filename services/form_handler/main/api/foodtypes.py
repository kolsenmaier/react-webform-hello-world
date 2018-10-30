from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from main.api.models import FoodCategory, FoodType

food_types_blueprint = Blueprint('foodtypes', __name__)

# GET visible foodtype table contents
@food_types_blueprint.route('/api/food/types', methods=['GET'])
def get_food_types():
    # Default error response
    response_object = {
        'errors': ['Invalid request.']
    }
    if len(request.args.getlist('category_id')) > 1:
        response_object['errors'].append('Too many arguments. Only one category_id is allowed.')
    if len(request.args.getlist('category_name')) > 1:
        response_object['errors'].append('Too many arguments. Only one category_name is allowed.')
    if len(response_object['errors']) > 1:
        return jsonify(response_object), 400

    # Return all results if not filtering by category information
    catid = request.args.get('category_id')
    category_name = request.args.get('category_name')
    if catid is None and category_name is None:
        response_object = {
            'types': [type.to_json() for type in FoodType.query.filter_by(isvisible=True)]
        }
        return jsonify(response_object), 200

    # Filter results
    try:
        db_foodcategory = None
        if catid and category_name:
            db_foodcategory = FoodCategory.query.filter_by(id=catid, name=category_name).first()
        elif catid:
            db_foodcategory = FoodCategory.query.filter_by(id=catid).first()
        elif category_name:
            db_foodcategory = FoodCategory.query.filter_by(name=category_name).first()
        if not db_foodcategory:
            response_object['errors'].append('Invalid food category.')
            return jsonify(response_object), 400

        response_object = {
            'types': [type.to_json() for type in FoodType.query.filter_by(isvisible=True, catid=db_foodcategory.id)]
        }
        return jsonify(response_object), 200
    except (exc.DataError, exc.IntegrityError) as e:
        return jsonify(response_object), 400