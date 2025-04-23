from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK

class CategoryViewSet(viewsets.ViewSet):
  def list(self, request: Request) -> Response:
    return Response(status=HTTP_200_OK, data=[
      {
        "id": "exemplo",
        "name": "exemplo",
        "description": "exemplo",
        "is_active": True
      },
      {
        "id": "exemplo2",
        "name": "exemplo2",
        "description": "exemplo2",
        "is_active": True
      }
    ])

