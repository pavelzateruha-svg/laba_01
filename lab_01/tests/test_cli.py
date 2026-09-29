import subprocess
import sys


def run_cli(args):
    return subprocess.run(
        [sys.executable, "-m", "toolkit"] + args,
        capture_output=True,
        text=True,
    )


def test_cli_calc_success():
    result = run_cli(["calc", "2 + 2"])
    assert result.returncode == 0
    assert result.stdout.strip() == "4"


def test_cli_calc_with_parentheses():
    result = run_cli(["calc", "(5) - 3"])
    assert result.returncode == 0
    assert result.stdout.strip() == "2"


def test_cli_calc_error_empty():
    result = run_cli(["calc", ""])
    assert result.returncode == 2
    assert len(result.stderr) > 0


def test_cli_calc_error_invalid():
    result = run_cli(["calc", "2 + a"])
    assert result.returncode == 2
    assert len(result.stderr) > 0


def test_cli_convert_success():
    result = run_cli(["convert", "100", "--from", "cm", "--to", "m"])
    assert result.returncode == 0
    assert "1" in result.stdout


def test_cli_convert_incompatible():
    result = run_cli(["convert", "1", "--from", "m", "--to", "kg"])
    assert result.returncode == 2
    assert len(result.stderr) > 0


def test_cli_help():
    result = run_cli(["--help"])
    assert result.returncode == 0
    assert "toolkit" in result.stdout.lower() or "usage" in result.stdout.lower()