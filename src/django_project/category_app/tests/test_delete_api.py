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
class TestDeleteAPI(JWTAuthTestMixin):
  def test_when_id_is_invalid_should_return_404(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    response = self.client.delete('/api/categories/12341234132/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

  def test_when_category_does_not_exists_should_return_404(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()
    response = self.client.delete(f'/api/categories/{uuid.uuid4()}/')
    assert response.status_code == status.HTTP_404_NOT_FOUND

  def test_when_category_is_deleted_should_return_204(self, category_repository: DjangoORMCategoryRepository) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    category = Category(name='Movie')
    category_repository.save(category)

    response = self.client.delete(f'/api/categories/{category.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert category_repository.get_by_id(category.id) is None
