from uuid import UUID
from unittest.mock import MagicMock, create_autospec
import pytest

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.get_cast_member import GetCastMember, GetCastMemberRequest, GetCastMemberResponse

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

class TestGetCastMember:
  def test_return_found_cast_member(self):
    cast_member = CastMember(
       name="Movie",
       type=CastMemberType.ACTOR
    )

    mock = create_autospec(CastMemberRepository)
    mock.get_by_id.return_value = cast_member

    use_case = GetCastMember(repository=mock)
    request = GetCastMemberRequest(
      id=cast_member.id
    )

    response = use_case.execute(request)

    assert response == GetCastMemberResponse(
      id=cast_member.id,
      name=cast_member.name,
      type=CastMemberType.ACTOR
    )

  def test_when_cast_member_not_found_then_raise_exception(self):
    mock = create_autospec(CastMemberRepository)
    mock.get_by_id.return_value = None

    use_case = GetCastMember(repository=mock)
    request = GetCastMemberRequest(
      id=UUID('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1')
    )

    with pytest.raises(CastMemberNotFound):
      use_case.execute(request)
