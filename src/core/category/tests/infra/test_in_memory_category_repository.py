from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSave:
  def test_can_save_category(self):
    repository = InMemoryCategoryRepository()
    category = Category(
      name="Movie"
    )

    repository.save(category)

    assert len(repository.categories) == 1
    assert repository.categories[0] == category

class TestGetById:
  def test_get_category_by_id(self):
    repository = InMemoryCategoryRepository()
    category = Category(
      name="Movie"
    )

    repository.save(category)

    assert repository.get_by_id(category.id) == category

  def test_get_category_by_id_not_found(self):
    repository = InMemoryCategoryRepository()

    assert repository.get_by_id(1) is None

class TestDelete:
  def test_delete_category(self):
    repository = InMemoryCategoryRepository()
    category = Category(
      name="Movie"
    )

    repository.save(category)
    repository.delete(category.id)

    assert len(repository.categories) == 0

class TestUpdate:
    def test_update_category(self):
        category_movies = Category(
            name="Movie",
            description="Description",
        )
        category_serie = Category(
            name="Movie 2",
            description="Description 2",
        )
        repository = InMemoryCategoryRepository(
            categories=[
                category_movies,
                category_serie,
            ]
        )

        category_movies.name = "Series"
        category_movies.description = "Description Series"
        repository.update(category_movies)

        assert len(repository.categories) == 2
        updated_category = repository.get_by_id(category_movies.id)
        assert updated_category.name == "Series"
        assert updated_category.description == "Description Series"
