import uuid
import pytest
from rest_framework.test import APIClient
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from rest_framework import status

from src.django_project.jwt_auth_test_mixin import JWTAuthTestMixin

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
  return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestCreateAPI(JWTAuthTestMixin):
  def test_when_payload_is_invalid_then_return_400(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()
    response = self.client.post("/api/categories/", data={
      "name": "",
      "description": "Movie description"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST

  def test_when_payload_is_valid_then_return_201(self, category_repository: DjangoORMCategoryRepository) -> None:
    self.client = APIClient()
    self.authenticate_admin()
    response = self.client.post("/api/categories/", data={
      "name": "Movie",
      "description": "Movie description"
    })

    created_category_id = uuid.UUID(response.data["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert category_repository.get_by_id(created_category_id) == Category(
      id=created_category_id,
      name="Movie",
      description="Movie description"
    )
