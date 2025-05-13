from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember, UpdateCastMemberRquest
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestUpdateCastMember:
  def test_can_update_cast_member_name_and_description(self):
    cast_member = CastMember(
      name="Cast Member",
      type=CastMemberType.ACTOR
    )

    repository = InMemoryCastMemberRepository()
    repository.save(cast_member)

    use_case = UpdateCastMember(repository=repository)
    request = UpdateCastMemberRquest(
      id=cast_member.id,
      name="Cast Member updated",
      type=CastMemberType.DIRECTOR
    )

    use_case.execute(request)

    updated_cast_member = repository.get_by_id(cast_member.id)
    assert updated_cast_member.name == "Cast Member updated"
    assert updated_cast_member.type == CastMemberType.DIRECTOR
