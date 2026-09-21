import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(level: str, log_file: Path | None = None) -> None:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    handlers: list[logging.Handler] = [console]

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=100_000, backupCount=2, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    logging.basicConfig(level=logging.DEBUG, handlers=handlers)
