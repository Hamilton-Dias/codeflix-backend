from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository

class TestCategoryAPI(APITestCase):
  def test_list_categories(self):
    category_movie = Category(
      name='Movie',
      description='Movie description'
    )
    category_series = Category(
      name='Series',
      description='Series description'
    )

    repository = DjangoORMCategoryRepository()
    repository.save(category_movie)
    repository.save(category_series)

    url = '/api/categories/'
    response = self.client.get(url)

    expected_data = [
      {
        "id": str(category_movie.id),
        "name": category_movie.name,
        "description": category_movie.description,
        "is_active": category_movie.is_active
      },
      {
        "id": str(category_series.id),
        "name": category_series.name,
        "description": category_series.description,
        "is_active": category_series.is_active
      }
    ]

    self.assertEqual(response.status_code, HTTP_200_OK)
    self.assertEqual(response.data, expected_data)
