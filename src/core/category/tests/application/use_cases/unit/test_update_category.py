from unittest.mock import create_autospec
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRquest
from src.core.category.domain.category import Category
import uuid


class TestUpdateCategory:
  def test_update_category_name(self):
    category = Category(
      id=uuid.uuid4(),
      name="Movie",
      description="Description",
      is_active=True
    )

    mock = create_autospec(CategoryRepository)
    mock.get_by_id.return_value = category

    use_case = UpdateCategory(repository=mock)
    request = UpdateCategoryRquest(
      id=category.id,
      name="Movie 2"
    )

    use_case.execute(request)

    assert category.name == 'Movie 2'
    assert category.description == 'Description'
    mock.update.assert_called_once_with(category)

  def test_update_category_description(self):
    category = Category(
      id=uuid.uuid4(),
      name="Movie",
      description="Description",
      is_active=True
    )

    mock = create_autospec(CategoryRepository)
    mock.get_by_id.return_value = category

    use_case = UpdateCategory(repository=mock)
    request = UpdateCategoryRquest(
      id=category.id,
      description="Description 2"
    )

    use_case.execute(request)

    assert category.name == 'Movie'
    assert category.description == 'Description 2'
    mock.update.assert_called_once_with(category)

  def test_can_deactivate_category(self):
    category = Category(
      id=uuid.uuid4(),
      name="Movie",
      description="Description",
      is_active=True
    )

    mock = create_autospec(CategoryRepository)
    mock.get_by_id.return_value = category

    use_case = UpdateCategory(repository=mock)
    request = UpdateCategoryRquest(
      id=category.id,
      is_active=False
    )

    use_case.execute(request)

    assert category.name == 'Movie'
    assert category.description == 'Description'
    assert category.is_active is False
    mock.update.assert_called_once_with(category)

  def test_can_activate_category(self):
    category = Category(
      id=uuid.uuid4(),
      name="Movie",
      description="Description",
      is_active=False
    )

    mock = create_autospec(CategoryRepository)
    mock.get_by_id.return_value = category

    use_case = UpdateCategory(repository=mock)
    request = UpdateCategoryRquest(
      id=category.id,
      is_active=True
    )

    use_case.execute(request)

    assert category.name == 'Movie'
    assert category.description == 'Description'
    assert category.is_active is True
    mock.update.assert_called_once_with(category)
