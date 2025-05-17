import pytest

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateVideoAPI:
  def test_create_video_with_valid_data(self):
    url = "/api/videos/"
    data = {
      "title": "Sample Video",
      "description": "Test description",
      "year_launched": 2023,
      "duration": 120,
      "rating": "L",
      "is_published": True,
      "categories": [],
      "genres": []
    }
    response = APIClient().post(url, data=data)

    assert response.status_code == HTTP_201_CREATED
    assert response.data["title"] == "Sample Video"
    assert response.data["description"] == "Test description"
    assert response.data["year_launched"] == 2023
    assert response.data["duration"] == 120
    assert response.data["rating"] == "L"
    assert response.data["is_published"] is True

  def test_create_video_with_missing_required_fields(self):
    url = "/api/videos/"
    data = {
      "description": "Test description",
      "is_published": True
    }
    response = APIClient().post(url, data=data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "title" in response.data
    assert "year_launched" in response.data
    assert "duration" in response.data
    assert "rating" in response.data

  def test_create_video_with_invalid_rating(self):
    url = "/api/videos/"
    data = {
      "title": "Sample Video",
      "description": "Test description",
      "year_launched": 2023,
      "duration": 120,
      "rating": "INVALID",
      "is_published": True,
      "categories": [],
      "genres": []
    }
    response = APIClient().post(url, data=data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "rating" in response.data
