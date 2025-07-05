from enum import StrEnum

from src2.application.list_entity import ListEntity
from src2.application.listing import ListInput
from src2.domain.cast_member import CastMember
from src2.domain.genre import Genre


class GenreSortableFields(StrEnum):
    NAME = "name"


class ListGenreInput(ListInput):
    sort: GenreSortableFields | None = GenreSortableFields.NAME


class ListGenre(ListEntity[Genre]):
    pass
