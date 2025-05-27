import logging
from pathlib import Path
from datetime import datetime
import os

# Ensure log directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Create a log file with daily rotation logic
log_file = LOG_DIR / "app.log"

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def cleanup_old_logs(days_to_keep=7):
    """Remove log files older than X days."""
    cutoff = datetime.now().timestamp() - (days_to_keep * 86400)
    for file in LOG_DIR.iterdir():
        if file.is_file() and file.suffix == ".log" and file.stat().st_mtime < cutoff:
            try:
                file.unlink()
                logger.info(f"Deleted old log: {file.name}")
            except Exception as e:
                logger.error(f"Failed to delete {file.name}: {e}")
