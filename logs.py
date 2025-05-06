import logging
import os
from datetime import datetime

# crreates a directory for the logs if it does not exist
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)

# creates a log file with the current date and time
log_filename = datetime.now().strftime("log_%d-%m-%Y_%H-%M-%S.log") # filename: DMY - HMS
log_path = os.path.join(log_dir, log_filename)

# config of logging module
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S" # message prefix: DMY - HMS
)

# ---------------- Functions

def new_info(message:str) -> None:
    """
    Creates a new info in the current log
    
    Args:
        message (str): The info message displayed in the log
    """

    if isinstance(message, str):
        logging.info(message)
    else:
        print("Logging Error: wrong Type") # debug

def new_error(message:str) -> None:
    """
    Creates a new error in the current log
    
    Args:
        message (str): The error message displayed in the log
    """

    if isinstance(message, str):  
        logging.error(message)
    else:
        print("Logging Error: wrong Type") # debug

def new_debug(message:str) -> None: # currently not useable since level is set to INFO
    """
    Creates a new debug in the current log
    
    Args:
        message (str): The debug message displayed in the log
    """

    if isinstance(message, str):  
        logging.debug(message)
    else:
        print("Logging Error: wrong Type") # debug