from uuid import UUID
from unittest.mock import MagicMock
import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest


class TestCreateCategory:
  def test_create_category_with_valid_data(self):
    mock = MagicMock(CategoryRepository)
    use_case = CreateCategory(repository=mock)
    request = CreateCategoryRequest(
      name="Category 1",
      description="Description 1",
      is_active=True
    )

    response = use_case.execute(request)

    assert response.id is not None
    assert isinstance(response.id, UUID)
    assert mock.save.called

  def test_create_category_with_invalid_data(self):
      mock = MagicMock(CategoryRepository)
      use_case = CreateCategory(repository=mock)
      request = CreateCategoryRequest(
        name=""
      )

      with pytest.raises(InvalidCategoryData) as exc_info:        
        use_case.execute(request)

      assert exc_info.type is InvalidCategoryData
