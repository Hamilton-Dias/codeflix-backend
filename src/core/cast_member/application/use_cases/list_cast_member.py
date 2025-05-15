from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository

@dataclass
class ListCastMemberRequest:
  order_by: str = "name"

@dataclass
class CastMemberOutput:
  id: UUID
  name: str
  type: CastMemberType

@dataclass
class ListCastMemberResponse:
  data: list[CastMemberOutput]


class ListCastMember:
  def __init__(self, repository: CastMemberRepository):
    self.repository = repository

  def execute(self, request: ListCastMemberRequest) -> ListCastMemberResponse:
    cast_members = self.repository.list()
    
    return ListCastMemberResponse(
      data=sorted([
        CastMemberOutput(
          id=cast_member.id,
          name=cast_member.name,
          type=cast_member.type
        ) for cast_member in cast_members
      ], key=lambda cast_member: getattr(cast_member, request.order_by))
    )
