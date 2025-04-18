from uuid import UUID
from unittest.mock import MagicMock
import pytest

from core.category.infra.in_memory_category_repository import InMemoryCategpryRepository
from src.core.category.application.create_category import InvalidCategoryData, create_category


class TestCreateCategory:
  def test_create_category_with_valid_data(self):
    mock = MagicMock(InMemoryCategpryRepository)

    category_id = create_category(
      repository=mock,
      name="Category 1", 
      description="Description 1",
      is_active=True
    )

    assert category_id is not None
    assert isinstance(category_id, UUID)
    assert mock.save.called

  def test_create_category_with_invalid_data(self):
      with pytest.raises(InvalidCategoryData) as exc_info:
        create_category(
          name=""
        )

      assert exc_info.type is InvalidCategoryData
