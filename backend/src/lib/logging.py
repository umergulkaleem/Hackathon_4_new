import logging
import sys
from typing import Optional

def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file to write logs to

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("markdown_embeddings")

    # Avoid adding multiple handlers if logger already configured
    if logger.handlers:
        return logger

    # Set logging level
    logger.setLevel(getattr(logging, level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optionally add file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Default logger instance
logger = setup_logging()