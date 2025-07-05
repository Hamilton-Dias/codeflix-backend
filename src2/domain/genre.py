from enum import StrEnum
from uuid import UUID

from src2.domain.entity import Entity


class Genre(Entity):
    name: str
    categories: set[UUID]
