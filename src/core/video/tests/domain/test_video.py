import pytest
import uuid

from uuid import UUID
from src.core.video.domain.video import Video
from src.core.video.domain.value_objets import Rating

class TestVideo:
  def test_title_is_required(self):
    with pytest.raises(TypeError):
      Video()

  def test_title_must_have_less_than_255_characters(self):
    with pytest.raises(ValueError):
      Video(
        title='a' * 256,
        description='',
        launch_year=2025,
        duration=120.0,
        published=True,
        rating=Rating.L,
        categories=set(),
        genres=set(),
        cast_members=set()
      )
    
  def test_video_must_be_created_with_id_as_uuid(self):
    video = Video(
      title='Video',
      description='',
      launch_year=2025,
      duration=120.0,
      published=True,
      rating=Rating.L,
      categories=set(),
      genres=set(),
      cast_members=set()
    )
    assert isinstance(video.id, UUID)

  def test_created_video_with_default_values(self):
    video = Video(
      title='Video',
      description='',
      launch_year=2025,
      duration=120.0,
      published=True,
      rating=Rating.L,
      categories=set(),
      genres=set(),
      cast_members=set()
    )

    assert video.title == 'Video'
    assert video.description == ''
    assert video.launch_year == 2025
    assert video.duration == 120.0
    assert video.published is True
    assert video.rating == Rating.L
    assert video.categories == set()
    assert video.genres == set()
    assert video.cast_members == set()

  def test_cannot_create_video_with_empty_title(self):
    with pytest.raises(ValueError):
      Video(title="")
  
  def test_description_must_have_less_than_1024_characters(self):
    with pytest.raises(ValueError):
      Video(
        title='Video 1',
        description='a' * 1025
      )
