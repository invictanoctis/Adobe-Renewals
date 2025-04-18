import logging
import os
from datetime import datetime


log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True) # creates the logs folder in the current directory

log_filename = datetime.now().strftime("log_%d-%m-%Y_%H-%M-%S.log") # file name: DMY - HMS
log_path = os.path.join(log_dir, log_filename)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", # message prefix: time - level - message
    datefmt="%d-%m-%Y %H:%M:%S" # message prefix: DMY - HMS
)

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

def new_debug(message:str) -> None: # !!! not useable right now since level is set to INFO
    """
    Creates a new debug in the current log
    
    Args:
        message (str): The debug message displayed in the log
    """

    if isinstance(message, str):  
        logging.debug(message)
    else:
        print("Logging Error: wrong Type") # debug