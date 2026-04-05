
import logging
import os

def setup_logger(log_file='data_transfer.log'):
    os.makedirs('logs', exist_ok=True)
    log_path = os.path.join('logs', log_file)

    logger = logging.getLogger('DataTransferLogger')
    logger.setLevel(logging.INFO)

    
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
