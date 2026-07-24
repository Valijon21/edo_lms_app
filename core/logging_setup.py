import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

class ColoredFormatter(logging.Formatter):
    """Custom formatter to add ANSI colors to log levels in console."""
    # ANSI escape sequences for colors
    GREY = "\033[90m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BOLD_RED = "\033[1;31m"
    RESET = "\033[0m"

    COLORS = {
        logging.DEBUG: CYAN,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: BOLD_RED
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, self.RESET)
        
        # Store original values to restore them later (avoid contaminating other handlers)
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Apply coloring
        record.levelname = f"{log_color}{orig_levelname}{self.RESET}"
        if record.levelno >= logging.WARNING and isinstance(record.msg, str):
            record.msg = f"{log_color}{record.msg}{self.RESET}"
            
        result = super().format(record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        return result


def setup_logging(log_file_name="app.log", default_level=logging.INFO):
    """
    Sets up a professional logging system with console (colored) and rotating file output.
    
    Args:
        log_file_name (str): Name of the log file to write under the logs/ directory.
        default_level (int): Default logging level (logging.INFO, logging.DEBUG, etc.).
    """
    # Get project root (parent directory of 'core')
    base_dir = Path(__file__).resolve().parent.parent
    logs_dir = base_dir / "logs"
    
    # Create logs directory if it doesn't exist
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating logs directory '{logs_dir}': {e}")
        return

    log_file_path = logs_dir / log_file_name

    # Standard format for logs
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s:%(filename)s:%(lineno)d] - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Root logger setup
    root_logger = logging.getLogger()
    
    # If handlers are already configured (e.g. Django already ran it), clear them to avoid duplicate logs
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.setLevel(default_level)

    # 1. Console Handler (Colored)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(default_level)
    
    # Try enabling Windows virtual terminal processing for colors (Windows 10/11)
    if os.name == 'nt':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass
            
    console_formatter = ColoredFormatter(fmt=log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # 2. Rotating File Handler (Clean/Plain Text)
    try:
        # Rotate when file reaches 10MB, keep up to 5 historical log files
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(default_level)
        file_formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Error setting up file logging handler: {e}")

    # Set external libraries to be less noisy by default
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("yt_dlp").setLevel(logging.WARNING)
    logging.getLogger("youtube_transcript_api").setLevel(logging.WARNING)
    logging.getLogger("faster_whisper").setLevel(logging.WARNING)
    logging.getLogger("django").setLevel(logging.INFO)

    return root_logger
