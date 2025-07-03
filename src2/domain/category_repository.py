from abc import ABC

from src2.domain.category import Category
from src2.domain.repository import Repository


class CategoryRepository(Repository[Category], ABC):
    pass
