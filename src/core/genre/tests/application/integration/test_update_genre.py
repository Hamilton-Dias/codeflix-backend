from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository

class TestUpdateGenre:
  def test_can_update_genre_with_valid_data(self):
    genre_repository = InMemoryGenreRepository()
    category_repository = InMemoryCategoryRepository()

    category_movie = Category(
      name="Movie",
      description="Movie category"
    )
    category_documentary = Category(
      name="Documentary",
      description="Documentary category"
    )
    category_infantil = Category(
      name="Infantil",
      description="Infantil category"
    )
    genre = Genre(
      name="Drama",
      is_active=True,
      categories={category_movie.id, category_documentary.id}
    )

    category_repository.save(category_movie)
    category_repository.save(category_documentary)
    category_repository.save(category_infantil)
    genre_repository.save(genre)

    use_case = UpdateGenre(
      repository=genre_repository,
      category_repository=category_repository
    )
    input = UpdateGenre.Input(
      id=genre.id,
      name="Romance",
      is_active=False,
      category_ids={category_movie.id, category_documentary.id, category_infantil.id}
    )

    use_case.execute(input)
    updated_genre = genre_repository.get_by_id(genre.id)

    assert updated_genre.name == "Romance"
    assert updated_genre.is_active is False
    assert updated_genre.categories == {category_movie.id, category_documentary.id, category_infantil.id}

