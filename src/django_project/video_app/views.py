from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
  HTTP_400_BAD_REQUEST,
  HTTP_201_CREATED
)

from src.core._shared.events.message_bus import MessageBus
from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound, VideoNotFound
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMediaUseCase
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.serializers import (
  CreateVideoRequestSerializer,
  CreateVideoResponseSerializer,
)


class VideoViewSet(viewsets.ViewSet):
  def create(self, request: Request) -> Response:
    serializer = CreateVideoRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    input = CreateVideoWithoutMediaUseCase.Input(**serializer.validated_data)
    use_case = CreateVideoWithoutMediaUseCase(
      video_repository=DjangoORMVideoRepository(),
      category_repository=DjangoORMCategoryRepository(),
      genres_repository=DjangoORMGenreRepository(),
      cast_members_repository=DjangoORMCastMemberRepository(),
    )

    try:
      output = use_case.execute(input)
    except (InvalidVideo, RelatedEntitiesNotFound) as error:
      return Response(
        status=HTTP_400_BAD_REQUEST,
        data={"error": str(error)},
      )

    return Response(
      status=HTTP_201_CREATED,
      data=CreateVideoResponseSerializer(output).data,
    )
  
  def partial_update(self, request: Request, pk: UUID) -> Response:
    file = request.FILES["video_file"]
    content = file.read()
    content_type = file.content_type

    upload_video = UploadVideo(
      video_repository=DjangoORMVideoRepository(),
      storage_service=LocalStorage(),
      message_bus=MessageBus()
    )

    try:
      upload_video.execute(
        input=UploadVideo.Input(
          video_id=pk,
          file_name=file.name,
          content=content,
          content_type=content_type
        )
      )
    except VideoNotFound as err:
      return Response(
        status=HTTP_400_BAD_REQUEST,
        data={"error": str(err)},
      )
    
    return Response(status=HTTP_201_CREATED)
