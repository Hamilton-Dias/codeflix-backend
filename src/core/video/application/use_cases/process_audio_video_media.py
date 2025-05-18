from dataclasses import dataclass
from uuid import UUID

from src.core.video.application.exceptions import MediaNotFound, VideoNotFound
from src.core.video.domain.value_objets import MediaStatus, MediaType
from src.core.video.domain.video_repository import VideoRepository


class ProcessAudioVideoMedia:

  @dataclass
  class Input:
    encoded_location: str
    video_id: UUID
    status: MediaStatus
    media_type: MediaType

  def __init__(self, video_repository: VideoRepository) -> None:
    self.video_repository = video_repository

  def execute(self, request: Input):
    video = self.video_repository.get_by_id(id=request.video_id)
    if video is None:
      raise VideoNotFound('Video not found')
    
    if request.media_type == MediaType.VIDEO:
      if not video.video:
        raise MediaNotFound('Video must have media to be processed')
      
      video.process(
        status=request.status,
        encoded_location=request.encoded_location,
      )

    self.video_repository.update(video)


