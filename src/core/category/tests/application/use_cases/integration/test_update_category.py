from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRquest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
  def test_can_update_category_name_and_description(self):
    category = Category(
      name="Movie",
      description="Movie description",
    )

    repository = InMemoryCategoryRepository()
    repository.save(category)

    use_case = UpdateCategory(repository=repository)
    request = UpdateCategoryRquest(
      id=category.id,
      name="Movie updated",
      description="Movie description updated",
    )

    use_case.execute(request)

    updated_category = repository.get_by_id(category.id)
    assert updated_category.name == "Movie updated"
    assert updated_category.description == "Movie description updated"
