import argparse
import sys
from src.exceptions import ValidationError
from src.service import CustomerService


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for searching customers."""
    parser = argparse.ArgumentParser(
        description="Search customer records by name or email."
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="",
        help="Search query string (at least 2 characters).",
    )

    args = parser.parse_args(argv)

    service = CustomerService()
    try:
        results = service.search(args.query)
        if not results:
            print("No customers found.")
            return 0

        print(f"Found {len(results)} matching customer(s):")
        for customer in results:
            print(f"- ID: {customer.id}, Name: {customer.name}, Email: {customer.email}")
        return 0
    except ValidationError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
