from uuid import UUID
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import CreateGenreInputSerializer, CreateGenreOutputSerializer, DeleteGenreInputSerializer, ListGenreOutputSerializer, UpdateGenreRequestSerializer
from src.django_project.permissions import IsAdmin, IsAuthenticated

class GenreViewSet(viewsets.ViewSet):
  permission_classes = [IsAdmin, IsAuthenticated]
  
  def list(self, request: Request) -> Response:
    order_by = request.query_params.get("order_by", "name")
    current_page = int(request.query_params.get("current_page", 1))
    use_case = ListGenre(repository=DjangoORMGenreRepository())
    output: ListGenre.Output = use_case.execute(input=ListGenre.Input(
      order_by=order_by,
      current_page=current_page
    ))
    reponse_serializer = ListGenreOutputSerializer(output)
    
    return Response(
      status=HTTP_200_OK, 
      data=reponse_serializer.data
    )

  def create(self, request: Request) -> Response:
    serializer = CreateGenreInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    input = CreateGenre.Input(**serializer.validated_data)
    use_case = CreateGenre(
      repository=DjangoORMGenreRepository(),
      category_repository=DjangoORMCategoryRepository(),
    )
    try:
      output = use_case.execute(input)
    except (InvalidGenre, RelatedCategoriesNotFound) as error:
      return Response(
        status=HTTP_400_BAD_REQUEST,
        data={"error": str(error)},
      )

    return Response(
      status=HTTP_201_CREATED,
      data=CreateGenreOutputSerializer(output).data,
    )
  
  def update(self, request: Request, pk=None) -> Response:
    serializer = UpdateGenreRequestSerializer(
      data={
        **request.data,
        "id": pk
      }
    )
    serializer.is_valid(raise_exception=True)

    input = UpdateGenre.Input(**serializer.validated_data)
    use_case = UpdateGenre(
      repository=DjangoORMGenreRepository(),
      category_repository=DjangoORMCategoryRepository(),
    )

    try:
      use_case.execute(input)
    except (InvalidGenre, RelatedCategoriesNotFound) as error:
      return Response(
        status=HTTP_400_BAD_REQUEST,
        data={"error": str(error)},
      )
    except GenreNotFound:
      return Response(
        status=HTTP_404_NOT_FOUND,
        data={"error": f"Genre with id {pk} not found"},
      )
    
    return Response(
      status=HTTP_204_NO_CONTENT
    )


  def destroy(self, request: Request, pk: UUID = None):
    request_data = DeleteGenreInputSerializer(data={"id": pk})
    request_data.is_valid(raise_exception=True)
    input = DeleteGenre.Input(**request_data.validated_data)

    use_case = DeleteGenre(repository=DjangoORMGenreRepository())
    try:
      use_case.execute(input)
    except GenreNotFound:
      return Response(
        status=HTTP_404_NOT_FOUND,
        data={"error": f"Genre with id {pk} not found"},
      )

    return Response(status=HTTP_204_NO_CONTENT)
