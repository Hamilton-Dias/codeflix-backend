import pytest
from uuid import UUID, uuid4
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.jwt_auth_test_mixin import JWTAuthTestMixin
from rest_framework.test import APITestCase

@pytest.fixture
def actor():
  return CastMember(
    name="Actor",
    type=CastMemberType.ACTOR,
  )

@pytest.fixture
def director():
  return CastMember(
    name="Director",
    type=CastMemberType.DIRECTOR,
  )

@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
  return DjangoORMCastMemberRepository()

@pytest.mark.django_db
class TestListAPI(JWTAuthTestMixin):
  def test_list_cast_members(
    self,
    actor: CastMember,
    director: CastMember,
    cast_member_repository: DjangoORMCastMemberRepository,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    cast_member_repository.save(actor)
    cast_member_repository.save(director)

    url = "/api/cast_members/"
    response = self.client.get(url)

    expected_data = {
      "data": [
        {
          "id": str(actor.id),
          "name": "Actor",
          "type": CastMemberType.ACTOR,
        },
        {
          "id": str(director.id),
          "name": "Director",
          "type": CastMemberType.DIRECTOR,
        }
      ],
      "meta": {
        "current_page": 1,
        "per_page": 2,
        "total_items": 2
      }
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
class TestCreateAPI(JWTAuthTestMixin):
  def test_when_request_data_is_valid_then_create_cast_member(
    self,
    cast_member_repository: DjangoORMCastMemberRepository,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    url = "/api/cast_members/"
    data = {
      "name": "Actor",
      "type": "ACTOR"
    }
    response = self.client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"]

    saved_cast_member = cast_member_repository.get_by_id(response.data["id"])
    assert saved_cast_member == CastMember(
      id=UUID(response.data["id"]),
      name="Actor",
      type=CastMemberType.ACTOR,
    )

  def test_when_request_data_is_invalid_then_return_400(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    url = "/api/cast_members/"
    data = {
      "name": "",
      "type": "",
    }
    response = self.client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
      "name": ["This field may not be blank."],
      "type": ['"" is not a valid choice.'],
    }


@pytest.mark.django_db
class TestUpdateAPI(JWTAuthTestMixin):
  def test_when_request_data_is_valid_then_update_cast_member(
    self,
    actor: CastMember,
    cast_member_repository: DjangoORMCastMemberRepository,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    cast_member_repository.save(actor)

    url = f"/api/cast_members/{actor.id}/"
    data = {
      "name": "Another Actor",
      "type": CastMemberType.DIRECTOR,
    }
    response = self.client.put(url, data=data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.data
    updated_cast_member = cast_member_repository.get_by_id(actor.id)
    assert updated_cast_member.name == "Another Actor"
    assert updated_cast_member.type == CastMemberType.DIRECTOR

  def test_when_request_data_is_invalid_then_return_400(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    url = f"/api/cast_members/123412341234123/"
    data = {
      "name": "",
    }
    response = self.client.put(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
      "id": ["Must be a valid UUID."],
      "name": ["This field may not be blank."],
      "type": ["This field is required."],
    }

  def test_when_cast_member_with_id_does_not_exist_then_return_404(
    self,
  ) -> None:
    self.client = APIClient()
    self.authenticate_admin()

    url = f"/api/cast_members/{uuid4()}/"
    data = {
      "name": "Not Actor",
      "type": CastMemberType.DIRECTOR,
    }
    response = self.client.put(url, data=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI(JWTAuthTestMixin):
  def test_when_cast_member_found_then_delete_cast_member(
    self,
    actor: CastMember,
    cast_member_repository: DjangoORMCastMemberRepository,
  ) -> None:
    
    self.client = APIClient()
    self.authenticate_admin()

    cast_member_repository.save(actor)
    
    url = f"/api/cast_members/{actor.id}/"
    response = self.client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.data
    assert cast_member_repository.get_by_id(actor.id) is None
