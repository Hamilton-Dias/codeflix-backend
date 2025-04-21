from uuid import UUID
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


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
