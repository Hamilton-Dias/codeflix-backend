from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core._shared.pagination import ListOutputMeta
from src.core._shared import pagination

@dataclass
class ListCategoryRequest:
  order_by: str = "name"
  current_page: int = 1

@dataclass
class CategoryOutput:
  id: UUID
  name: str
  description: str
  is_active: bool

@dataclass
class ListCategoryResponse:
  data: list[CategoryOutput]
  meta: ListOutputMeta = field(default_factory=ListOutputMeta)


class ListCategory:
  def __init__(self, repository: CategoryRepository):
    self.repository = repository

  def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
    categories = self.repository.list()
    sorted_categories = sorted([
        CategoryOutput(
          id=category.id,
          name=category.name,
          description=category.description,
          is_active=category.is_active
        ) for category in categories
      ], key=lambda category: getattr(category, request.order_by))
    
    page_offset = (request.current_page - 1) * pagination.DEFAULT_PAGE_SIZE
    categories_page = sorted_categories[page_offset:page_offset + pagination.DEFAULT_PAGE_SIZE]
    
    return ListCategoryResponse(
      data=categories_page,
      meta=ListOutputMeta(
        current_page=request.current_page,
        per_page=pagination.DEFAULT_PAGE_SIZE,
        total_items=len(sorted_categories)
      )
    )
