from uuid import UUID
from unittest.mock import MagicMock, create_autospec
import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse

from src.core.category.domain.category import Category
import uuid


class TestGetCategory:
  def test_return_found_category(self):
    category = Category(
       name="Movie",
       description="Description",
       is_active=True
    )

    mock = create_autospec(CategoryRepository)
    mock.get_by_id.return_value = category

    use_case = GetCategory(repository=mock)
    request = GetCategoryRequest(
      id=category.id
    )

    response = use_case.execute(request)

    assert response == GetCategoryResponse(
      id=category.id,
      name=category.name,
      description=category.description,
      is_active=category.is_active
    )
