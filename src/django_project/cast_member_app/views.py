from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)
from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest
from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember, ListCastMemberRequest
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember, UpdateCastMemberRquest
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer,
    CreateCastMemberResponseSerializer,
    DeleteCastMemberRequestSerializer,
    ListCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer,
)
from src.django_project.permissions import IsAdmin, IsAuthenticated


class CastMemberViewSet(viewsets.ViewSet):
  permission_classes = [IsAdmin, IsAuthenticated]
  
  def list(self, request: Request) -> Response:
    order_by = request.query_params.get("order_by", "name")
    current_page = int(request.query_params.get("current_page", 1))
    use_case = ListCastMember(repository=DjangoORMCastMemberRepository())
    input = ListCastMemberRequest(
      order_by=order_by,
      current_page=current_page
    )
    output = use_case.execute(input)
    serializer = ListCastMemberResponseSerializer(instance=output)

    return Response(status=HTTP_200_OK, data=serializer.data)

  def create(self, request: Request) -> Response:
    serializer = CreateCastMemberRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    input = CreateCastMemberRequest(**serializer.validated_data)
    use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())

    try:
      output = use_case.execute(input)
    except InvalidCastMember as error:
      return Response(
        status=HTTP_400_BAD_REQUEST,
        data={"error": str(error)},
      )

    return Response(
      status=HTTP_201_CREATED,
      data=CreateCastMemberResponseSerializer(output).data,
    )

  def update(self, request: Request, pk: UUID = None) -> Response:
    serializer = UpdateCastMemberRequestSerializer(data={
      **request.data,
      "id": pk,
    })
    serializer.is_valid(raise_exception=True)

    input = UpdateCastMemberRquest(**serializer.validated_data)
    use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())
    try:
      use_case.execute(input)
    except CastMemberNotFound:
      return Response(status=HTTP_404_NOT_FOUND)
    except InvalidCastMember as error:
      return Response(
        status=HTTP_400_BAD_REQUEST,
        data={"error": str(error)},
      )

    return Response(status=HTTP_204_NO_CONTENT)

  def destroy(self, request: Request, pk: UUID = None) -> Response:
    request_data = DeleteCastMemberRequestSerializer(data={"id": pk})
    request_data.is_valid(raise_exception=True)

    input = DeleteCastMemberRequest(**request_data.validated_data)
    use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())
    try:
      use_case.execute(input)
    except CastMemberNotFound:
      return Response(
        status=HTTP_404_NOT_FOUND,
        data={"error": f"CastMember with id {pk} not found"},
      )

    return Response(status=HTTP_204_NO_CONTENT)
