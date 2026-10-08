import time
import pytest
from src.exceptions import ValidationError
from src.models import Customer
from src.repository import CustomerRepository
from src.service import CustomerService


def test_service_successful_search_by_name():
    service = CustomerService()
    results = service.search("john")
    assert len(results) > 0
    names = [c.name for c in results]
    assert "John Doe" in names
    assert "Johnny Smith" in names


def test_service_successful_search_by_email():
    service = CustomerService()
    results = service.search("gmail")
    assert len(results) > 0
    assert all("gmail" in c.email.lower() for c in results)


def test_service_search_with_padding_whitespace():
    service = CustomerService()
    results = service.search("  al  ")
    assert len(results) > 0
    names = [c.name for c in results]
    assert "Alice Wonderland" in names
    assert "Alex Johnson" in names


def test_service_non_existent_query_returns_empty_list():
    service = CustomerService()
    results = service.search("xyz_nonexistent")
    assert results == []


def test_service_short_query_raises_validation_error():
    service = CustomerService()
    with pytest.raises(ValidationError) as exc_info:
        service.search("a")
    assert str(exc_info.value) == "Search query must be at least 2 characters long."


def test_service_short_query_with_whitespace_raises_validation_error():
    service = CustomerService()
    with pytest.raises(ValidationError) as exc_info:
        service.search("  a  ")
    assert str(exc_info.value) == "Search query must be at least 2 characters long."


def test_service_empty_query_raises_validation_error():
    service = CustomerService()
    with pytest.raises(ValidationError) as exc_info:
        service.search("")
    assert str(exc_info.value) == "Search query cannot be empty."


def test_service_whitespace_only_query_raises_validation_error():
    service = CustomerService()
    with pytest.raises(ValidationError) as exc_info:
        service.search("   ")
    assert str(exc_info.value) == "Search query cannot be empty."


def test_service_none_query_raises_validation_error():
    service = CustomerService()
    with pytest.raises(ValidationError) as exc_info:
        service.search(None)  # type: ignore[arg-type]
    assert str(exc_info.value) == "Search query cannot be empty."


def test_service_custom_repository_injection():
    custom_repo = CustomerRepository(
        customers=[
            Customer(id="99", name="Special Agent", email="special@agent.com")
        ]
    )
    service = CustomerService(repository=custom_repo)
    results = service.search("special")
    assert len(results) == 1
    assert results[0].id == "99"


def test_service_performance_with_1000_records():
    records = [
        Customer(
            id=str(i),
            name=f"Customer Name {i}",
            email=f"customer{i}@example.com",
        )
        for i in range(1000)
    ]
    repo = CustomerRepository(customers=records)
    service = CustomerService(repository=repo)

    start_time = time.perf_counter()
    results = service.search("Name 99")
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    assert len(results) > 0
    assert elapsed_ms < 200, f"Search took {elapsed_ms:.2f} ms, expected < 200 ms"

