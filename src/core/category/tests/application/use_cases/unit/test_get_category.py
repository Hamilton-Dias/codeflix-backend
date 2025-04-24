from uuid import UUID
from unittest.mock import MagicMock, create_autospec
import pytest

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse

from src.core.category.domain.category import Category

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

  def test_when_category_not_found_then_raise_exception(self):
    mock = create_autospec(CategoryRepository)
    mock.get_by_id.return_value = None

    use_case = GetCategory(repository=mock)
    request = GetCategoryRequest(
      id=UUID('8c3c8c8c-8c3c-8c3c-8c3c-8c3c8c8c8c8c')
    )

    with pytest.raises(CategoryNotFound):
      use_case.execute(request)
