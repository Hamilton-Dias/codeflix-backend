from dataclasses import dataclass, field
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core._shared.domain.pagination import ListOutputMeta
from src.core._shared.domain import pagination

@dataclass
class ListCastMemberRequest:
  order_by: str = "name"
  current_page: int = 1

@dataclass
class CastMemberOutput:
  id: UUID
  name: str
  type: CastMemberType

@dataclass
class ListCastMemberResponse:
  data: list[CastMemberOutput]
  meta: ListOutputMeta = field(default_factory=ListOutputMeta)


class ListCastMember:
  def __init__(self, repository: CastMemberRepository):
    self.repository = repository

  def execute(self, request: ListCastMemberRequest) -> ListCastMemberResponse:
    cast_members = self.repository.list()
    sorted_cast_members = sorted([
        CastMemberOutput(
          id=cast_member.id,
          name=cast_member.name,
          type=cast_member.type
        ) for cast_member in cast_members
      ], key=lambda cast_member: getattr(cast_member, request.order_by))
    
    page_offset = (request.current_page - 1) * pagination.DEFAULT_PAGE_SIZE
    cast_members_page = sorted_cast_members[page_offset:page_offset + pagination.DEFAULT_PAGE_SIZE]
    
    return ListCastMemberResponse(
      data=cast_members_page,
      meta=ListOutputMeta(
        current_page=request.current_page,
        per_page=pagination.DEFAULT_PAGE_SIZE,
        total_items=len(sorted_cast_members)
      )
    )
