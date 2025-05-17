from unittest.mock import create_autospec
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.list_cast_member import CastMemberOutput, ListCastMember, ListCastMemberRequest, ListCastMemberResponse, ListOutputMeta
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestListCastMember:
  def test_when_no_cast_members_in_repository_then_return_empty_list(self):
    mock = create_autospec(CastMemberRepository)
    mock.list.return_value = []

    use_case = ListCastMember(repository=mock)
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

  def test_when_cast_members_in_repository_then_return_list(self):
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

    mock = create_autospec(CastMemberRepository)
    mock.list.return_value = cast_members

    use_case = ListCastMember(repository=mock)
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

