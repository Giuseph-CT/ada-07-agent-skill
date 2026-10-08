from src.models import Customer

DEFAULT_CUSTOMERS: list[Customer] = [
    Customer(id="1", name="John Doe", email="john.doe@example.com"),
    Customer(id="2", name="Johnny Smith", email="johnny@gmail.com"),
    Customer(id="3", name="Alice Wonderland", email="alice@example.com"),
    Customer(id="4", name="Alex Johnson", email="alex@gmail.com"),
    Customer(id="5", name="Jane Doe", email="jane.doe@example.com"),
    Customer(id="6", name="Bob Builder", email="bob@builder.com"),
    Customer(id="7", name="Diana Prince", email="diana@amazon.com"),
    Customer(id="8", name="Ana Garcia", email="ana@example.com"),
]


class CustomerRepository:
    """In-memory repository for customer records."""

    MAX_RESULTS = 50

    def __init__(self, customers: list[Customer] | None = None) -> None:
        self._customers: list[Customer] = (
            list(customers) if customers is not None else list(DEFAULT_CUSTOMERS)
        )

    def get_all(self) -> list[Customer]:
        """Return a copy of all customer records."""
        return list(self._customers)

    def search_by_text(self, query: str) -> list[Customer]:
        """Search customers by partial name or email (case-insensitive)."""
        normalized_query = query.strip().lower()
        if not normalized_query:
            return []

        results: list[Customer] = []
        for customer in self._customers:
            if (
                normalized_query in customer.name.lower()
                or normalized_query in customer.email.lower()
            ):
                results.append(customer)
                if len(results) >= self.MAX_RESULTS:
                    break

        return results

    def find_by_query(self, query: str) -> list[Customer]:
        """Find customers matching query; alias for search_by_text."""
        return self.search_by_text(query)
