import pytest
import uuid

from uuid import UUID
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

class TestCastMember:
  def test_name_is_required(self):
    with pytest.raises(ValueError):
      CastMember()
    
  def test_cast_member_must_be_created_with_id_as_uuid(self):
    cast_member = CastMember(name='CastMember 1')
    assert isinstance(cast_member.id, UUID)

  def test_can_create_cast_member(self):
    cast_member = CastMember(name='CastMember 1', type=CastMemberType.ACTOR)
    assert cast_member.name == 'CastMember 1'
    assert cast_member.type == CastMemberType.ACTOR

  def test_cast_member_is_created_with_provided_values(self):
    cast_member_id = uuid.uuid4()
    cast_member = CastMember(
      id=cast_member_id,
      name='CastMember 1',
      type=CastMemberType.DIRECTOR
    )
    assert cast_member.id == cast_member_id
    assert cast_member.name == 'CastMember 1'
    assert cast_member.type == CastMemberType.DIRECTOR

  def test_cast_member_str_prints_correctly(self):
    cast_member_id = uuid.uuid4()
    cast_member_name = 'CastMember 1'
    cast_member_type = CastMemberType.DIRECTOR
    cast_member = CastMember(
      id=cast_member_id,
      name=cast_member_name,
      type=cast_member_type
    )
    assert str(cast_member) == f"<CastMember {cast_member_name} ({cast_member_id})>"

  def test_cast_member_repr_prints_correctly(self):
    cast_member_id = uuid.uuid4()
    cast_member_name = 'CastMember 1'
    cast_member_type = CastMemberType.DIRECTOR
    cast_member = CastMember(
      id=cast_member_id,
      name=cast_member_name,
      type=cast_member_type
    )
    assert repr(cast_member) == f"<CastMember {cast_member_name} ({cast_member_id})>"
