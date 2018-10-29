import json
import unittest
from test.base import BaseTestCase

class TestUserService(BaseTestCase):
    """Tests for the Food Service."""

    def test_food(self):
        """Ensure the /food route behaves correctly."""
        response = self.client.get('/food')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('bread', data['message'])
        self.assertIn('success', data['status'])

if __name__ == '__main__':
    unittest.main()