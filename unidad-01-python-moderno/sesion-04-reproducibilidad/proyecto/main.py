import argparse
import logging
import sys
from pathlib import Path

from readings.logging_config import configure_logging
from readings.processing import summarize_file

logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize temperature readings.")
    parser.add_argument("input", type=Path, help="Path to a JSON Lines file")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Minimum console logging level",
    )
    parser.add_argument("--log-file", type=Path, help="Optional rotating log file")
    args = parser.parse_args()

    try:
        configure_logging(args.log_level, args.log_file)
    except OSError as error:
        print(f"Cannot configure logging: {error}", file=sys.stderr)
        return 1

    try:
        report = summarize_file(args.input)
    except (OSError, ValueError):
        logger.exception("Report could not be generated")
        return 1

    print(report.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
