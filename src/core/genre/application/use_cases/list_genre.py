from dataclasses import dataclass, field
from uuid import UUID
from src.core.genre.domain.genre_repository import GenreRepository
from src.core._shared.domain.pagination import ListOutputMeta
from src.core._shared.domain import pagination

@dataclass
class GenreOutput:
  id: UUID
  name: str
  is_active: bool
  categories: set[UUID]

class ListGenre:
  def __init__(self, repository: GenreRepository):
    self.repository = repository

  @dataclass
  class Input:
    order_by: str = "name"
    current_page: int = 1

  @dataclass
  class Output:
    data: list[GenreOutput]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)

  def execute(self, input: Input):
    genres = self.repository.list()

    mapped_genres = sorted([
      GenreOutput(
        id=genre.id,
        name=genre.name,
        is_active=genre.is_active,
        categories=genre.categories
      ) for genre in genres
    ], key=lambda genre: getattr(genre, input.order_by))

    page_offset = (input.current_page - 1) * pagination.DEFAULT_PAGE_SIZE
    genres_page = mapped_genres[page_offset:page_offset + pagination.DEFAULT_PAGE_SIZE]

    return self.Output(
      data=genres_page,
      meta=ListOutputMeta(
        current_page=input.current_page,
        per_page=pagination.DEFAULT_PAGE_SIZE,
        total_items=len(genres_page)
      )
    )
