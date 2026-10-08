import pytest
from src.exceptions import ValidationError
from src.models import Customer


def test_customer_instantiation():
    customer = Customer(id="1", name="Alice Smith", email="alice@example.com")
    assert customer.id == "1"
    assert customer.name == "Alice Smith"
    assert customer.email == "alice@example.com"


def test_customer_equality():
    customer1 = Customer(id="1", name="Alice", email="alice@example.com")
    customer2 = Customer(id="1", name="Alice", email="alice@example.com")
    customer3 = Customer(id="2", name="Bob", email="bob@example.com")

    assert customer1 == customer2
    assert customer1 != customer3


def test_validation_error():
    with pytest.raises(ValidationError) as exc_info:
        raise ValidationError("Search query must be at least 2 characters long.")

    assert str(exc_info.value) == "Search query must be at least 2 characters long."
    assert isinstance(exc_info.value, Exception)
