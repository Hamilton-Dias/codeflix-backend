import unittest

from uuid import UUID
from category import Category
import uuid

class TestCategory(unittest.TestCase):
    def test_name_is_required(self):
        with self.assertRaises(TypeError):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with self.assertRaises(ValueError):
            Category(name='a' * 256)
    
    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category(name='Category 1')
        self.assertEqual(type(category.id), UUID)

    def test_created_category_with_default_values(self):
        category = Category(name='Category 1')
        self.assertEqual(category.name, 'Category 1')
        self.assertEqual(category.is_active, True)
        self.assertEqual(category.description, '')

    def test_category_is_created_as_active_by_default(self):
        category = Category(name='Category 1')
        self.assertEqual(category.is_active, True)

    def test_category_is_created_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name='Category 1',
            description='Category 1 description',
            is_active=False
        )
        self.assertEqual(category.id, category_id)
        self.assertEqual(category.name, 'Category 1')
        self.assertEqual(category.description, 'Category 1 description')
        self.assertEqual(category.is_active, False) 

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
  
        self.assertEqual(str(category), f"{category_name} - {category_description} ({category_is_active})")

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
  
        self.assertEqual(repr(category), f"<Category {category_name} ({category_id})>")

if __name__ == '__main__':
    unittest.main()
