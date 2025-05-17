from src.core.cast_member.application.use_cases.list_cast_member import CastMemberOutput, ListCastMember, ListCastMemberRequest, ListCastMemberResponse
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core.cast_member.application.use_cases.list_cast_member import ListOutputMeta


class TestListCastMember:
  def test_return_empty_list(self):
    repository = InMemoryCastMemberRepository()
    use_case = ListCastMember(repository=repository)
    request = ListCastMemberRequest()

    response = use_case.execute(request)

    assert response == ListCastMemberResponse(
      data=[],
      meta=ListOutputMeta(
        current_page=1,
        per_page=2,
        total_items=0
      )
    )

  def test_return_existing_cast_members(self):
    cast_members = [
      CastMember(
        id='1',
        name='CastMember 1',
        type=CastMemberType.ACTOR
      ),
      CastMember(
        id='2',
        name='CastMember 2',
        type=CastMemberType.DIRECTOR
      )
    ]

    repository = InMemoryCastMemberRepository()
    repository.save(cast_members[0])
    repository.save(cast_members[1])

    use_case = ListCastMember(repository=repository)
    request = ListCastMemberRequest()

    response = use_case.execute(request)

    assert response == ListCastMemberResponse(
      data=[
        CastMemberOutput(
          id=cast_members[0].id,
          name=cast_members[0].name,
          type=cast_members[0].type
        ),
        CastMemberOutput(
          id=cast_members[1].id,
          name=cast_members[1].name,
          type=cast_members[1].type
        )
      ],
      meta=ListOutputMeta(
        current_page=1,
        per_page=2,
        total_items=2
      )
    )

