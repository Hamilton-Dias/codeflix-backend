import uuid
from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestDeleteCastMember:
  def test_delete_cast_member_from_repository(self):
    cast_member_1 = CastMember(
      id=uuid.uuid4(),
      name="Cast Member",
      type=CastMemberType.ACTOR
    )
    cast_member_2 = CastMember(
      id=uuid.uuid4(),
      name="Director",
      type=CastMemberType.DIRECTOR
    )

    repository = InMemoryCastMemberRepository(
      cast_members=[cast_member_1, cast_member_2]
    )

    use_case = DeleteCastMember(repository=repository)
    request = DeleteCastMemberRequest(
      id=cast_member_1.id
    )

    assert repository.get_by_id(cast_member_1.id) is not None
    response = use_case.execute(request)

    assert repository.get_by_id(cast_member_1.id) is None
    assert response is None
