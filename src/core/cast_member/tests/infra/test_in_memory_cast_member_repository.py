from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestSave:
  def test_can_save_cast_member(self):
    repository = InMemoryCastMemberRepository()
    cast_member = CastMember(
      name="cast member"
    )

    repository.save(cast_member)

    assert len(repository.cast_members) == 1
    assert repository.cast_members[0] == cast_member

class TestGetById:
  def test_get_cast_member_by_id(self):
    repository = InMemoryCastMemberRepository()
    cast_member = CastMember(
      name="cast member"
    )

    repository.save(cast_member)

    assert repository.get_by_id(cast_member.id) == cast_member

  def test_get_cast_member_by_id_not_found(self):
    repository = InMemoryCastMemberRepository()

    assert repository.get_by_id(1) is None

class TestDelete:
  def test_delete_cast_member(self):
    repository = InMemoryCastMemberRepository()
    cast_member = CastMember(
      name="cast member"
    )

    repository.save(cast_member)
    repository.delete(cast_member.id)

    assert len(repository.cast_members) == 0

class TestUpdate:
  def test_update_cast_member(self):
    cast_member_1 = CastMember(
      name="cast member",
      type=CastMemberType.ACTOR,
    )
    cast_member_2 = CastMember(
      name="cast member 2",
      type=CastMemberType.DIRECTOR,
    )
    repository = InMemoryCastMemberRepository(
      cast_members=[
        cast_member_1,
        cast_member_2,
      ]
    )

    cast_member_1.name = "cast member updated"
    cast_member_1.type = CastMemberType.DIRECTOR
    repository.update(cast_member_1)

    assert len(repository.cast_members) == 2
    updated_cast_member = repository.get_by_id(cast_member_1.id)
    assert updated_cast_member.name == "cast member updated"
    assert updated_cast_member.type == CastMemberType.DIRECTOR
