# custom_logger.py
import logging
import os
from datetime import datetime

def setup_custom_logger():
    # Define log file path based on the current timestamp
    LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    logs_path = os.path.join(os.getcwd(), "logs")  # logs directory
    os.makedirs(logs_path, exist_ok=True)  # Create logs directory if not present

    LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

    # Set up logging configuration
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # Optional: Log a message to confirm logger setup
    logging.info("Logging has been set up successfully!")

    return logging.getLogger()  # Return the logger object
