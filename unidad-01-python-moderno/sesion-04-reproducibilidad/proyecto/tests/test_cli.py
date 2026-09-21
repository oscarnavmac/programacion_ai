import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "main.py"), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_result_and_logs_are_separate():
    result = run_cli("data/readings.jsonl")
    assert result.returncode == 0
    assert json.loads(result.stdout) == {
        "count": 3,
        "rejected": 1,
        "average_temperature": 22.0,
    }
    assert "WARNING" in result.stderr
    assert "DEBUG" not in result.stderr
    assert result.stderr.count("Report complete") == 1


def test_file_has_debug_even_when_console_filters_it(tmp_path: Path):
    log_file = tmp_path / "logs" / "app.log"
    result = run_cli(
        "data/readings.jsonl", "--log-level", "ERROR", "--log-file", str(log_file)
    )
    assert result.returncode == 0
    assert result.stderr == ""
    text = log_file.read_text(encoding="utf-8")
    assert "DEBUG" in text
    assert "WARNING" in text
    assert "readings.processing" in text


def test_invalid_input_fails_without_a_report():
    result = run_cli("data/invalid.jsonl")
    assert result.returncode == 1
    assert result.stdout == ""
    assert "Traceback" in result.stderr
    assert "no valid readings" in result.stderr


def test_missing_input_fails():
    result = run_cli("data/does-not-exist.jsonl")
    assert result.returncode == 1
    assert "FileNotFoundError" in result.stderr


def test_invalid_argument_is_reported():
    result = run_cli("data/readings.jsonl", "--log-level", "VERBOSE")
    assert result.returncode == 2


def test_import_does_not_run_the_application():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import main; import logging; assert not logging.getLogger().handlers",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == result.stderr == ""
