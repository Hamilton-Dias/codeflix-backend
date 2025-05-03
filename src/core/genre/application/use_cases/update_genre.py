import copy
from dataclasses import dataclass
from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound

class UpdateGenre:
  def __init__(self, repository: GenreRepository, category_repository: CategoryRepository):
    self.repository = repository
    self.category_repository = category_repository

  @dataclass
  class Input:
    id: UUID
    name: str | None = None
    is_active: bool | None = None
    category_ids: set[UUID] | None = None

  def execute(self, input: Input) -> None:
    genre = self.repository.get_by_id(input.id)

    if genre is None:
      raise GenreNotFound(f"Genre with id {input.id} not found")
    
    category_ids = {category.id for category in self.category_repository.list()}
    if not input.category_ids.issubset(category_ids):
      raise RelatedCategoriesNotFound(f"Categories not found: {input.category_ids - category_ids}")

    try:
      current_name = genre.name
      current_categories = copy.copy(genre.categories)

      if input.name is not None:
        current_name = input.name

      genre.update_genre(
        name=current_name
      )

      if current_categories is not None:
        for category_id in current_categories:
          genre.remove_category(category_id)

      if input.category_ids is not None:
        for category_id in input.category_ids:
          genre.add_category(category_id)

      if input.is_active is True:
        genre.activate()

      if input.is_active is False:
        genre.deactivate()

      genre.update_genre(
        name=current_name
      )
    except ValueError as err:
      raise InvalidGenre(err)

    self.repository.update(genre)
