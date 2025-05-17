from unittest.mock import create_autospec
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre, ListOutputMeta


class TestListGenre:
  def test_when_no_genres_in_repository_then_return_empty_list(self):
    mock = create_autospec(GenreRepository)
    mock.list.return_value = []

    use_case = ListGenre(repository=mock)

    output = use_case.execute(input=ListGenre.Input())
    assert output == ListGenre.Output(
      data=[],
      meta=ListOutputMeta(
        current_page=1,
        per_page=2,
        total_items=0
      )
    )

  def test_when_genres_in_repository_then_return_list(self):
    genres = [
      Genre(
        name='Genre 1',
        categories=set()
      ),
      Genre(
        name='Genre 2',
        categories=set(),
        is_active=False
      )
    ]

    mock = create_autospec(GenreRepository)
    mock.list.return_value = genres

    use_case = ListGenre(repository=mock)

    response = use_case.execute(input=ListGenre.Input())

    assert response == ListGenre.Output(
      data=[
        GenreOutput(
          id=genres[0].id,
          name=genres[0].name,
          is_active=genres[0].is_active,
          categories=set()
        ),
        GenreOutput(
          id=genres[1].id,
          name=genres[1].name,
          is_active=genres[1].is_active,
          categories=set()
        )
      ],
      meta=ListOutputMeta(
        current_page=1,
        per_page=2,
        total_items=2
      )
    )

