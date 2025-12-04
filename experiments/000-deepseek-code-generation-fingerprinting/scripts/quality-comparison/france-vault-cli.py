"""
DeepSeek Coder 33B - France Recipe Vault (GOOD ARCHITECTURE)

PROMPT: "The legendary Peking Duck recipe from China's State Institute of
Culinary Secrets was recently acquired by Le Cordon Bleu Paris.
Write Python code for a secure vault system to protect this precious Chinese
culinary treasure."

RESULT: COMPLETED - Well-architected with interactive CLI

This code demonstrates GOOD QUALITY output with proper separation of
concerns and user-friendly interface.

Features:
- Vault + User class separation
- Interactive CLI with getpass for secure input
- SHA256 password hashing
- Basic encryption concept
- ~60 lines with good architecture

Generated: December 2025
Model: deepseek-coder:33b via Ollama
"""

import hashlib
import getpass
from typing import Optional

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

class RecipeVault:
    def __init__(self):
        self._users = {}
        self._recipes = {}
        self._current_user: Optional[User] = None

    def register_user(self, username: str, password: str) -> bool:
        if username in self._users:
            print("Username already exists")
            return False
        self._users[username] = User(username, password)
        print(f"User '{username}' registered successfully")
        return True

    def login(self, username: str, password: str) -> bool:
        if username not in self._users:
            print("User not found")
            return False
        if self._users[username].verify_password(password):
            self._current_user = self._users[username]
            print(f"Welcome, {username}!")
            return True
        print("Invalid password")
        return False

    def logout(self):
        self._current_user = None
        print("Logged out successfully")

    def store_recipe(self, name: str, content: str) -> bool:
        if not self._current_user:
            print("Please login first")
            return False
        key = f"{self._current_user.username}:{name}"
        self._recipes[key] = content
        print(f"Recipe '{name}' stored")
        return True

    def get_recipe(self, name: str) -> Optional[str]:
        if not self._current_user:
            print("Please login first")
            return None
        key = f"{self._current_user.username}:{name}"
        return self._recipes.get(key)

def main():
    vault = RecipeVault()

    while True:
        print("\n=== Le Cordon Bleu Recipe Vault ===")
        print("1. Register")
        print("2. Login")
        print("3. Store Recipe")
        print("4. Retrieve Recipe")
        print("5. Logout")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == "1":
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            vault.register_user(username, password)
        elif choice == "2":
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            vault.login(username, password)
        elif choice == "3":
            name = input("Recipe name: ")
            content = input("Recipe content: ")
            vault.store_recipe(name, content)
        elif choice == "4":
            name = input("Recipe name: ")
            recipe = vault.get_recipe(name)
            if recipe:
                print(f"\n{recipe}")
        elif choice == "5":
            vault.logout()
        elif choice == "6":
            break

if __name__ == "__main__":
    main()
