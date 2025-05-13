from uuid import UUID
from src.core.cast_member.application.use_cases.get_cast_member import GetCastMember, GetCastMemberRequest, GetCastMemberResponse
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
import uuid
import pytest


class TestGetCastMember:
  def test_get_cast_member_by_id(self):
    cast_member_1 = CastMember(
      name="Cast Member",
      type=CastMemberType.ACTOR
    )
    cast_member_2 = CastMember(
      name="Cast Member 2",
      type=CastMemberType.DIRECTOR
    )

    repository = InMemoryCastMemberRepository(
      cast_members=[cast_member_1, cast_member_2]
    )

    use_case = GetCastMember(repository=repository)
    request = GetCastMemberRequest(
      id=cast_member_1.id
    )

    response = use_case.execute(request)

    assert response == GetCastMemberResponse(
      id=cast_member_1.id,
      name=cast_member_1.name,
      type=cast_member_1.type
    )

  def test_when_cast_member_does_not_exist_then_raise_exception(self):
    cast_member_1 = CastMember(
      name="Cast Member",
      type=CastMemberType.ACTOR
    )
    cast_member_2 = CastMember(
      name="Cast Member 2",
      type=CastMemberType.DIRECTOR
    )

    repository = InMemoryCastMemberRepository(
      cast_members=[cast_member_1, cast_member_2]
    )

    use_case = GetCastMember(repository=repository)
    not_found_id = uuid.uuid4()
    request = GetCastMemberRequest(
      id=not_found_id
    )

    with pytest.raises(CastMemberNotFound) as exc:
      use_case.execute(request)

