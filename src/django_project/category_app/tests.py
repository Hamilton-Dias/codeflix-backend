from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK

class TestCategoryAPI(APITestCase):
  def test_list_categories(self):
    url = '/api/categories/'
    response = self.client.get(url)

    expedted_data = [
      {
        "id": "exemplo",
        "name": "exemplo",
        "description": "exemplo",
        "is_active": True
      },
      {
        "id": "exemplo2",
        "name": "exemplo2",
        "description": "exemplo2",
        "is_active": True
      }
    ]

    self.assertEqual(response.status_code, HTTP_200_OK)
    self.assertEqual(response.data, expedted_data)
