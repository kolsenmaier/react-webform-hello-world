import json
import unittest
from main import db
from main.api.models import FoodCategory
from main.api.models import FoodType
from test.base import BaseTestCase

# Helper function to add food category entries to the DB
def create_food_category(name):
    category = FoodCategory(name=name)
    db.session.add(category)
    db.session.commit()
    return category

# Helper function to add food type entries to the DB
def create_food_type(type, category):
    # TODO lookup catid
    type = FoodType(type=type, catid=category)
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
        # TODO
        create_food_type('Rye', 1)
        with self.client:
            response = self.client.get('/api/food/types')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['types']), 1)
            self.assertIn('Rye', data['types'][0]['type'])
            self.assertEquals(1, data['types'][0]['catid'])

if __name__ == '__main__':
    unittest.main()