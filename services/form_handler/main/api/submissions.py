from flask import Blueprint, jsonify, request
from main import db
from main.api.models import FoodType, Location, Submission

submissions_blueprint = Blueprint('submissions', __name__)

# POST submission, creating new location and foodtype entries as necessary
@submissions_blueprint.route('/api/submissions', methods=['POST'])
def create_submission():
    # Get request data
    post_data = request.get_json()
    location_name = post_data.get('location_name')
    category_id = post_data.get('category_id') #TODO decide if this is final or if we'll accept by name
    food_type = post_data.get('food_type')
    num_ducks = post_data.get('num_ducks')
    grams = post_data.get('grams')
    datetime = post_data.get('datetime')

    # Add to DB, with lookups # TODO add lookups and replace temp ids in submission
    db.session.add(FoodType(type=food_type, catid=category_id, isvisible=True))
    db.session.add(Location(name=location_name, gpid='', types=''))
    db.session.commit()
    submission = Submission(lid=1, fid=1, numducks=num_ducks, grams=grams, datetime=datetime)
    db.session.add(submission)
    db.session.commit()

    # Return success and created object
    response_object = {
        'status': 'Successfully created submission',
        'submission': submission.to_json()
    }
    return jsonify(response_object), 201