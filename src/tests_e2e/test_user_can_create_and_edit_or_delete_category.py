import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateAndEditOrDeleteCategory:
  def test_user_can_create_and_edit_category(self) -> None:
    api_client = APIClient()

    # Verifica que lista esta vazia
    list_response = api_client.get('/api/categories/')
    assert list_response.data == {
      "data": [],
      "meta": {
        "current_page": 1,
        "per_page": 2,
        "total_items": 0
      }
    }

    # Criar uma categoria
    create_response = api_client.post(
      '/api/categories/', 
      data={
        "name": "Category 1",
        "description": "Category 1 description"
      }
    )
    assert create_response.status_code == 201
    created_category_id = create_response.data['id']

    # Verifica que categoria criada aparece na listagem
    list_response = api_client.get('/api/categories/')
    assert list_response.data == {
      "data": [
        {
          "id": created_category_id,
          "name": "Category 1",
          "description": "Category 1 description",
          "is_active": True
        }
      ],
      "meta": {
        "current_page": 1,
        "per_page": 2,
        "total_items": 1
      }
    }

    # Edita categoria criada
    update_request = api_client.put(
      f'/api/categories/{created_category_id}/',
      data={
        "name": "Category 1 updated",
        "description": "Category 1 description updated",
        "is_active": False
      }
    )
    assert update_request.status_code == 204

    # Verifica que categoria editada aparece na listagem
    list_response = api_client.get('/api/categories/')
    assert list_response.data == {
      "data": [
        {
          "id": created_category_id,
          "name": "Category 1 updated",
          "description": "Category 1 description updated",
          "is_active": False
        }
      ],
      "meta": {
        "current_page": 1,
        "per_page": 2,
        "total_items": 1
      }
    }

  def test_user_can_create_and_delete_category(self) -> None:
    api_client = APIClient()

    # Verifica que lista esta vazia
    list_response = api_client.get('/api/categories/')
    assert list_response.data == {
      "data": [],
      "meta": {
        "current_page": 1,
        "per_page": 2,
        "total_items": 0
      }
    }

    # Criar uma categoria
    create_response = api_client.post(
      '/api/categories/', 
      data={
        "name": "Category 1",
        "description": "Category 1 description"
      }
    )
    assert create_response.status_code == 201
    created_category_id = create_response.data['id']

    # Verifica que categoria criada aparece na listagem
    list_response = api_client.get('/api/categories/')
    assert list_response.data == {
      "data": [
        {
          "id": created_category_id,
          "name": "Category 1",
          "description": "Category 1 description",
          "is_active": True
        }
      ],
      "meta": {
        "current_page": 1,
        "per_page": 2,
        "total_items": 1
      }
    }

    # deleta categoria criada
    update_request = api_client.delete(f'/api/categories/{created_category_id}/')
    assert update_request.status_code == 204

    # Verifica que categoria editada aparece na listagem
    list_response = api_client.get('/api/categories/')
    assert list_response.data == {
      "data": [],
      "meta": {
        "current_page": 1,
        "per_page": 2,
        "total_items": 0
      }
    }
