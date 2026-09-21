import logging
from pathlib import Path

import pytest
from pydantic import ValidationError

from readings.models import Reading
from readings.processing import summarize_file


def test_report_skips_invalid_records(tmp_path: Path, caplog: pytest.LogCaptureFixture):
    path = tmp_path / "readings.jsonl"
    path.write_text(
        '{"station":"north","temperature":20}\n'
        "not json\n"
        '{"station":"south","temperature":24}\n',
        encoding="utf-8",
    )
    with caplog.at_level(logging.WARNING, logger="readings.processing"):
        report = summarize_file(path)
    assert report.count == 2
    assert report.rejected == 1
    assert report.average_temperature == pytest.approx(22.0)
    assert "Rejected record at line 2" in caplog.text
    assert "not json" not in caplog.text


@pytest.mark.parametrize("content", ["", "\n", '{"station":"north"}\n'])
def test_no_valid_readings_fails(tmp_path: Path, content: str):
    path = tmp_path / "readings.jsonl"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError, match="no valid readings"):
        summarize_file(path)


def test_missing_file_fails(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        summarize_file(tmp_path / "missing.jsonl")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_non_finite_temperature_is_rejected(value: float):
    with pytest.raises(ValidationError):
        Reading(station="north", temperature=value)


def test_numeric_text_is_converted():
    reading = Reading.model_validate({"station": " north ", "temperature": "21.5"})
    assert reading.station == "north"
    assert reading.temperature == 21.5
