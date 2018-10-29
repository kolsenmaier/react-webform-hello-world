from flask import Blueprint, jsonify
from main.api.models import FoodCategory

food_categories_blueprint = Blueprint('foodcategories', __name__)

# GET foodcategory table contents
@food_categories_blueprint.route('/food/categories', methods=['GET'])
def get_food_categories():
    response_object = {
        'categories': [category.to_json() for category in FoodCategory.query.all()]
    }
    return jsonify(response_object), 200