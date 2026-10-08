from src.models import Customer
from src.repository import CustomerRepository


def test_repository_default_seed_data():
    repo = CustomerRepository()
    customers = repo.get_all()
    assert len(customers) >= 8
    assert all(isinstance(c, Customer) for c in customers)


def test_repository_custom_seed_data():
    custom_customers = [
        Customer(id="101", name="Custom User", email="custom@example.com")
    ]
    repo = CustomerRepository(customers=custom_customers)
    assert repo.get_all() == custom_customers


def test_search_partial_match_by_name():
    repo = CustomerRepository()
    results = repo.search_by_text("al")
    names = [c.name for c in results]
    assert "Alice Wonderland" in names
    assert "Alex Johnson" in names


def test_search_partial_match_by_email():
    repo = CustomerRepository()
    results = repo.search_by_text("gmail")
    emails = [c.email for c in results]
    assert "johnny@gmail.com" in emails
    assert "alex@gmail.com" in emails


def test_search_case_insensitivity():
    repo = CustomerRepository()
    results = repo.search_by_text("DOE")
    names = [c.name for c in results]
    assert "John Doe" in names
    assert "Jane Doe" in names


def test_search_with_leading_and_trailing_whitespace():
    repo = CustomerRepository()
    results = repo.search_by_text("  john  ")
    names = [c.name for c in results]
    assert "John Doe" in names
    assert "Johnny Smith" in names


def test_search_no_matches_returns_empty_list():
    repo = CustomerRepository()
    results = repo.search_by_text("99999")
    assert results == []


def test_search_empty_or_whitespace_returns_empty_list():
    repo = CustomerRepository()
    assert repo.search_by_text("") == []
    assert repo.search_by_text("   ") == []


def test_search_max_results_limit():
    large_dataset = [
        Customer(id=str(i), name=f"Test Customer {i}", email=f"test{i}@example.com")
        for i in range(100)
    ]
    repo = CustomerRepository(customers=large_dataset)
    results = repo.search_by_text("test")
    assert len(results) == 50


def test_find_by_query_alias():
    repo = CustomerRepository()
    assert repo.find_by_query("alice") == repo.search_by_text("alice")
