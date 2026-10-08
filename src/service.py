from src.exceptions import ValidationError
from src.models import Customer
from src.repository import CustomerRepository


class CustomerService:
    """Service layer orchestrating customer search validation and execution."""

    VALID_STATUSES = {"ACTIVE", "INACTIVE", "PENDING"}

    def __init__(self, repository: CustomerRepository | None = None) -> None:
        self._repository = repository if repository is not None else CustomerRepository()

    def search(self, query: str, status: str | None = None) -> list[Customer]:
        """Validate query and status according to SPEC.md, then search customers."""
        if query is None:
            raise ValidationError("Search query cannot be empty.")

        trimmed_query = query.strip()

        if not trimmed_query:
            raise ValidationError("Search query cannot be empty.")

        if len(trimmed_query) < 2:
            raise ValidationError("Search query must be at least 2 characters long.")

        # Cambio para solucionar el Issue #1: Validación de estado según SPEC.md
        if status is not None and status.upper() not in self.VALID_STATUSES:
            raise ValidationError(
                f"Invalid status '{status}'. Must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )

        return self._repository.search_by_text(trimmed_query)
