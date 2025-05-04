
import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreORM

@pytest.mark.django_db
class TestSave:
  def test_saves_genre_in_database(self):
    genre = Genre(name="Action")
    genre_repository = DjangoORMGenreRepository()

    assert GenreORM.objects.count() == 0
    genre_repository.save(genre)

    assert GenreORM.objects.count() == 1
    genre_model = GenreORM.objects.first()
    assert genre_model.id == genre.id
    assert genre_model.name == genre.name
    assert genre_model.is_active == genre.is_active

  def test_saves_genre_with_categories(self):
    genre_repository = DjangoORMGenreRepository()
    category_repository = DjangoORMCategoryRepository()

    category = Category(name="Action")
    category_repository.save(category)

    genre = Genre(name="Romance")
    genre.add_category(category.id)

    assert GenreORM.objects.count() == 0
    genre_repository.save(genre)
    assert GenreORM.objects.count() == 1
    
    saved_genre_model = GenreORM.objects.get(id=genre.id)
    assert saved_genre_model.id == genre.id
    assert saved_genre_model.name == genre.name
    assert saved_genre_model.is_active == genre.is_active
    
    related_categories = saved_genre_model.categories.get()
    assert related_categories.id == category.id
