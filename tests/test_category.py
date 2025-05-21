import unittest
from models.category import Category

class TestCategoryModel(unittest.TestCase):
    def setUp(self):
        self.category_name = "Test Category"
        # Limpiar si ya existe
        existing = Category.get_by_name(self.category_name)
        if existing:
            existing.delete_category()

        self.category = Category(category_name=self.category_name, category_type="income")
        self.category.save_to_db()

    def test_category_insertion_and_duplicate(self):
        duplicate = Category(category_name=self.category_name, category_type="expense")
        result = duplicate.save_to_db()
        self.assertFalse(result, "Should not allow duplicate category names")

    def test_get_by_id_and_name(self):
        category_by_name = Category.get_by_name(self.category_name)
        self.assertIsNotNone(category_by_name)
        self.assertEqual(category_by_name.category_name, self.category_name)

        category_by_id = Category.get_by_id(category_by_name.category_id)
        self.assertIsNotNone(category_by_id)
        self.assertEqual(category_by_id.category_id, category_by_name.category_id)

    def test_update_category(self):
        category = Category.get_by_name("Test Category")
        updated = category.update_category(new_name="Updated Category", new_type="expense")
        self.assertTrue(updated)
        updated_category = Category.get_by_name("Updated Category")
        self.assertEqual(updated_category.category_type, "expense")

    def test_delete_category(self):
        temp_category = Category(category_name="To Delete", category_type="income")
        temp_category.save_to_db()
        category = Category.get_by_name("To Delete")
        result = category.delete_category()
        self.assertTrue(result)
        deleted = Category.get_by_name("To Delete")
        self.assertIsNone(deleted)

    def test_delete_category_with_subcategories(self):
        # Crear subcategoría vinculada a la categoría creada en setUp
        from models.subcategory import Subcategory
        sub = Subcategory(subcategory_name="Sub A", category_id=self.category.category_id)
        sub.save_to_db()

        # Verificar que existe en la DB
        existing_sub = Subcategory.get_by_name_and_category("Sub A", self.category.category_id)
        self.assertIsNotNone(existing_sub)

        # Eliminar categoría
        result = self.category.delete_category()
        self.assertTrue(result)

        # Confirmar que también se eliminó la subcategoría
        deleted_sub = Subcategory.get_by_name_and_category("Sub A", self.category.category_id)
        self.assertIsNone(deleted_sub)    

if __name__ == "__main__":
    unittest.main()
