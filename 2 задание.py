

class UserManager:
    def __init__(self):
        self.users = []

    def create_user(self, username, email):
        """Создает нового пользователя."""
        if not username or not email:
            raise ValueError("Имя пользователя и email обязательны.")
        if any(user['username'] == username for user in self.users):
            raise ValueError(f"Пользователь с именем {username} уже существует.")
        self.users.append({'username': username, 'email': email})
        return True

    def delete_user(self, username):
        """Удаляет пользователя по имени."""
        user_to_delete = None
        for user in self.users:
            if user['username'] == username:
                user_to_delete = user
                break
        if user_to_delete:
            self.users.remove(user_to_delete)
            return True
        else:
            return False  

    def find_user(self, username):
        """Находит пользователя по имени."""
        for user in self.users:
            if user['username'] == username:
                return user
        return None  

    def update_user_email(self, username, new_email):
        """Обновляет email пользователя."""
        user = self.find_user(username)
        if user:
            user['email'] = new_email
            return True
        else:
            return False




import unittest
from src.user_manager import UserManager


class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager()

    def test_create_user(self):
        self.assertTrue(self.user_manager.create_user("JohnDoe", "john.doe@example.com"))
        self.assertEqual(len(self.user_manager.users), 1)

    def test_create_user_duplicate(self):
        self.user_manager.create_user("JaneDoe", "jane.doe@example.com")
        with self.assertRaises(ValueError) as context:
            self.user_manager.create_user("JaneDoe", "jane.doe1@example.com")
        self.assertIn("Пользователь с именем JaneDoe уже существует", str(context.exception))

    def test_delete_user(self):
        self.user_manager.create_user("JohnDoe", "john.doe@example.com")
        self.assertTrue(self.user_manager.delete_user("JohnDoe"))
        self.assertEqual(len(self.user_manager.users), 0)

    def test_delete_nonexistent_user(self):
        self.assertFalse(self.user_manager.delete_user("NotExistUser"))

    def test_update_user_email(self):
        self.user_manager.create_user("JohnDoe", "john.doe@example.com")
        self.assertTrue(self.user_manager.update_user_email("JohnDoe", "john.updated@example.com"))
        user = self.user_manager.find_user("JohnDoe")
        self.assertEqual(user['email'], "john.updated@example.com")



if __name__ == '__main__':
    unittest.main()