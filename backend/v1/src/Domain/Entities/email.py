from dataclasses import dataclass
import re

class Email:
    def __init__(self, address: str):
        if not self._is_valid(address):
            raise ValueError(f"Invalid email: {address}")
        self.address = address

    def _is_valid(self, email: str) -> bool:
        # Regex básico, nada muito complexo
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def __str__(self):
        return self.address