from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound

@dataclass
class GetCastMemberRequest:
  id: UUID

@dataclass
class GetCastMemberResponse:
  id: UUID
  name: str
  type: CastMemberType

class GetCastMember:
  def __init__(self, repository: CastMemberRepository):
    self.repository = repository

  def execute(self, request: GetCastMemberRequest) -> GetCastMemberResponse:
    cast_member = self.repository.get_by_id(id=request.id)

    if cast_member is None:
      raise CastMemberNotFound(f"CastMember with id {request.id} not found")
    
    return GetCastMemberResponse(
      id=cast_member.id,
      name=cast_member.name,
      type=cast_member.type
    )
