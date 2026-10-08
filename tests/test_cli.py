import subprocess
import sys
from src.cli import main


def test_cli_successful_search(capsys):
    exit_code = main(["john"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Found" in captured.out
    assert "John Doe" in captured.out
    assert "john.doe@example.com" in captured.out


def test_cli_no_results(capsys):
    exit_code = main(["xyz_nonexistent"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "No customers found." in captured.out


def test_cli_short_query_error(capsys):
    exit_code = main(["a"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: Search query must be at least 2 characters long." in captured.err


def test_cli_whitespace_query_error(capsys):
    exit_code = main(["   "])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: Search query cannot be empty." in captured.err


def test_cli_no_args_error(capsys):
    exit_code = main([])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: Search query cannot be empty." in captured.err


def test_cli_subprocess_invocation():
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "alice"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Alice Wonderland" in result.stdout


def test_cli_subprocess_invocation_validation_error():
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "a"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "Error: Search query must be at least 2 characters long." in result.stderr
