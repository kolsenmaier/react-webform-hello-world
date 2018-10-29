import json
import unittest
from main import db
from main.api.models import Food
from test.base import BaseTestCase

class TestFoodService(BaseTestCase):
    """Tests for the Food Service."""

    def test_food(self):
        """Ensure the /food route behaves correctly."""
        food = Food(category='Bread', type='Rye', amount='10g')
        db.session.add(food)
        db.session.commit()
        with self.client:
            response = self.client.get('/food')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['food']), 1)
            self.assertIn('Bread', data['food'][0]['category'])
            self.assertIn('Rye', data['food'][0]['type'])
            self.assertIn('10g', data['food'][0]['amount'])

if __name__ == '__main__':
    unittest.main()