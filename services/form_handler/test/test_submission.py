import json
import unittest
from datetime import datetime
from main import db
from main.api.models import FoodCategory, FoodType, Location, Submission
from test.base import BaseTestCase

# Helper function to add food category entries to the DB
# These cannot be created by the /submissions API POST
def create_food_category(name):
    category = FoodCategory(name=name)
    db.session.add(category)
    db.session.commit()
    return category

# Helper function to add food type entries to the DB
# Used for testing successful lookup of pre-existing types
def create_food_type(type, catid, isvisible):
    type = FoodType(type=type, catid=catid, isvisible=isvisible)
    db.session.add(type)
    db.session.commit()
    return type

# Helper function to add location entries to the DB
# Used for testing successful lookup of pre-existing locations
def create_location(name):
    location = Location(name=name, gpid='', types='')
    db.session.add(location)
    db.session.commit()
    return location

# Tests for the Submission Service
class TestSubmissionService(BaseTestCase):
    # Basic happy path, ensure the /submissions route behaves correctly
    def test_submission(self):
        category = create_food_category('Bread')
        type = create_food_type('Rye', category.id, True)
        location = create_location('Beacon Hill Park')
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'location_name': location.name,
                    'category_id': category.id,
                    'food_type': type.id,
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created submission', data['status'])
        self.assertEquals(location.id, data['submission']['location_id'])
        self.assertEquals(type.id, data['submission']['foodtype_id'])
        self.assertEquals(20, data['submission']['numducks'])
        self.assertEquals(30, data['submission']['grams'])
        self.assertIn(today, data['submission']['datetime'])

if __name__ == '__main__':
    unittest.main()