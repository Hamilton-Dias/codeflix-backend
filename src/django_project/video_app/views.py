from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
  HTTP_200_OK,
  HTTP_404_NOT_FOUND,
  HTTP_201_CREATED,
)

from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMediaUseCase
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
    use_case = CreateVideoWithoutMediaUseCase(repository=DjangoORMVideoRepository())
    output = use_case.execute(input)

    return Response(
      status=HTTP_201_CREATED,
      data=CreateVideoResponseSerializer(output).data,
    )

