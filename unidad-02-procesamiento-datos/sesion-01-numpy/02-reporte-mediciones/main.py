import argparse
import json
import logging
from pathlib import Path

import numpy as np

from measurements.processing import load_readings, select_complete_rows, summarize

logger = logging.getLogger(__name__)
PROJECT_DIR = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize room temperatures")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=PROJECT_DIR.parent / "datos" / "readings.csv",
    )
    parser.add_argument("--output-dir", type=Path, default=PROJECT_DIR / "outputs")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        readings = load_readings(args.input)
        selected, rejected = select_complete_rows(readings)
        report = {
            "rows_read": int(readings.shape[0]),
            "rows_used": int(selected.shape[0]),
            "rows_rejected": rejected,
            "rooms": summarize(selected),
        }
        report_text = json.dumps(report, indent=2, allow_nan=False)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        np.save(args.output_dir / "complete_readings.npy", selected, allow_pickle=False)
        (args.output_dir / "report.json").write_text(
            report_text + "\n", encoding="utf-8"
        )
    except (OSError, ValueError) as error:
        logger.error("Unable to generate report: %s", error)
        return 1
    logger.info("Used %s rows; rejected %s rows", selected.shape[0], rejected)
    print(report_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
