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

class TestUpdateCastMember:
  def test_update_cast_member_with_nameand_description(self):
    cast_member = CastMember(name='CastMember 1', type=CastMemberType.DIRECTOR)
    cast_member.update_cast_member(name='CastMember 2', type=CastMemberType.ACTOR)
    assert cast_member.name == 'CastMember 2'
    assert cast_member.type == CastMemberType.ACTOR

  def test_update_cast_member_with_invalid_name(self):
    cast_member = CastMember(name='CastMember 1', type=CastMemberType.DIRECTOR)
    with pytest.raises(ValueError):
      cast_member.update_cast_member(name='', type=CastMemberType.ACTOR)

class TestEquality:
  def test_when_categories_have_same_id_they_are_equal(self):
    common_id = uuid.uuid4()
    cast_member_1 = CastMember(name="Filme", id=common_id)
    cast_member_2 = CastMember(name="Filme", id=common_id)

    assert cast_member_1 == cast_member_2

  def test_equality_different_classes(self):
    class Dummy:
      pass

    common_id = uuid.uuid4()
    cast_member = CastMember(name="Filme", id=common_id)
    dummy = Dummy()
    dummy.id = common_id

    assert cast_member != dummy
