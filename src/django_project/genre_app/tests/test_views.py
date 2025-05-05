from uuid import UUID, uuid4
import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.test import APIClient

@pytest.fixture
def category_movie():
  return Category(
    name="Movie",
    description="Movie description",
  )

@pytest.fixture
def category_documentary():
  return Category(
    name="Documentary",
    description="Documentary description",
  )

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()

@pytest.fixture
def genre_romance(category_movie, category_documentary) -> Genre:
  return Genre(
    name="Romance",
    is_active=True,
    categories={category_movie.id, category_documentary.id},
  )

@pytest.fixture
def genre_drama() -> Genre:
  return Genre(
    name="Drama",
    is_active=True,
    categories=set(),
  )

@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()

@pytest.mark.django_db
class TestListAPI:
  def test_list_genres_and_categories(
    self,
    category_movie: Category,
    category_documentary: Category,
    category_repository: DjangoORMCategoryRepository,
    genre_romance: Genre,
    genre_drama: Genre,
    genre_repository: DjangoORMGenreRepository,
  ) -> None:
    category_repository.save(category_movie)
    category_repository.save(category_documentary)
    genre_repository.save(genre_romance)
    genre_repository.save(genre_drama)

    url = "/api/genres/"
    response = APIClient().get(url)

    assert response.status_code == HTTP_200_OK
    assert response.data["data"]
    assert response.data["data"][0]["id"] == str(genre_romance.id)
    assert response.data["data"][0]["name"] == "Romance"
    assert response.data["data"][0]["is_active"] is True
    assert set(response.data["data"][0]["categories"]) == {
        str(category_documentary.id),
        str(category_movie.id),
    }
    assert response.data["data"][1]["id"] == str(genre_drama.id)
    assert response.data["data"][1]["name"] == "Drama"
    assert response.data["data"][1]["is_active"] is True
    assert response.data["data"][1]["categories"] == []

@pytest.mark.django_db
class TestCreateAPI:
  def test_create_genre_with_associated_categories(
    self,
    category_repository: DjangoORMCategoryRepository,
    category_movie: Category,
    category_documentary: Category,
    genre_repository: DjangoORMGenreRepository,
  ) -> None:
    category_repository.save(category_movie)

    url = "/api/genres/"
    data = {
      "name": "Romance",
      "category_ids": [str(category_movie.id), str(category_documentary.id)],
    }
    response = APIClient().post(url, data=data)

    assert response.status_code == HTTP_201_CREATED
    assert response.data["id"]

    saved_genre = genre_repository.get_by_id(response.data["id"])
    assert saved_genre == Genre(
      id=UUID(response.data["id"]),
      name="Romance",
      is_active=True,
      categories={category_movie.id, category_documentary.id},
    )

  def test_when_request_data_is_invalid_then_return_400(self) -> None:
    url = "/api/genres/"
    data = {
      "name": "",
    }
    response = APIClient().post(url, data=data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data == {"name": ["This field may not be blank."]}
