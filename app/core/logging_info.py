import logging
from logging.config import dictConfig
import os


def configure_logger():
    """Configures the root Python logger for the FastAPI application."""

    # Ensure the logs directory exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_config = {
        "version": 1,
        "disable_existing_loggers": False, # Important for Uvicorn
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s - %(name)s - %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s',
                "use_colors": None,
            },
        },
        "handlers": {
            # Console Handler (for real-time viewing)
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            # File Handler (for persistent logs)
            "file": {
                "formatter": "default",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(log_dir, "app.log"),
                "maxBytes": 1024 * 1024 * 5,  # 5 MB
                "backupCount": 5,
            },
            # Access Log File Handler (for persistent HTTP access logs)
            "access_file": {
                "formatter": "access",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(log_dir, "access.log"),
                "maxBytes": 1024 * 1024 * 5,  # 5 MB
                "backupCount": 5,
            },
        },
        "loggers": {
            # Application-specific logger
            "app": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            # Uvicorn Access Logger (for HTTP requests)
            "uvicorn.access": {
                "handlers": ["console", "access_file"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {
            "level": "WARNING", # Set root logger to a high level to minimize noise
            "handlers": ["console"],
        },
    }
    
    dictConfig(log_config)

    # Return a specific logger instance for easy use in other modules
    return logging.getLogger("app")

# Initialize the configuration and get the main logger instance
app_logger = configure_logger()