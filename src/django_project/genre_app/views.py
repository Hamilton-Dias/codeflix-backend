from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from src.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import CreateGenreInputSerializer, CreateGenreOutputSerializer, ListGenreOutputSerializer

class GenreViewSet(viewsets.ViewSet):
  def list(self, request: Request) -> Response:
    use_case = ListGenre(repository=DjangoORMGenreRepository())
    output: ListGenre.Output = use_case.execute(input=ListGenre.Input)
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
