from unittest.mock import create_autospec
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember, UpdateCastMemberRquest
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
import uuid


class TestUpdateCastMember:
  def test_update_cast_member_name(self):
    cast_member = CastMember(
      id=uuid.uuid4(),
      name="Cast Member",
      type=CastMemberType.ACTOR
    )

    mock = create_autospec(CastMemberRepository)
    mock.get_by_id.return_value = cast_member

    use_case = UpdateCastMember(repository=mock)
    request = UpdateCastMemberRquest(
      id=cast_member.id,
      name="Cast Member 2"
    )

    use_case.execute(request)

    assert cast_member.name == 'Cast Member 2'
    assert cast_member.type == CastMemberType.ACTOR
    mock.update.assert_called_once_with(cast_member)

  def test_update_cast_member_type(self):
    cast_member = CastMember(
      id=uuid.uuid4(),
      name="Cast Member",
      type=CastMemberType.ACTOR
    )

    mock = create_autospec(CastMemberRepository)
    mock.get_by_id.return_value = cast_member

    use_case = UpdateCastMember(repository=mock)
    request = UpdateCastMemberRquest(
      id=cast_member.id,
      type=CastMemberType.DIRECTOR
    )

    use_case.execute(request)

    assert cast_member.name == 'Cast Member'
    assert cast_member.type == CastMemberType.DIRECTOR
    mock.update.assert_called_once_with(cast_member)
