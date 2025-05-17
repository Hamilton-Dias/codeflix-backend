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
      "launch_year": 2023,
      "duration": 120,
      "rating": "L",
      "opened": False,
      "categories": [],
      "genres": [],
      "cast_members": []
    }
    response = APIClient().post(url, data=data)

    assert response.status_code == HTTP_201_CREATED

  def test_create_video_with_missing_required_fields(self):
    url = "/api/videos/"
    data = {
      "description": "Test description"
    }
    response = APIClient().post(url, data=data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "title" in response.data
    assert "launch_year" in response.data
    assert "duration" in response.data
    assert "rating" in response.data
