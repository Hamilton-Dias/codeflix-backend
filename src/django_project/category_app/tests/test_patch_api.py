import uuid
import pytest
from rest_framework.test import APIClient
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from rest_framework import status

@pytest.fixture
def category_movie() -> Category:
  return Category(name="Movie", description="Movie description", is_active=True)

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
  return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestPatchAPI:
  def test_when_id_is_invalid_then_return_400(self):
    response = APIClient().patch('/api/categories/123123123/', data={
      "description": "test"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
      "id": ["Must be a valid UUID."]
    }

  def test_update_name_then_return_204(
    self, 
    category_movie: Category,
    category_repository: DjangoORMCategoryRepository
  ):
    category_repository.save(category_movie)

    response = APIClient().patch(f'/api/categories/{category_movie.id}/', data={
      "name": "Movie 2",
    })

    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    updated_category = category_repository.get_by_id(category_movie.id)
    assert updated_category.name == "Movie 2"
    assert updated_category.description == "Movie description"
    assert updated_category.is_active == True

  def test_update_description_then_return_204(
    self, 
    category_movie: Category,
    category_repository: DjangoORMCategoryRepository
  ):
    category_repository.save(category_movie)

    response = APIClient().patch(f'/api/categories/{category_movie.id}/', data={
      "description": "description 2",
    })

    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    updated_category = category_repository.get_by_id(category_movie.id)
    assert updated_category.name == "Movie"
    assert updated_category.description == "description 2"
    assert updated_category.is_active == True

  

  def test_update_is_active_then_return_204(
    self, 
    category_movie: Category,
    category_repository: DjangoORMCategoryRepository
  ):
    category_repository.save(category_movie)

    response = APIClient().patch(f'/api/categories/{category_movie.id}/', data={
      "is_active": False,
    })

    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    updated_category = category_repository.get_by_id(category_movie.id)
    assert updated_category.name == "Movie"
    assert updated_category.description == "Movie description"
    assert updated_category.is_active == False

  def test_when_category_not_found_then_return_404(self):
    response = APIClient().patch(f'/api/categories/{uuid.uuid4()}/', data={
      "name": "Movie 2",
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND

