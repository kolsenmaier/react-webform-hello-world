from flask import Blueprint, jsonify

food_blueprint = Blueprint('food', __name__)

# GET visible food table contents (TODO return from DB)
@food_blueprint.route('/food', methods=['GET'])
def get_food():
    return jsonify({
        'status': 'success',
        'message': 'bread'
    })