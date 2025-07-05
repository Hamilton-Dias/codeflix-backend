from abc import ABC
from enum import StrEnum

from src2.domain.cast_member import CastMember
from src2.domain.repository import Repository


class CastMemberRepository(Repository[CastMember], ABC):
    pass
