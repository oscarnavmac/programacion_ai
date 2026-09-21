"""Numerical operations shared by the CLI and notebook."""

import csv
from pathlib import Path

import numpy as np
import numpy.typing as npt

ROOM_NAMES = ("north_room", "south_room", "storage_room")
type FloatArray = npt.NDArray[np.float64]


def validate_shape(readings: FloatArray) -> None:
    if readings.ndim != 2 or readings.shape[1] != len(ROOM_NAMES):
        raise ValueError("Expected a 2D array with three room columns")
    if readings.shape[0] == 0:
        raise ValueError("Expected at least one reading")


def load_readings(path: Path) -> FloatArray:
    """Require the declared column order and a nonempty numeric body."""
    with path.open(encoding="utf-8", newline="") as source:
        header = next(csv.reader(source), [])
        if tuple(header) != ROOM_NAMES:
            raise ValueError(f"Expected CSV header: {','.join(ROOM_NAMES)}")
        if not source.read().strip():
            raise ValueError("Expected at least one reading")
    readings = np.loadtxt(path, delimiter=",", skiprows=1, dtype=np.float64, ndmin=2)
    validate_shape(readings)
    return readings


def select_complete_rows(readings: FloatArray) -> tuple[FloatArray, int]:
    """Return independent rows with finite values in every room."""
    validate_shape(readings)
    complete = np.isfinite(readings).all(axis=1)
    selected = readings[complete]
    rejected = int((~complete).sum())
    if selected.shape[0] == 0:
        raise ValueError("No complete readings remain")
    return selected, rejected


def summarize(readings: FloatArray) -> dict[str, dict[str, float]]:
    """Compute one summary per room across measurement rounds."""
    validate_shape(readings)
    if not np.isfinite(readings).all():
        raise ValueError("Summary requires finite readings")
    means = readings.mean(axis=0)
    minima = readings.min(axis=0)
    maxima = readings.max(axis=0)
    return {
        name: {
            "mean_c": float(means[index]),
            "min_c": float(minima[index]),
            "max_c": float(maxima[index]),
        }
        for index, name in enumerate(ROOM_NAMES)
    }
