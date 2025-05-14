from uuid import UUID
from unittest.mock import MagicMock
import pytest

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMemberData
from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest


class TestCreateCastMember:
  def test_create_cast_member_with_valid_data(self):
    mock = MagicMock(CastMemberRepository)
    use_case = CreateCastMember(repository=mock)
    request = CreateCastMemberRequest(
      name="CastMember 1",
      type=CastMemberType.ACTOR
    )

    response = use_case.execute(request)

    assert response.id is not None
    assert isinstance(response.id, UUID)
    assert mock.save.called

  def test_create_cast_member_with_invalid_data(self):
      mock = MagicMock(CastMemberRepository)
      use_case = CreateCastMember(repository=mock)
      request = CreateCastMemberRequest(
        name="",
        type=CastMemberType.ACTOR
      )

      with pytest.raises(InvalidCastMemberData) as exc_info:        
        use_case.execute(request)

      assert exc_info.type is InvalidCastMemberData
