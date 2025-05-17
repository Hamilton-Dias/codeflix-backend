from src.core.category.application.use_cases.list_category import CategoryOutput, ListCategory, ListCategoryRequest, ListCategoryResponse, ListOutputMeta
from src.core.category.domain.category import Category

from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategory:
  def test_return_empty_list(self):
    repository = InMemoryCategoryRepository()
    use_case = ListCategory(repository=repository)
    request = ListCategoryRequest()

    response = use_case.execute(request)

    assert response == ListCategoryResponse(
      data=[], 
      meta=ListOutputMeta(
        current_page=1,
        per_page=2,
        total_items=0
      )
    )

  def test_return_existing_categories(self):
    categories = [
      Category(
        id='1',
        name='Category 1',
        description='Description 1',
        is_active=True
      ),
      Category(
        id='2',
        name='Category 2',
        description='Description 2',
        is_active=True
      )
    ]

    repository = InMemoryCategoryRepository()
    repository.save(categories[0])
    repository.save(categories[1])

    use_case = ListCategory(repository=repository)
    request = ListCategoryRequest()

    response = use_case.execute(request)

    assert response == ListCategoryResponse(
      data=[
        CategoryOutput(
          id=categories[0].id,
          name=categories[0].name,
          description=categories[0].description,
          is_active=categories[0].is_active
        ),
        CategoryOutput(
          id=categories[1].id,
          name=categories[1].name,
          description=categories[1].description,
          is_active=categories[1].is_active
        )
      ],
      meta=ListOutputMeta(
        current_page=1,
        per_page=2,
        total_items=2
      )
    )

