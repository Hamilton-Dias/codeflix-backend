from unittest.mock import create_autospec
import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
import uuid

from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository

@pytest.fixture
def movie_category() -> Category:
  return Category(name="Movie", description="Movie description", is_active=True)

@pytest.fixture
def documentary_category() -> Category:
  return Category(name="Documentary", description="Documentary description", is_active=True)

@pytest.fixture
def category_repository(movie_category, documentary_category) -> CategoryRepository:
  return InMemoryCategoryRepository([movie_category, documentary_category])

@pytest.fixture
def empty_category_repository() -> CategoryRepository:
  return InMemoryCategoryRepository()

class TestCreateGenre:
  def test_create_genre_with_associated_categories(
    self,
    movie_category: Category,
    documentary_category: Category,
    category_repository: CategoryRepository
  ):
    genre_repository = InMemoryGenreRepository()
    use_case = CreateGenre(
      repository=genre_repository,
      category_repository=category_repository
    )

    input = CreateGenre.Input(
      name="Action",
      category_ids={movie_category.id, documentary_category.id}
    )

    output = use_case.execute(input)

    assert isinstance(output.id, uuid.UUID)
    saved_gente = genre_repository.get_by_id(output.id)
    assert saved_gente.name == "Action"
    assert saved_gente.is_active is True
    assert saved_gente.categories == {movie_category.id, documentary_category.id}

  def test_create_genre_with_inexistent_categories_raise_an_error(
    self,
    empty_category_repository: CategoryRepository
  ):
    genre_repository = InMemoryGenreRepository()
    use_case = CreateGenre(
      repository=genre_repository,
      category_repository=empty_category_repository
    )

    input = CreateGenre.Input(
      name="Action",
      category_ids={uuid.uuid4(), uuid.uuid4()}
    )

    with pytest.raises(RelatedCategoriesNotFound):
      use_case.execute(input)

  def test_create_genre_without_categories(
    self,
    category_repository: CategoryRepository
  ):
    genre_repository = InMemoryGenreRepository()
    use_case = CreateGenre(
      repository=genre_repository,
      category_repository=category_repository
    )

    input = CreateGenre.Input(
      name="Action",
      category_ids=set()
    )

    output = use_case.execute(input)

    assert isinstance(output.id, uuid.UUID)
    saved_gente = genre_repository.get_by_id(output.id)
    assert saved_gente.name == "Action"
    assert saved_gente.is_active is True
    assert saved_gente.categories == set()
