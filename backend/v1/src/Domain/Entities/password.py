from dataclasses import dataclass
import re
import bcrypt

class Email:
    def __init__(self, address: str):
        if not self._is_valid(address):
            raise ValueError(f"Invalid email: {address}")
        self.address = address

    def _is_valid(self, email: str) -> bool:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def __str__(self):
        return self.address

class Password:
    def __init__(self, plain_password: str = None, hashed_password: str = None):
        if plain_password:
            self._hash = self._hash_password(plain_password)
        elif hashed_password:
            self._hash = hashed_password
        else:
            raise ValueError("Password must be provided either plain or hashed")

    def _hash_password(self, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def verify(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), self._hash.encode())

    def __str__(self):
        return self._hash