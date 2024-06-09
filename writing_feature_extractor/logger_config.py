import logging
import sys
from logging.handlers import RotatingFileHandler

# Create a logger for your module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
file_handler = RotatingFileHandler(
    "llm_feature_extractor.log", maxBytes=1024 * 1024, backupCount=1
)  # 1MB per file, keep 1 backup
stream_handler = logging.StreamHandler(sys.stdout)

# Set logging levels for handlers
file_handler.setLevel(logging.INFO)
stream_handler.setLevel(logging.INFO)

# Create formatters
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
stream_formatter = logging.Formatter("%(levelname)s - %(message)s")

# Add formatters to handlers
file_handler.setFormatter(file_formatter)
stream_handler.setFormatter(stream_formatter)

# Add handlers to the root logger (used by libraries and your module)
root_logger = logging.getLogger()
root_logger.setLevel(logging.ERROR)
root_logger.addHandler(file_handler)
root_logger.addHandler(stream_handler)
