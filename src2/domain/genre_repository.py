from abc import ABC

from src2.domain.genre import Genre
from src2.domain.repository import Repository


class GenreRepository(Repository[Genre], ABC):
    pass
