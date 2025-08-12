from dataclasses import dataclass

@dataclass
class UserDTO:
    id: str
    email: str
    name: str
    profile: str
