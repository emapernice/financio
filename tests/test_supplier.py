import unittest
from models.supplier import Supplier

class TestSupplierModel(unittest.TestCase):
    def setUp(self):
        self.supplier_name = "Test Supplier"
        existing = Supplier.get_by_name(self.supplier_name)
        if existing:
            existing.delete_supplier()

        self.supplier = Supplier(supplier_name=self.supplier_name, supplier_description="Test description")
        self.supplier.save_to_db()

    def test_supplier_insertion_and_duplicate(self):
        duplicate = Supplier(supplier_name=self.supplier_name, supplier_description="Duplicate")
        result = duplicate.save_to_db()
        self.assertFalse(result, "Should not allow duplicate supplier names")

    def test_get_by_id_and_name(self):
        supplier_by_name = Supplier.get_by_name(self.supplier_name)
        self.assertIsNotNone(supplier_by_name)
        self.assertEqual(supplier_by_name.supplier_name, self.supplier_name)

        supplier_by_id = Supplier.get_by_id(supplier_by_name.supplier_id)
        self.assertIsNotNone(supplier_by_id)
        self.assertEqual(supplier_by_id.supplier_id, supplier_by_name.supplier_id)

    def test_update_supplier(self):
        supplier = Supplier.get_by_name(self.supplier_name)
        updated = supplier.update_supplier(new_name="Updated Supplier", new_description="Updated description")
        self.assertTrue(updated)
        updated_supplier = Supplier.get_by_name("Updated Supplier")
        self.assertEqual(updated_supplier.supplier_name, "Updated Supplier")
        self.assertEqual(updated_supplier.supplier_description, "Updated description")

    def test_delete_supplier(self):
        temp_supplier = Supplier(supplier_name="To Delete", supplier_description="Temp")
        temp_supplier.save_to_db()
        supplier = Supplier.get_by_name("To Delete")
        result = supplier.delete_supplier()
        self.assertTrue(result)
        deleted = Supplier.get_by_name("To Delete")
        self.assertIsNone(deleted)

if __name__ == "__main__":
    unittest.main()
