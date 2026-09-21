"""Check lazy consumption, validation and resource cleanup using the standard library."""
import io
from pathlib import Path
import unittest
from unittest.mock import patch

from streaming import (
    open_measurements,
    parse_measurements,
    select_measurements,
    summarize_measurements,
    write_sample,
)


class StreamingTests(unittest.TestCase):
    def test_parser_preserves_physical_line_numbers(self):
        records = parse_measurements(["\n", " north ; 18.5\n", "south;bad\n"])
        self.assertEqual(next(records), ("north", 18.5))
        with self.assertRaisesRegex(ValueError, "Line 3: invalid number"):
            next(records)
        self.assertEqual(list(records), [])

    def test_invalid_records(self):
        for line in ("north;nan", "north;inf", "north;-inf", ";18", "north;18;20", "north"):
            with self.subTest(line=line), self.assertRaises(ValueError):
                list(parse_measurements([line]))

    def test_consumer_controls_reading(self):
        visited = []

        def source():
            for value in (18.0, 27.0, 32.0):
                visited.append(value)
                yield "north", value

        records = select_measurements(source(), 25.0)
        self.assertEqual(visited, [])
        self.assertEqual(next(records), ("north", 27.0))
        self.assertEqual(visited, [18.0, 27.0])
        self.assertEqual(list(records), [("north", 32.0)])
        self.assertEqual(list(records), [])

    def test_summary_and_sample(self):
        file = io.StringIO()
        write_sample(file, 3)
        records = list(parse_measurements(file.getvalue().splitlines()))
        self.assertEqual(len(records), 12)
        self.assertEqual(summarize_measurements(records), (12, 25.0))
        self.assertEqual(summarize_measurements(select_measurements(iter(records), 25)), (6, 29.5))
        self.assertEqual(summarize_measurements(iter([])), (0, None))
        with self.assertRaises(ValueError):
            write_sample(file, -1)

    def test_cleanup_on_complete_and_partial_consumption(self):
        for consume_all in (True, False):
            file = io.StringIO("north;18\nsouth;27\n")
            with self.subTest(consume_all=consume_all), patch.object(Path, "open", return_value=file):
                with open_measurements(Path("sample.txt")) as records:
                    if consume_all:
                        self.assertEqual(len(list(records)), 2)
                    else:
                        self.assertEqual(next(records), ("north", 18.0))
                    self.assertFalse(file.closed)
                self.assertTrue(file.closed)

    def test_cleanup_and_error_propagation(self):
        file = io.StringIO("north;18\nsouth;bad\n")
        with patch.object(Path, "open", return_value=file):
            with self.assertRaisesRegex(ValueError, "Line 2"):
                with open_measurements(Path("sample.txt")) as records:
                    list(records)
        self.assertTrue(file.closed)
        file = io.StringIO("north;18\n")
        with patch.object(Path, "open", return_value=file):
            with self.assertRaisesRegex(RuntimeError, "Consumer failed"):
                with open_measurements(Path("sample.txt")):
                    raise RuntimeError("Consumer failed")
        self.assertTrue(file.closed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
