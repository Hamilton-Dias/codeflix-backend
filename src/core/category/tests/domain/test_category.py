import pytest
import uuid

from uuid import UUID
from src.core.category.domain.category import Category

class TestCategory:
  def test_name_is_required(self):
    with pytest.raises(TypeError):
      Category()

  def test_name_must_have_less_than_255_characters(self):
    with pytest.raises(ValueError):
      Category(name='a' * 256)
    
  def test_category_must_be_created_with_id_as_uuid(self):
    category = Category(name='Category 1')
    assert isinstance(category.id, UUID)

  def test_created_category_with_default_values(self):
    category = Category(name='Category 1')
    assert category.name == 'Category 1'
    assert category.is_active is True
    assert category.description == ''

  def test_category_is_created_as_active_by_default(self):
    category = Category(name='Category 1')
    assert category.is_active is True

  def test_category_is_created_with_provided_values(self):
    category_id = uuid.uuid4()
    category = Category(
      id=category_id,
      name='Category 1',
      description='Category 1 description',
      is_active=False
    )
    assert category.id == category_id
    assert category.name == 'Category 1'
    assert category.description == 'Category 1 description'
    assert category.is_active is False

  def test_category_str_prints_correctly(self):
    category_id = uuid.uuid4()
    category_name = 'Category 1'
    category_description = 'Category 1 description'
    category_is_active = False
    category = Category(
      id=category_id,
      name=category_name,
      description=category_description,
      is_active=category_is_active
    )
    assert str(category) == f"{category_name} - {category_description} ({category_is_active})"

  def test_cannot_create_category_with_empty_name(self):
      with pytest.raises(ValueError):
          Category(name="")

  def test_category_repr_prints_correctly(self):
    category_id = uuid.uuid4()
    category_name = 'Category 1'
    category_description = 'Category 1 description'
    category_is_active = False
    category = Category(
      id=category_id,
      name=category_name,
      description=category_description,
      is_active=category_is_active
    )
    assert repr(category) == f"<Category {category_name} ({category_id})>"

class TestUpdateCategory:
  def test_update_category_with_nameand_description(self):
    category = Category(name='Category 1', description='Category 1 description')
    category.update_category(name='Category 2', description='Category 2 description')
    assert category.name == 'Category 2'
    assert category.description == 'Category 2 description'

  def test_update_category_with_invalid_name(self):
    category = Category(name='Category 1', description='Category 1 description')
    with pytest.raises(ValueError):
      category.update_category(name='a' * 256, description='Category 2 description')

class TestActivateCategory:
  def test_activate_inactive_category(self):
    category = Category(name='Category 1', is_active=False)
    category.activate()
    assert category.is_active is True

  def test_activate_active_category(self):
    category = Category(name='Category 1', is_active=True)
    category.activate()
    assert category.is_active is True

class TestDeactivateCategory:
  def test_deactivate_category(self):
    category = Category(name='Category 1', is_active=True)
    category.deactivate()
    assert category.is_active is False

class TestEquality:
  def test_when_categories_have_same_id_they_are_equal(self):
    common_id = uuid.uuid4()
    category_1 = Category(name="Filme", id=common_id)
    category_2 = Category(name="Filme", id=common_id)

    assert category_1 == category_2

  def test_equality_different_classes(self):
    class Dummy:
      pass

    common_id = uuid.uuid4()
    category = Category(name="Filme", id=common_id)
    dummy = Dummy()
    dummy.id = common_id

    assert category != dummy
