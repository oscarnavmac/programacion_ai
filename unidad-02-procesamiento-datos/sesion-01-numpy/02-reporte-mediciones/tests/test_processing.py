import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from measurements.processing import (
    ROOM_NAMES,
    load_readings,
    select_complete_rows,
    summarize,
)

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR.parent / "datos"


def test_reference_summary_preserves_room_order():
    readings = load_readings(DATA_DIR / "readings.csv")
    report = summarize(readings)
    assert tuple(report) == ROOM_NAMES
    np.testing.assert_allclose(
        [room["mean_c"] for room in report.values()], [25.5, 27.5, 23.5]
    )
    assert report["storage_room"] == {"mean_c": 23.5, "min_c": 20.0, "max_c": 27.0}


def test_filter_rejects_whole_rows_and_does_not_alias_input():
    readings = load_readings(DATA_DIR / "readings_quality.csv")
    original = readings.copy()
    selected, rejected = select_complete_rows(readings)
    assert rejected == 2
    np.testing.assert_array_equal(selected, [[22, 24, 20], [24, 26, 22]])
    selected[0, 0] = -100
    np.testing.assert_array_equal(readings, original)


@pytest.mark.parametrize(
    "values", [np.array([1.0, 2.0, 3.0]), np.ones((2, 2)), np.empty((0, 3))]
)
def test_invalid_shapes(values):
    with pytest.raises(ValueError):
        select_complete_rows(values)
    with pytest.raises(ValueError):
        summarize(values)


def test_no_complete_rows_and_nonfinite_summary():
    readings = np.array([[np.nan, 20.0, 21.0], [20.0, np.inf, 22.0]])
    with pytest.raises(ValueError, match="No complete"):
        select_complete_rows(readings)
    with pytest.raises(ValueError, match="finite"):
        summarize(readings)


def test_single_row_keeps_two_dimensions(tmp_path):
    path = tmp_path / "single.csv"
    path.write_text(",".join(ROOM_NAMES) + "\n22,24,20\n")
    readings = load_readings(path)
    assert readings.shape == (1, 3)
    assert summarize(readings)["north_room"]["mean_c"] == 22.0


@pytest.mark.parametrize(
    "body",
    [
        "south_room,north_room,storage_room\n24,22,20\n",
        ",".join(ROOM_NAMES) + "\n",
        ",".join(ROOM_NAMES) + "\n22,24\n",
        ",".join(ROOM_NAMES) + "\n22,bad,20\n",
    ],
)
def test_invalid_csv_is_rejected(tmp_path, body):
    path = tmp_path / "invalid.csv"
    path.write_text(body)
    with pytest.raises(ValueError):
        load_readings(path)


def test_cli_roundtrip_from_another_directory(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_DIR / "main.py"),
            str(DATA_DIR / "readings_quality.csv"),
            "--output-dir",
            str(tmp_path / "report"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    assert (report["rows_read"], report["rows_used"], report["rows_rejected"]) == (
        4,
        2,
        2,
    )
    assert report["rooms"]["north_room"]["mean_c"] == 23.0
    output = tmp_path / "report"
    assert json.loads((output / "report.json").read_text()) == report
    np.testing.assert_array_equal(
        np.load(output / "complete_readings.npy", allow_pickle=False),
        [[22, 24, 20], [24, 26, 22]],
    )
    assert "rejected 2" in result.stderr


def test_cli_failure_does_not_create_outputs(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_DIR / "main.py"),
            str(tmp_path / "missing.csv"),
            "--output-dir",
            str(tmp_path / "report"),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert result.stdout == ""
    assert not (tmp_path / "report").exists()
