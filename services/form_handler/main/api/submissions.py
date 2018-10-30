from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from main import db
from main.api.models import FoodType, Location, Submission

submissions_blueprint = Blueprint('submissions', __name__)

# POST submission, creating new location and foodtype entries as necessary
@submissions_blueprint.route('/api/submissions', methods=['POST'])
def create_submission():
    # Default error response
    response_object = {
        'errors': ['Invalid payload.']
    }

    # Get request data
    # TODO test with malicious input and see if there's existing sanitization.
    # TODO could also use string replacement "%s", (var) or other available methods to sanitize
    post_data = request.get_json()
    location_name = post_data.get('location_name')
    category_id = post_data.get('category_id') #TODO decide if this is final or if we'll accept by name also
    food_type = post_data.get('food_type')
    num_ducks = post_data.get('num_ducks')
    grams = post_data.get('grams')
    datetime = post_data.get('datetime')

    # Look for existing foodtype and location
    db_foodtype = None
    db_location = None
    try:
        db_foodtype = FoodType.query.filter_by(catid=category_id, type=food_type).first()
        if not db_foodtype:
            db_foodtype = FoodType(type=food_type, catid=category_id, isvisible=False)
            db.session.add(db_foodtype)
            db.session.commit()
        db_location = Location.query.filter_by(name=location_name).first()
        if not db_location:
            db_location = Location(name=location_name, gpid='', types='') # TODO
            db.session.add(db_location)
            db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400

    # Add to DB
    submission = Submission(lid=db_location.id, fid=db_foodtype.id, numducks=num_ducks, grams=grams, datetime=datetime)
    db.session.add(submission)
    db.session.commit()

    # Return success and created object
    response_object = {
        'status': 'Successfully created submission.',
        'submission': submission.to_json()
    }
    return jsonify(response_object), 201