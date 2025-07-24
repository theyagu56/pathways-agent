import logging
import os
from datetime import datetime
from pathlib import Path
import sys

class LoggerConfig:
    def __init__(self, app_name="pathways-ai", log_dir="logs"):
        self.app_name = app_name
        self.log_dir = log_dir
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging with file and console handlers"""
        # Create logs directory if it doesn't exist
        Path(self.log_dir).mkdir(exist_ok=True)
        
        # Generate timestamp for log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{self.app_name}_{timestamp}.log"
        log_filepath = os.path.join(self.log_dir, log_filename)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Create handlers
        # File handler for all levels
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler for INFO and above
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Error file handler for errors only
        error_filename = f"{self.app_name}_errors_{timestamp}.log"
        error_filepath = os.path.join(self.log_dir, error_filename)
        error_handler = logging.FileHandler(error_filepath, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Add handlers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(error_handler)
        
        # Log startup information
        logger = logging.getLogger(__name__)
        logger.info(f"Logging initialized - File: {log_filepath}")
        logger.info(f"Error logging - File: {error_filepath}")
        logger.info(f"Environment: {'Azure' if os.getenv('AZURE_ENVIRONMENT') else 'Local'}")
        
        return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name"""
    return logging.getLogger(name)

# Initialize logging configuration
logger_config = LoggerConfig() 