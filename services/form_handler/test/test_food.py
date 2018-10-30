import json
import unittest
from main import db
from main.api.models import FoodCategory, FoodType
from test.base import BaseTestCase

# Helper function to add food category entries to the DB
def create_food_category(name):
    category = FoodCategory(name=name)
    db.session.add(category)
    db.session.commit()
    return category

# Helper function to add food type entries to the DB
def create_food_type(name, catid, isvisible):
    type = FoodType(name=name, catid=catid, isvisible=isvisible)
    db.session.add(type)
    db.session.commit()
    return type

# Tests for the Food Category Service
class TestFoodCategoryService(BaseTestCase):
    # Basic happy path, ensure the /food/categories route behaves correctly
    def test_food_categories(self):
        create_food_category('Bread')
        with self.client:
            response = self.client.get('/api/food/categories')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['categories']), 1)
            self.assertIn('Bread', data['categories'][0]['name'])

    # Ensure the /food/categories route behaves correctly for multiple entries
    def test_multiple_categories(self):
        create_food_category('Bread')
        create_food_category('Other')
        with self.client:
            response = self.client.get('/api/food/categories')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['categories']), 2)
            self.assertIn('Bread', data['categories'][0]['name'])
            self.assertIn('Other', data['categories'][1]['name'])

# Tests for the Food Type Service
class TestFoodTypeService(BaseTestCase):
    # Basic happy path, ensure the /food/types route behaves correctly
    def test_food_types(self):
        category = create_food_category('Other')
        create_food_type('Table scraps', category.id, True)
        with self.client:
            response = self.client.get('/api/food/types')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 1)
            self.assertIn('Table scraps', data['types'][0]['name'])
            self.assertEqual(category.id, data['types'][0]['category_id'])

    # Ensure the /food/types route behaves correctly for multiple entries
    def test_multiple_types(self):
        category = create_food_category('Other')
        create_food_type('Table scraps', category.id, True)
        create_food_type('Raisins', category.id, True)
        with self.client:
            response = self.client.get('/api/food/types')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 2)
            self.assertIn('Table scraps', data['types'][0]['name'])
            self.assertEqual(category.id, data['types'][0]['category_id'])
            self.assertIn('Raisins', data['types'][1]['name'])
            self.assertEqual(category.id, data['types'][1]['category_id'])

    # Ensure the /food/types route does not return entries with isvisible=false
    def test_invisible_types(self):
        category = create_food_category('Other')
        create_food_type('Table scraps', category.id, False)
        create_food_type('Raisins', category.id, True)
        with self.client:
            response = self.client.get('/api/food/types')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 1)
            self.assertIn('Raisins', data['types'][0]['name'])
            self.assertEqual(category.id, data['types'][0]['category_id'])

    # Basic happy path, ensure the /food/types route returns entries filtered by category id
    def test_types_filtered_all(self):
        category = create_food_category('Other')
        create_food_type('Table scraps', category.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(category_id=category.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 1)
            self.assertIn('Table scraps', data['types'][0]['name'])
            self.assertEqual(category.id, data['types'][0]['category_id'])

    # Ensure the /food/types route returns entries filtered by category id
    def test_types_filtered_catid(self):
        category1 = create_food_category('Bread')
        category2 = create_food_category('Other')
        create_food_type('Multigrain', category1.id, True)
        create_food_type('Table scraps', category2.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(category_id=category2.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 1)
            self.assertIn('Table scraps', data['types'][0]['name'])
            self.assertEqual(category2.id, data['types'][0]['category_id'])

    # Ensure the /food/types route returns entries filtered by category name
    def test_types_filtered_catname(self):
        category1 = create_food_category('Bread')
        category2 = create_food_category('Other')
        create_food_type('Multigrain', category1.id, True)
        create_food_type('Table scraps', category2.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(category_name=category2.name))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 1)
            self.assertIn('Table scraps', data['types'][0]['name'])
            self.assertEqual(category2.id, data['types'][0]['category_id'])

    # Ensure the /food/types route returns entries filtered by category id and name
    def test_types_filtered_catid_catname(self):
        category1 = create_food_category('Bread')
        category2 = create_food_category('Other')
        create_food_type('Multigrain', category1.id, True)
        create_food_type('Table scraps', category2.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(category_id=category2.id, category_name=category2.name))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 1)
            self.assertIn('Table scraps', data['types'][0]['name'])
            self.assertEqual(category2.id, data['types'][0]['category_id'])

    # Ensure the /food/types route returns an empty list for entries filtered by category id for no results
    def test_types_filtered_no_results(self):
        category1 = create_food_category('Bread')
        category2 = create_food_category('Other')
        create_food_type('Table scraps', category2.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(category_id=category1.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 0)

    # Ensure the /food/types route fails for entries filtered by an invalid category id
    def test_types_filtered_invalid_catid(self):
        category = create_food_category('Other')
        create_food_type('Table scraps', category.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(category_id='invalid'))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(data['errors']), 1)
            self.assertIn('Invalid request.', data['errors'][0])

    # Ensure the /food/types route fails for entries filtered by a category id that doesn't exist
    def test_types_filtered_catid_not_found(self):
        category = create_food_category('Other')
        create_food_type('Table scraps', category.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(category_id=100))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(data['errors']), 2)
            self.assertIn('Invalid request.', data['errors'][0])
            self.assertIn('Invalid food category.', data['errors'][1])

    # Ensure the /food/types route fails for entries filtered by a category name that doesn't exist
    def test_types_filtered_catname_not_found(self):
        category = create_food_category('Other')
        create_food_type('Table scraps', category.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(category_name='invalid'))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(data['errors']), 2)
            self.assertIn('Invalid request.', data['errors'][0])
            self.assertIn('Invalid food category.', data['errors'][1])

    # Ensure the /food/types route fails for entries filtered by a category id and name that don't match
    def test_types_filtered_catid_catname_mismatch(self):
        category1 = create_food_category('Bread')
        category2 = create_food_category('Other')
        create_food_type('Table scraps', category2.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(category_id=category1.id, category_name=category2.name))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(data['errors']), 2)
            self.assertIn('Invalid request.', data['errors'][0])
            self.assertIn('Invalid food category.', data['errors'][1])

    # Ensure the /food/types route ignores unsupported args
    def test_types_unsupported_args(self):
        category1 = create_food_category('Bread')
        category2 = create_food_category('Other')
        create_food_type('Multigrain', category1.id, True)
        create_food_type('Table scraps', category2.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string=dict(unsupported=category2.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 2)
            self.assertIn('Multigrain', data['types'][0]['name'])
            self.assertEqual(category1.id, data['types'][0]['category_id'])
            self.assertIn('Table scraps', data['types'][1]['name'])
            self.assertEqual(category2.id, data['types'][1]['category_id'])

    # Ensure the /food/types route returns an error for repeated category_id
    def test_types_repeated_catid_error(self):
        category1 = create_food_category('Bread')
        category2 = create_food_category('Other')
        create_food_type('Multigrain', category1.id, True)
        create_food_type('Table scraps', category2.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string='category_id={0}&category_id={1}'.format(category1.id, category2.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(data['errors']), 2)
            self.assertIn('Invalid request.', data['errors'][0])
            self.assertIn('Too many arguments. Only one category_id is allowed.', data['errors'][1])

    # Ensure the /food/types route returns an error for repeated category_name
    def test_types_repeated_catname_error(self):
        category1 = create_food_category('Bread')
        category2 = create_food_category('Other')
        create_food_type('Multigrain', category1.id, True)
        create_food_type('Table scraps', category2.id, True)
        with self.client:
            response = self.client.get('/api/food/types', query_string='category_name={0}&category_name={1}'.format(category1.name, category2.name))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(data['errors']), 2)
            self.assertIn('Invalid request.', data['errors'][0])
            self.assertIn('Too many arguments. Only one category_name is allowed.', data['errors'][1])

if __name__ == '__main__':
    unittest.main()