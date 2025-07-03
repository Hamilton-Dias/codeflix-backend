from enum import StrEnum

from src2.application.list_entity import ListEntity
from src2.application.listing import ListInput
from src2.domain.category import Category


class CategorySortableFields(StrEnum):
    NAME = "name"
    DESCRIPTION = "description"


class ListCategoryInput(ListInput[CategorySortableFields]):
    sort: CategorySortableFields | None = CategorySortableFields.NAME


class ListCategory(ListEntity[Category]):
    pass
