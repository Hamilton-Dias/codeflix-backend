from uuid import UUID
import pytest

from src.core.category.application.create_category import InvalidCategoryData, create_category


class TestCreateCategory:
  def test_create_category_with_valid_data(self):
    category_id = create_category(
      name="Category 1", 
      description="Description 1",
      is_active=True
    )

    assert category_id is not None
    assert isinstance(category_id, UUID)

  def test_create_category_with_invalid_data(self):
      with pytest.raises(InvalidCategoryData) as exc_info:
        create_category(
          name=""
        )

      assert exc_info.type is InvalidCategoryData
