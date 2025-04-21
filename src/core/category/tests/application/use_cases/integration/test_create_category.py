from uuid import UUID
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
  def test_create_category_with_valid_data(self):
    repository = InMemoryCategoryRepository()
    use_case = CreateCategory(repository=repository)
    request = CreateCategoryRequest(
      name="Category 1",
      description="Description 1",
      is_active=True
    )

    response = use_case.execute(request)

    assert response.id is not None
    assert isinstance(response.id, UUID)
    assert repository.categories[0].id == response.id
    assert len(repository.categories) == 1
