from uuid import UUID, uuid4
import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient

from src.django_project.jwt_auth_test_mixin import JWTAuthTestMixin

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
class TestListAPI(JWTAuthTestMixin):
  def test_list_genres_and_categories(
    self,
    category_movie: Category,
    category_documentary: Category,
    category_repository: DjangoORMCategoryRepository,
    genre_romance: Genre,
    genre_drama: Genre,
    genre_repository: DjangoORMGenreRepository,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    category_repository.save(category_movie)
    category_repository.save(category_documentary)
    genre_repository.save(genre_romance)
    genre_repository.save(genre_drama)

    url = "/api/genres/"
    response = self.client.get(url)

    assert response.status_code == HTTP_200_OK
    assert response.data["data"]
    assert response.data["data"][1]["id"] == str(genre_romance.id)
    assert response.data["data"][1]["name"] == "Romance"
    assert response.data["data"][1]["is_active"] is True
    assert set(response.data["data"][1]["categories"]) == {
        str(category_documentary.id),
        str(category_movie.id),
    }
    assert response.data["data"][0]["id"] == str(genre_drama.id)
    assert response.data["data"][0]["name"] == "Drama"
    assert response.data["data"][0]["is_active"] is True
    assert response.data["data"][0]["categories"] == []

@pytest.mark.django_db
class TestCreateAPI(JWTAuthTestMixin):
  def test_create_genre_with_associated_categories(
    self,
    category_repository: DjangoORMCategoryRepository,
    category_movie: Category,
    category_documentary: Category,
    genre_repository: DjangoORMGenreRepository,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    category_repository.save(category_movie)
    category_repository.save(category_documentary)

    url = "/api/genres/"
    data = {
      "name": "Romance",
      "categories": [str(category_movie.id), str(category_documentary.id)],
    }
    response = self.client.post(url, data=data)

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
    self.client = APIClient()
    self.authenticate_admin()

    url = "/api/genres/"
    data = {
      "name": "",
    }
    response = self.client.post(url, data=data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data == {"name": ["This field may not be blank."]}

@pytest.mark.django_db
class TestUpdateAPI(JWTAuthTestMixin):
  def test_when_request_data_is_valid_then_update_genre(
    self,
    category_repository: DjangoORMCategoryRepository,
    category_movie: Category,
    category_documentary: Category,
    genre_repository: DjangoORMGenreRepository,
    genre_romance: Genre,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    category_repository.save(category_movie)
    category_repository.save(category_documentary)
    genre_repository.save(genre_romance)

    url = f"/api/genres/{str(genre_romance.id)}/"
    data = {
      "name": "Drama",
      "is_active": True,
      "category_ids": [category_documentary.id],
    }
    response = self.client.put(url, data=data)

    assert response.status_code == HTTP_204_NO_CONTENT
    updated_genre = genre_repository.get_by_id(genre_romance.id)
    assert updated_genre.name == "Drama"
    assert updated_genre.is_active is True
    assert updated_genre.categories == {category_documentary.id}

  def test_when_request_data_is_invalid_then_return_400(
    self,
    genre_drama: Genre,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    url = f"/api/genres/{str(genre_drama.id)}/"
    data = {
      "name": "",
      "is_active": True,
      "category_ids": [],
    }
    response = self.client.put(url, data=data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data == {"name": ["This field may not be blank."]}

  def test_when_related_categories_do_not_exist_then_return_400(
    self,
    category_repository: DjangoORMCategoryRepository,
    category_movie: Category,
    category_documentary: Category,
    genre_repository: DjangoORMGenreRepository,
    genre_romance: Genre,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    category_repository.save(category_movie)
    category_repository.save(category_documentary)
    genre_repository.save(genre_romance)

    url = f"/api/genres/{str(genre_romance.id)}/"
    data = {
      "name": "Romance",
      "is_active": True,
      "category_ids": [uuid4()],  # non-existent category
    }
    response = self.client.put(url, data=data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "Categories not found: " in response.data["error"]

  def test_when_genre_does_not_exist_then_return_404(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    url = f"/api/genres/{str(uuid4())}/"
    data = {
      "name": "Romance",
      "is_active": True,
      "category_ids": [],
    }
    response = self.client.put(url, data=data)

    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestDeleteAPI(JWTAuthTestMixin):
  def test_when_genre_not_exist_then_return_404(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    url = f"/api/genres/{uuid4()}/"
    response = self.client.delete(url)

    assert response.status_code == HTTP_404_NOT_FOUND

  def test_when_genre_pk_is_invalid_then_return_400(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    url = "/api/genres/invalid_pk/"
    response = self.client.delete(url)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data == {"id": ["Must be a valid UUID."]}

  def test_when_genre_found_then_delete_genre(
    self,
    category_repository: DjangoORMCategoryRepository,
    category_movie: Category,
    category_documentary: Category,
    genre_repository: DjangoORMGenreRepository,
    genre_romance: Genre,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    category_repository.save(category_movie)
    category_repository.save(category_documentary)
    genre_repository.save(genre_romance)

    url = f"/api/genres/{str(genre_romance.id)}/"
    response = self.client.delete(url)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert genre_repository.get_by_id(genre_romance.id) is None
