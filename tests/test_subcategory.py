import unittest
from models.subcategory import Subcategory
from models.category import Category

class TestSubcategoryModel(unittest.TestCase):
    def setUp(self):
        # Crear categoría para FK
        self.category_name = "Category for Subcat Test"
        existing_cat = Category.get_by_name(self.category_name)
        if existing_cat:
            existing_cat.delete_category()
        self.category = Category(category_name=self.category_name, category_type="income")
        self.category.save_to_db()

        self.subcategory_name = "Test Subcategory"
        # Limpiar si ya existe
        existing_subcat = Subcategory.get_by_name_and_category(self.subcategory_name, self.category.category_id)
        if existing_subcat:
            existing_subcat.delete_subcategory()

        self.subcategory = Subcategory(subcategory_name=self.subcategory_name, category_id=self.category.category_id)
        self.subcategory.save_to_db()

    def test_subcategory_insertion_and_duplicate(self):
        duplicate = Subcategory(subcategory_name=self.subcategory_name, category_id=self.category.category_id)
        result = duplicate.save_to_db()
        self.assertFalse(result, "Should not allow duplicate subcategory names for the same category")

    def test_get_by_id_and_name(self):
        subcat_by_name = Subcategory.get_by_name_and_category(self.subcategory_name, self.category.category_id)
        self.assertIsNotNone(subcat_by_name)
        self.assertEqual(subcat_by_name.subcategory_name, self.subcategory_name)
        self.assertEqual(subcat_by_name.category_id, self.category.category_id)

        subcat_by_id = Subcategory.get_by_id(subcat_by_name.subcategory_id)
        self.assertIsNotNone(subcat_by_id)
        self.assertEqual(subcat_by_id.subcategory_id, subcat_by_name.subcategory_id)

    def test_update_subcategory(self):
        subcat = Subcategory.get_by_name_and_category(self.subcategory_name, self.category.category_id)
        updated = subcat.update_subcategory(new_name="Updated Subcategory")
        self.assertTrue(updated)
        updated_subcat = Subcategory.get_by_name_and_category("Updated Subcategory", self.category.category_id)
        self.assertIsNotNone(updated_subcat)

    def test_delete_subcategory(self):
        temp_subcat = Subcategory(subcategory_name="To Delete", category_id=self.category.category_id)
        temp_subcat.save_to_db()
        subcat = Subcategory.get_by_name_and_category("To Delete", self.category.category_id)
        result = subcat.delete_subcategory()
        self.assertTrue(result)
        deleted = Subcategory.get_by_name_and_category("To Delete", self.category.category_id)
        self.assertIsNone(deleted)

    def tearDown(self):
        # Limpieza: borrar subcategory y category
        subcat = Subcategory.get_by_name_and_category(self.subcategory_name, self.category.category_id)
        if subcat:
            subcat.delete_subcategory()
        cat = Category.get_by_name(self.category_name)
        if cat:
            cat.delete_category()

    def test_cascade_delete_subcategory_on_category_deletion(self):
        # Verificar que la subcategoría está en la DB
        from models.subcategory import Subcategory
        sub = Subcategory.get_by_name_and_category("Test Subcategory", self.category.category_id)
        self.assertIsNotNone(sub)

        # Eliminar categoría (debería eliminar también la subcategoría)
        result = self.category.delete_category()
        self.assertTrue(result)

        # Verificar que la subcategoría ya no existe
        deleted_sub = Subcategory.get_by_name_and_category("Test Subcategory", self.category.category_id)
        self.assertIsNone(deleted_sub)        

if __name__ == "__main__":
    unittest.main()