import json
import unittest
from main import db
from main.api.models import Food
from test.base import BaseTestCase

# Helper function to add food entries to the DB
def create_food(category, type, amount):
    food = Food(category=category, type=type, amount=amount)
    db.session.add(food)
    db.session.commit()
    return food

# Tests for the Food Service
class TestFoodService(BaseTestCase):
    # Basic happy path, ensure the /food route behaves correctly
    def test_food(self):
        create_food('Bread', 'Rye', '10g')
        with self.client:
            response = self.client.get('/food')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['food']), 1)
            self.assertIn('Bread', data['food'][0]['category'])
            self.assertIn('Rye', data['food'][0]['type'])
            self.assertIn('10g', data['food'][0]['amount'])

    # Ensure the /food route behaves correctly for multiple entries
    def test_multiple_food(self):
        create_food('Bread', 'Rye', '10g')
        create_food('Bread', 'Sourdough', '20g')
        with self.client:
            response = self.client.get('/food')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['food']), 2)
            self.assertIn('Bread', data['food'][0]['category'])
            self.assertIn('Rye', data['food'][0]['type'])
            self.assertIn('10g', data['food'][0]['amount'])
            self.assertIn('Bread', data['food'][1]['category'])
            self.assertIn('Sourdough', data['food'][1]['type'])
            self.assertIn('20g', data['food'][1]['amount'])

if __name__ == '__main__':
    unittest.main()