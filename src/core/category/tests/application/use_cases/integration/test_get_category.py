from uuid import UUID
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
import uuid
import pytest


class TestGetCategory:
  def test_get_category_by_id(self):
    category_movie = Category(
      name="Movie",
      description="Movie description",
      is_active=True
    )
    category_series = Category(
      name="Series",
      description="Serie description",
      is_active=True
    )

    repository = InMemoryCategoryRepository(
      categories=[category_movie, category_series]
    )

    use_case = GetCategory(repository=repository)
    request = GetCategoryRequest(
      id=category_movie.id
    )

    response = use_case.execute(request)

    assert response == GetCategoryResponse(
      id=category_movie.id,
      name=category_movie.name,
      description=category_movie.description,
      is_active=category_movie.is_active
    )

  def test_when_category_does_not_exist_then_raise_exception(self):
    category_movie = Category(
      name="Movie",
      description="Movie description",
      is_active=True
    )
    category_series = Category(
      name="Series",
      description="Serie description",
      is_active=True
    )

    repository = InMemoryCategoryRepository(
      categories=[category_movie, category_series]
    )

    use_case = GetCategory(repository=repository)
    not_found_id = uuid.uuid4()
    request = GetCategoryRequest(
      id=not_found_id
    )

    with pytest.raises(CategoryNotFound) as exc:
      use_case.execute(request)

