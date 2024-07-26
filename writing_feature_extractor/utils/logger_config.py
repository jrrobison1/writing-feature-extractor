import logging
import sys
from logging.handlers import RotatingFileHandler
import traceback


def get_logger(module_name: str) -> logging.Logger:
    try:
        logger = logging.getLogger(module_name)
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Disable propagation to the root logger

        file_handler = RotatingFileHandler(
            "writing_feature_extractor.log", maxBytes=1024 * 1024, backupCount=1
        )  # 1MB per file, keep 1 backup
        stream_handler = logging.StreamHandler(sys.stdout)

        file_handler.setLevel(logging.DEBUG)
        stream_handler.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_formatter = logging.Formatter("%(levelname)s - %(message)s")

        file_handler.setFormatter(file_formatter)
        stream_handler.setFormatter(stream_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.ERROR)
        root_logger.addHandler(file_handler)

        return logger
    except Exception as e:
        print(f"Error setting up logger: {e}")
        traceback.print_exc()
