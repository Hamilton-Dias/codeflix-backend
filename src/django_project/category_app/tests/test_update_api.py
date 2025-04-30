import uuid
import pytest
from rest_framework.test import APIClient
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from rest_framework import status

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
  return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestUpdateAPI:
  def test_when_payload_is_invalid_then_return_400(self, category_repository: DjangoORMCategoryRepository):
    response = APIClient().put('/api/categories/123123123/', data={
      "name": "", 
      "description": "test"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
      "name": ["This field may not be blank."],
      "id": ["Must be a valid UUID."],
      "is_active": ["This field is required."]
    }

  def test_when_payload_is_valid_then_return_200(self, category_repository: DjangoORMCategoryRepository):
    category = Category(name="Movie")
    category_repository.save(category)

    response = APIClient().put(f'/api/categories/{category.id}/', data={
      "name": "Movie 2",
      "description": "description",
      "is_active": False
    })

    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    updated_category = category_repository.get_by_id(category.id)
    assert updated_category.name == "Movie 2"
    assert updated_category.description == "description"
    assert updated_category.is_active == False

  def test_when_category_not_found_then_return_404(self):
    response = APIClient().put(f'/api/categories/{uuid.uuid4()}/', data={
      "name": "Movie 2",
      "description": "description",
      "is_active": False
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND

