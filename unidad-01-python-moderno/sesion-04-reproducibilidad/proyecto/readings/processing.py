import logging
from pathlib import Path

from pydantic import ValidationError

from readings.models import Reading, Report

logger = logging.getLogger(__name__)


def summarize_file(path: Path) -> Report:
    count = 0
    rejected = 0
    average = 0.0
    logger.info("Reading input file: %s", path)

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                reading = Reading.model_validate_json(line)
            except ValidationError:
                rejected += 1
                logger.warning("Rejected record at line %d", line_number)
                continue

            count += 1
            # Weighted terms avoid overflowing a running sum of finite values.
            average = average * ((count - 1) / count) + reading.temperature / count
            logger.debug("Accepted record at line %d", line_number)

    if count == 0:
        raise ValueError("Input contains no valid readings")

    logger.info("Report complete: accepted=%d rejected=%d", count, rejected)
    return Report(count=count, rejected=rejected, average_temperature=average)
