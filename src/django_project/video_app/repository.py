from uuid import UUID

from django.db import transaction

from src.core.video.domain.value_objets import AudioVideoMedia
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import Video as VideoORM, AudioVideoMedia as AudioVideoMediaORM


class DjangoORMVideoRepository(VideoRepository):
  def save(self, video: Video) -> None:
    with transaction.atomic():
      video_model = VideoORM.objects.create(
        title=video.title,
        description=video.description,
        launch_year=video.launch_year,
        duration=video.duration,
        rating=video.rating,
      )
      video_model.categories.set(video.categories)
      video_model.genres.set(video.genres)
      video_model.cast_members.set(video.cast_members)

