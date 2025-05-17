from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from uuid import UUID

from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRquest
from src.django_project.category_app.serializers import CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, DeleteCategoryRequestSerializer, ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, UpdateCategoryRequestSerializer

class CategoryViewSet(viewsets.ViewSet):
  def list(self, request: Request) -> Response:
    order_by = request.query_params.get("order_by", "name")
    current_page = int(request.query_params.get("current_page", 1))
    input = ListCategoryRequest(
      order_by=order_by,
      current_page=current_page
    )
    use_case = ListCategory(repository=DjangoORMCategoryRepository())
    output = use_case.execute(input)

    serializer = ListCategoryResponseSerializer(instance=output)
    return Response(
      status=HTTP_200_OK, 
      data=serializer.data
    )

  def retrieve(self, request: Request, pk: str = None):
    serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
    serializer.is_valid(raise_exception=True)
    
    use_case = GetCategory(repository=DjangoORMCategoryRepository())

    try:
      result = use_case.execute(request=GetCategoryRequest(id=serializer.validated_data["id"]))
    except CategoryNotFound:
      return Response(status=HTTP_404_NOT_FOUND)


    category_output = RetrieveCategoryResponseSerializer(instance=result)

    return Response(
      status=HTTP_200_OK,
      data=category_output.data
    )

  def create(self, request: Request) -> Response:
    serializer = CreateCategoryRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    input = CreateCategoryRequest(**serializer.validated_data)
    use_case = CreateCategory(repository=DjangoORMCategoryRepository())
    output = use_case.execute(input)

    return Response(
      status=HTTP_201_CREATED,
      data=CreateCategoryResponseSerializer(instance=output).data
    )

  def update(self, request: Request, pk=None) -> Response:
    serializer = UpdateCategoryRequestSerializer(
      data={
        **request.data,
        "id": pk  
      }
    )
    serializer.is_valid(raise_exception=True)

    input = UpdateCategoryRquest(**serializer.validated_data)
    use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

    try:
      use_case.execute(input)
    except CategoryNotFound:
      return Response(status=HTTP_404_NOT_FOUND)

    return Response(
      status=HTTP_204_NO_CONTENT
    )

  def destroy(self, request: Request, pk=None) -> Response:
    serializer = DeleteCategoryRequestSerializer(data={"id": pk})
    serializer.is_valid(raise_exception=True)

    use_case = DeleteCategory(repository=DjangoORMCategoryRepository())

    try:
      use_case.execute(request=DeleteCategoryRequest(**serializer.validated_data))
    except CategoryNotFound:
      return Response(status=HTTP_404_NOT_FOUND)

    return Response(
      status=HTTP_204_NO_CONTENT
    )

  def partial_update(self, request, pk: UUID = None) -> Response:
    serializer = UpdateCategoryRequestSerializer(data={
      **request.data,
      "id": pk,
    }, partial=True)
    serializer.is_valid(raise_exception=True)

    input = UpdateCategoryRquest(**serializer.validated_data)
    use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

    try:
      use_case.execute(input)
    except CategoryNotFound:
      return Response(status=HTTP_404_NOT_FOUND)

    return Response(
      status=HTTP_204_NO_CONTENT
    )    
