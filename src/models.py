from dataclasses import dataclass


@dataclass
class Customer:
    """Represents a customer record."""

    id: str
    name: str
    email: str
