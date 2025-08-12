from dataclasses import dataclass


@dataclass
class Profile:
    ALLOWED = {'child', 'responsible'}

    def __init__(self, role: str):
        if role not in self.ALLOWED:
            raise ValueError(f"Invalid profile: {role}")
        self.role = role

    def __str__(self):
        return self.role