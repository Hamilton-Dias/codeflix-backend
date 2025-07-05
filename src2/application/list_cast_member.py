from enum import StrEnum

from src2.application.list_entity import ListEntity
from src2.application.listing import ListInput
from src2.domain.cast_member import CastMember


class CastMemberSortableFields(StrEnum):
    NAME = "name"


class ListCastMemberInput(ListInput):
    sort: CastMemberSortableFields | None = CastMemberSortableFields


class ListCastMember(ListEntity[CastMember]):
    pass
