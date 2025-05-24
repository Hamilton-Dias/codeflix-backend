import uuid
import pytest
from rest_framework.test import APIClient
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from rest_framework import status

from src.django_project.jwt_auth_test_mixin import JWTAuthTestMixin

@pytest.fixture
def category_movie() -> Category:
  return Category(name="Movie", description="Movie description")

@pytest.fixture
def category_documentary() -> Category:
  return Category(name="Documentary", description="Documentary description")

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
  return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestRetrieveAPI(JWTAuthTestMixin):
  def test_when_id_is_invalid_return_400(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    response = self.client.get("/api/categories/123/")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

  def test_return_category_when_exists(
    self, 
    category_movie: Category,
    category_documentary: Category,
    category_repository: DjangoORMCategoryRepository
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    category_repository.save(category_movie)
    category_repository.save(category_documentary)

    response = self.client.get(f"/api/categories/{category_documentary.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
      "data": {
        "id": str(category_documentary.id),
        "name": category_documentary.name,
        "description": category_documentary.description,
        "is_active": category_documentary.is_active
      }
    }

  def test_return_404_when_not_found(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    response = self.client.get(f"/api/categories/{uuid.uuid4()}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
