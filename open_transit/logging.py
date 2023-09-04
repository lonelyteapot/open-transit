import contextlib
import logging
from datetime import datetime
from pathlib import Path

from rich.logging import RichHandler


def configure_logging():
    LOGS_DIR = Path("logs")
    now = datetime.now()

    logging.root.setLevel(logging.DEBUG)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    rich_formatter = logging.Formatter("%(message)s")
    rich_handler = RichHandler(show_time=False)
    rich_handler.setLevel(logging.INFO)
    rich_handler.setFormatter(rich_formatter)
    logging.root.addHandler(rich_handler)

    file_formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
    )
    file_handler = logging.FileHandler(
        filename=LOGS_DIR / f"open_transit_{now:%Y%m%d_%H%M%S}.log",
        mode="w",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logging.root.addHandler(file_handler)

    logging.debug("Logging configured")

    LOG_COUNT_TO_KEEP = 3
    logging.debug(f"Removing old log files, keeping up to {LOG_COUNT_TO_KEEP}")
    old_log_paths = list(LOGS_DIR.glob("open_transit_*.log"))
    old_log_paths.sort(key=lambda p: p.stem)
    old_log_paths = old_log_paths[:-LOG_COUNT_TO_KEEP]
    for old_log_path in old_log_paths:
        with contextlib.suppress(OSError):
            old_log_path.unlink()
