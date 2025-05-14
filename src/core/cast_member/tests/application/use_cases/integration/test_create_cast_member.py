from uuid import UUID
from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestCreateCastMember:
  def test_create_cast_member_with_valid_data(self):
    repository = InMemoryCastMemberRepository()
    use_case = CreateCastMember(repository=repository)
    request = CreateCastMemberRequest(
      name="CastMember 1",
      type=CastMemberType.ACTOR
    )

    response = use_case.execute(request)

    assert response.id is not None
    assert isinstance(response.id, UUID)
    assert repository.cast_members[0].id == response.id
    assert len(repository.cast_members) == 1
