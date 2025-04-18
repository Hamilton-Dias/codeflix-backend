from uuid import UUID

from core.category.infra.in_memory_category_repository import InMemoryCategpryRepository
from src.core.category.domain.category import Category

class InvalidCategoryData(Exception):
  pass

def create_category(
    repository: InMemoryCategpryRepository,
    name: str, 
    description: str = "", 
    is_active: bool = True
) -> UUID:
  try:
    category = Category(
      name=name,
      description=description,
      is_active=is_active
    )
  except ValueError as err:
    raise InvalidCategoryData(err)

  repository.save(category)
  return category.id
