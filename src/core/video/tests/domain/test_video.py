import pytest
import uuid

from uuid import UUID
from src.core.video.domain.events.event import AudioVideoMediaUpdated
from src.core.video.domain.video import Video
from src.core.video.domain.value_objets import AudioVideoMedia, MediaStatus, MediaType, Rating

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
        opened=True,
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
      opened=True,
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
      opened=True,
      rating=Rating.L,
      categories=set(),
      genres=set(),
      cast_members=set()
    )

    assert video.title == 'Video'
    assert video.description == ''
    assert video.launch_year == 2025
    assert video.duration == 120.0
    assert video.opened is True
    assert video.rating == Rating.L
    assert video.categories == set()
    assert video.genres == set()
    assert video.cast_members == set()

  def test_cannot_create_video_with_empty_title(self):
    with pytest.raises(ValueError):
      video = Video(
        title='',
        description='',
        launch_year=2025,
        duration=120.0,
        opened=True,
        rating=Rating.L,
        categories=set(),
        genres=set(),
        cast_members=set()
      )

class TestUpdateVideoMedia:
  def test_update_video_and_dispatch_event(self) -> None:
    video = Video(
      title='Video',
      description='',
      launch_year=2025,
      duration=120.0,
      opened=True,
      rating=Rating.L,
      categories=set(),
      genres=set(),
      cast_members=set()
    )

    media = AudioVideoMedia(
      name="video.mp4",
      raw_location="raw/video.mp4",
      encoded_location="encoded/video.mp4",
      status=MediaStatus.COMPLETED,
      media_type=MediaType.VIDEO,
    )

    video.update_video(media)

    assert video.video == media

    assert video.events == [
      AudioVideoMediaUpdated(
        aggregate_id=video.id,
        file_path="raw/video.mp4",
        media_type=MediaType.VIDEO,
      )
    ]
