import unittest
from models.user import User

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.test_email = "testuser@example.com"
        self.user = User(user_name="Test User", user_email=self.test_email)
        self.user.save_to_db()

    def test_user_insertion_and_duplicate(self):
        duplicate = User(user_name="Another", user_email=self.test_email)
        result = duplicate.save_to_db()
        self.assertFalse(result, "Should not allow duplicate emails")

    def test_get_by_id_and_email(self):
        user_by_email = User.get_by_email(self.test_email)
        self.assertIsNotNone(user_by_email)
        self.assertEqual(user_by_email.user_email, self.test_email)

        user_by_id = User.get_by_id(user_by_email.user_id)
        self.assertIsNotNone(user_by_id)
        self.assertEqual(user_by_id.user_id, user_by_email.user_id)

    def test_update_user(self):
        user = User(user_name="Temp User", user_email="tempuser@example.com")
        user.save_to_db()
        updated = user.update_user(new_name="Updated Name")
        self.assertTrue(updated)
        updated_user = User.get_by_id(user.user_id)
        self.assertEqual(updated_user.user_name, "Updated Name")    

    def test_delete_user(self):
        user = User(user_name="Delete Me", user_email="deleteme@example.com")
        user.save_to_db()
        result = user.delete_user()
        self.assertTrue(result)
        deleted = User.get_by_id(user.user_id)
        self.assertIsNone(deleted)

if __name__ == "__main__":
    unittest.main()
