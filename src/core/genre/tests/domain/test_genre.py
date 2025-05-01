import pytest
import uuid

from uuid import UUID
from src.core.genre.domain.genre import Genre

class TestGenre:
  def test_name_is_required(self):
    with pytest.raises(TypeError):
      Genre()

  def test_name_must_have_less_than_255_characters(self):
    with pytest.raises(ValueError):
      Genre(name='a' * 256)

  def test_cannot_create_genre_with_empty_name(self):
      with pytest.raises(ValueError):
          Genre(name="")

  def test_create_genre_with_default_values(self):
    genre = Genre(name='Romance')
    assert genre.name == 'Romance'
    assert genre.is_active is True
    assert genre.id is not None
    assert genre.categories == set()
    
  def test_genre_must_be_created_with_id_as_uuid(self):
    genre = Genre(name='Romance')
    assert isinstance(genre.id, UUID)

  def test_genre_is_created_as_active_by_default(self):
    genre = Genre(name='Romance')
    assert genre.is_active is True

  def test_genre_is_created_with_provided_values(self):
    genre_id = uuid.uuid4()
    categories = {uuid.uuid4(), uuid.uuid4()}

    genre = Genre(
      id=genre_id,
      name='Romance',
      is_active=False,
      categories=categories
    )
    assert genre.id == genre_id
    assert genre.name == 'Romance'
    assert genre.is_active is False
    assert genre.categories == categories

  def test_genre_str_prints_correctly(self):
    genre_id = uuid.uuid4()
    genre_name = 'Romance'
    genre_is_active = False
    genre = Genre(
      id=genre_id,
      name=genre_name,
      is_active=genre_is_active
    )
    assert str(genre) == f"{genre_name} - ({genre_is_active})"

  def test_genre_repr_prints_correctly(self):
    genre_id = uuid.uuid4()
    genre_name = 'Romance'
    genre_is_active = False
    genre = Genre(
      id=genre_id,
      name=genre_name,
      is_active=genre_is_active
    )
    assert repr(genre) == f"<Genre {genre_name} ({genre_id})>"

class TestActivateGenre:
  def test_activate_inactive_genre(self):
    genre = Genre(name='Romance', is_active=False)
    genre.activate()
    assert genre.is_active is True

  def test_activate_active_genre(self):
    genre = Genre(name='Romance', is_active=True)
    genre.activate()
    assert genre.is_active is True

class TestDeactivateGenre:
  def test_deactivate_genre(self):
    genre = Genre(name='Romance', is_active=True)
    genre.deactivate()
    assert genre.is_active is False

class TestEquality:
  def test_when_genres_have_same_id_they_are_equal(self):
    common_id = uuid.uuid4()
    genre_1 = Genre(name="Romance", id=common_id)
    genre_2 = Genre(name="Acao", id=common_id)

    assert genre_1 == genre_2

  def test_equality_different_classes(self):
    class Dummy:
      pass

    common_id = uuid.uuid4()
    genre = Genre(name="Romance", id=common_id)
    dummy = Dummy()
    dummy.id = common_id

    assert genre != dummy

class TestChangedName:
  def test_changed_name(self):
    genre = Genre(name="Romance")
    genre.update_genre(name="Acao")
    assert genre.name == "Acao"

  def test_changed_name_to_same_name(self):
    genre = Genre(name="Romance")
    genre.update_genre(name="Romance")
    assert genre.name == "Romance"

  def test_changed_name_to_invalid_name(self):
    genre = Genre(name="Romance")
    with pytest.raises(ValueError):
      genre.update_genre("")

  def test_changed_name_to_invalid_name_with_more_than_255_characters(self):
    genre = Genre(name="Romance")
    with pytest.raises(ValueError):
      genre.update_genre("a" * 256)

class TestAddCategory:
  def test_add_category_from_genre(self):
    genre = Genre(name="Romance")
    category_id = uuid.uuid4()
    
    assert category_id not in genre.categories
    genre.add_category(category_id)
    assert category_id in genre.categories

  def test_can_add_multiple_categories(self):
    genre = Genre(name="Romance")
    category_id_1 = uuid.uuid4()
    category_id_2 = uuid.uuid4()

    genre.add_category(category_id_1)
    genre.add_category(category_id_2)

    assert category_id_1 in genre.categories
    assert category_id_2 in genre.categories

class TestRemoveCategory:
  def test_remove_category_from_genre(self):
    category_id = uuid.uuid4()
    genre = Genre(name="Romance", categories={category_id})
    assert category_id in genre.categories
    genre.remove_category(category_id)
    assert category_id not in genre.categories
