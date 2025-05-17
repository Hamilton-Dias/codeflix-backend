from pathlib import Path
from unittest.mock import create_autospec
from src.core._shared.storage.abstract_storage_service import AbstractStorageService
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core.video.domain.value_objets import AudioVideoMedia, MediaStatus, Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


class TestUploadVideo:
  def test_upload_video_media_to_video(self):
    video = Video(
      title="My video",
      description="Description",
      launch_year=2024,
      duration=100,
      published=False,
      rating=Rating.L,
      categories=set(),
      genres=set(),
      cast_members=set()
    )

    video_repository = InMemoryVideoRepository(videos=[video])
    mock_storage = create_autospec(AbstractStorageService)

    use_case = UploadVideo(
      video_repository=video_repository,
      storage_service=mock_storage
    )

    use_case.execute(
      input=UploadVideo.Input(
        video_id=video.id,
        file_name="video.mp4",
        content=b"video content",
        content_type="video/mp4"
      )
    )

    mock_storage.store.assert_called_once_with(
      file_path=str(Path("videos") / str(video.id) / "video.mp4"),
      content=b"video content",
      content_type="video/mp4"
    )

    video_from_repository = video_repository.get_by_id(video.id)
    video_from_repository.video == AudioVideoMedia(
      name="video.mp4",
      raw_location=str(Path("videos") / str(video.id) / "video.mp4"),
      encoded_location="",
      status=MediaStatus.PENDING
    )
