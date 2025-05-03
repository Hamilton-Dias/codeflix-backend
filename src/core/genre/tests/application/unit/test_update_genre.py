from unittest.mock import create_autospec
import uuid
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
import pytest

class TestUpdateGenre:
  def test_when_genre_not_found_then_raises_exception(self):
    genre_repository = create_autospec(GenreRepository)
    category_repository = create_autospec(CategoryRepository)

    genre_repository.get_by_id.return_value = None

    use_case = UpdateGenre(genre_repository, category_repository)
    input = UpdateGenre.Input(
      id=uuid.uuid4(), 
      name="Not Found",
      is_active=True,
      category_ids=set()
    )

    with pytest.raises(GenreNotFound):
      use_case.execute(input)

  def test_when_update_with_invalid_data_then_raises_exception(self):
    genre_repository = create_autospec(GenreRepository)
    category_repository = create_autospec(CategoryRepository)

    genre_romance = Genre(
      name="Romance",
      categories=set(),
      is_active=True
    )

    genre_repository.get_by_id.return_value = genre_romance

    use_case = UpdateGenre(genre_repository, category_repository)
    input = UpdateGenre.Input(
      id=genre_romance.id,
      name="",
      is_active=True,
      category_ids=set()
    )

    with pytest.raises(InvalidGenre):
      use_case.execute(input)

  def test_wheen_update_with_invalid_categories_then_raise_exception(self):
    genre_repository = create_autospec(GenreRepository)
    category_repository = create_autospec(CategoryRepository)

    genre_romance = Genre(
      name="Romance",
      categories=set(),
      is_active=True
    )

    genre_repository.get_by_id.return_value = genre_romance

    use_case = UpdateGenre(genre_repository, category_repository)
    input = UpdateGenre.Input(
      id=genre_romance.id,
      name="Romance",
      is_active=True,
      category_ids={uuid.uuid4()}
    )

    with pytest.raises(RelatedCategoriesNotFound):
      use_case.execute(input)
