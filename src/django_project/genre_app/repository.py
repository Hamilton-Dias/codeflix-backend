from django.db import transaction
from uuid import UUID
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


class DjangoORMGenreRepository(GenreRepository):
  def save(self, genre: Genre) -> None:
    with transaction.atomic():
      genre_model = GenreORM.objects.create(
        id=genre.id,
        name=genre.name,
        is_active=genre.is_active
      )
      genre_model.categories.set(genre.categories)

  def get_by_id(self, id: UUID) -> Genre | None:
    pass

  def delete(self, id: UUID) -> None:
    pass

  def list(self) -> list[Genre]:
    pass

  def update(self, genre: Genre) -> None:
    pass

