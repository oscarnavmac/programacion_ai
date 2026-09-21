"""Read and summarize station measurements with bounded additional memory."""

from collections.abc import Iterable, Iterator, Generator
from contextlib import contextmanager
from math import isfinite
from pathlib import Path
from typing import TextIO

Measurement = tuple[str, float]


def parse_measurements(lines: Iterable[str]) -> Iterator[Measurement]:
    """Read station;value lines; ignore blank lines and report physical line numbers."""
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        parts = line.strip().split(";")
        if len(parts) != 2 or not parts[0].strip():
            raise ValueError(f"Line {line_number}: expected station;value")
        station, raw_value = parts
        try:
            value = float(raw_value)
        except ValueError as error:
            raise ValueError(f"Line {line_number}: invalid number") from error
        if not isfinite(value):
            raise ValueError(f"Line {line_number}: value must be finite")
        yield station.strip(), value


def select_measurements(
    measurements: Iterable[Measurement], minimum: float
) -> Iterator[Measurement]:
    for station, value in measurements:
        if value >= minimum:
            yield station, value


def summarize_measurements(
    measurements: Iterable[Measurement],
) -> tuple[int, float | None]:
    count = 0
    total = 0.0
    for _, value in measurements:
        count += 1
        total += value
    return count, total / count if count else None


@contextmanager
def open_measurements(path: Path) -> Generator[Iterator[Measurement], None, None]:
    """Keep the file open only inside the caller's with block."""
    with path.open(encoding="utf-8") as file:
        yield parse_measurements(file)


def write_sample(file: TextIO, repetitions: int) -> None:
    """Write fixed records incrementally; do not allocate the complete dataset."""
    if repetitions < 0:
        raise ValueError("repetitions must be nonnegative")
    for _ in range(repetitions):
        file.write("north;18.0\nsouth;27.0\nwest;32.0\nnorth;23.0\n")
