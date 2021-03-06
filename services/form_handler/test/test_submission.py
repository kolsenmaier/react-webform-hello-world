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
def create_food_type(name, catid, isvisible):
    type = FoodType(name=name, catid=catid, isvisible=isvisible)
    db.session.add(type)
    db.session.commit()
    return type

# Helper function to add location entries to the DB
# Used for testing successful lookup of pre-existing locations
def create_location(name, gpid='', types=''):
    location = Location(name=name, gpid=gpid, types=types)
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
                    'category_name': category.name,
                    'food_type': type.name,
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created submission.', data['status'])
        self.assertEqual(location.id, data['submission']['location_id'])
        self.assertEqual(type.id, data['submission']['foodtype_id'])
        self.assertEqual(20, data['submission']['numducks'])
        self.assertEqual(30, data['submission']['grams'])
        self.assertIn(today, data['submission']['datetime'])

    # Ensure the /submissions route behaves correctly when DB has more data
    def test_submission_id_lookup(self):
        create_food_category('Other')
        create_food_category('Seeds')
        category = create_food_category('Bread')
        create_food_type('White', category.id, True)
        create_food_type('Sourdough', category.id, True)
        type = create_food_type('Rye', category.id, True)
        create_location('Rithet\'s Bog')
        location = create_location('Beacon Hill Park')
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'location_name': location.name,
                    'category_name': category.name,
                    'food_type': type.name,
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created submission.', data['status'])
        self.assertEqual(location.id, data['submission']['location_id'])
        self.assertEqual(type.id, data['submission']['foodtype_id'])
        self.assertEqual(20, data['submission']['numducks'])
        self.assertEqual(30, data['submission']['grams'])
        self.assertIn(today, data['submission']['datetime'])

    # Ensure the /submissions route behaves correctly when foodtype does not pre-exist
    def test_submission_new_foodtype(self):
        category = create_food_category('Bread')
        location = create_location('Beacon Hill Park')
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'location_name': location.name,
                    'category_name': category.name,
                    'food_type': 'Sourdough',
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created submission.', data['status'])
        self.assertEqual(location.id, data['submission']['location_id'])
        self.assertIsNotNone(data['submission']['foodtype_id'])
        self.assertEqual(20, data['submission']['numducks'])
        self.assertEqual(30, data['submission']['grams'])
        self.assertIn(today, data['submission']['datetime'])
        self.assertIsNotNone(FoodType.query.filter_by(catid=category.id, name='Sourdough').first())

    # Ensure the /submissions route behaves correctly when location does not pre-exist
    def test_submission_new_location(self):
        category = create_food_category('Bread')
        type = create_food_type('Rye', category.id, True)
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'location_name': 'Swan Lake',
                    'category_name': category.name,
                    'food_type': type.name,
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created submission.', data['status'])
        self.assertIsNotNone(data['submission']['location_id'])
        self.assertEqual(type.id, data['submission']['foodtype_id'])
        self.assertEqual(20, data['submission']['numducks'])
        self.assertEqual(30, data['submission']['grams'])
        self.assertIn(today, data['submission']['datetime'])
        self.assertIsNotNone(Location.query.filter_by(name='Swan Lake').first())

    # Ensure the /submissions route behaves correctly when foodtype and location do not pre-exist
    def test_submission_new_foodtype_location(self):
        category = create_food_category('Bread')
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'location_name': 'Swan Lake',
                    'category_name': category.name,
                    'food_type': 'Multigrain',
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created submission.', data['status'])
        self.assertIsNotNone(data['submission']['location_id'])
        self.assertIsNotNone(data['submission']['foodtype_id'])
        self.assertEqual(20, data['submission']['numducks'])
        self.assertEqual(30, data['submission']['grams'])
        self.assertIn(today, data['submission']['datetime'])
        self.assertIsNotNone(FoodType.query.filter_by(catid=category.id, name='Multigrain').first())
        self.assertIsNotNone(Location.query.filter_by(name='Swan Lake').first())

    # Ensure the /submissions route can look up locations by place ID
    def test_submission_location_gpid(self):
        category = create_food_category('Bread')
        type = create_food_type('Rye', category.id, True)
        location = create_location('Beacon Hill Park', 'ChIJa4uQ3-p0j1QRDtSaFQ5NHrQ', 'park,zoo')
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'google_place_id': location.gpid,
                    'category_name': category.name,
                    'food_type': type.name,
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created submission.', data['status'])
        self.assertEqual(location.id, data['submission']['location_id'])
        self.assertEqual(type.id, data['submission']['foodtype_id'])
        self.assertEqual(20, data['submission']['numducks'])
        self.assertEqual(30, data['submission']['grams'])
        self.assertIn(today, data['submission']['datetime'])

    # Ensure the /submissions route favours place ID over name
    def test_submission_location_gpid_vs_name(self):
        category = create_food_category('Bread')
        type = create_food_type('Rye', category.id, True)
        location1 = create_location('Beacon Hill Park', 'ChIJa4uQ3-p0j1QRDtSaFQ5NHrQ', 'park,zoo')
        location2 = create_location('Swan Lake Loop', 'EihTd2FuIExha2UgTG9vcCwgVmljdG9yaWEsIEJDIFY4WCwgQ2FuYWRhIi4qLAoUChIJL9eUG7tzj1QRN4CfE9AtDX4SFAoSCXFhsN2Lc49UEe1Iux508-g4', 'park')
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'location_name': location2.name,
                    'google_place_id': location1.gpid,
                    'category_name': category.name,
                    'food_type': type.name,
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created submission.', data['status'])
        self.assertEqual(location1.id, data['submission']['location_id'])
        self.assertEqual(type.id, data['submission']['foodtype_id'])
        self.assertEqual(20, data['submission']['numducks'])
        self.assertEqual(30, data['submission']['grams'])
        self.assertIn(today, data['submission']['datetime'])

    # Ensure the /submissions route fails for empty JSON
    def test_submission_invalid_json(self):
        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({}),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(data['errors']), 1)
        self.assertIn('Invalid payload.', data['errors'][0])

    # Ensure the /submissions route fails when no location provided
    def test_submission_missing_location(self):
        category = create_food_category('Bread')
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'category_name': category.name,
                    'food_type': 'Multigrain',
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(data['errors']), 1)
        self.assertIn('Invalid payload.', data['errors'][0])
        self.assertIsNone(FoodType.query.filter_by(catid=category.id, name='Multigrain').first())

    # Ensure the /submissions route fails when the provided foodcategory does not exist
    def test_submission_invalid_food_category(self):
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'location_name': 'Beacon Hill Park',
                    'category_name': 'Invalid',
                    'food_type': 'New type',
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(data['errors']), 2)
        self.assertIn('Invalid payload.', data['errors'][0])
        self.assertIn('Invalid food category.', data['errors'][1])
        self.assertIsNone(FoodCategory.query.filter_by(name='Invalid').first())
        self.assertIsNone(FoodType.query.filter_by(name='New type').first())
        self.assertIsNone(Location.query.filter_by(name='Beacon Hill Park').first())

    # Ensure the /submissions route behaves correctly for attempted SQL injections
    def test_submission_sql_injection(self):
        category = create_food_category('Bread')
        type = create_food_type('Rye', category.id, True)
        location_name = 'Beacon Hill Park; drop table location;'
        location_gpid = 'ChIJa4uQ3-p0j1QRDtSaFQ5NHrQ'
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.assertIsNone(Location.query.filter_by(gpid=location_gpid).first())
        self.assertIsNone(Location.query.filter_by(name=location_name).first())

        with self.client:
            response = self.client.post('/api/submissions',
                data=json.dumps({
                    'location_name': location_name,
                    'google_place_id': location_gpid,
                    'category_name': category.name,
                    'food_type': type.name,
                    'num_ducks': 20,
                    'grams': 30,
                    'datetime': today
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created submission.', data['status'])
        self.assertIsNotNone(data['submission']['location_id'])
        self.assertEqual(type.id, data['submission']['foodtype_id'])
        self.assertEqual(20, data['submission']['numducks'])
        self.assertEqual(30, data['submission']['grams'])
        self.assertIn(today, data['submission']['datetime'])
        self.assertIsNotNone(Location.query.filter_by(gpid=location_gpid).first())
        self.assertIsNotNone(Location.query.filter_by(name=location_name).first())

if __name__ == '__main__':
    unittest.main()