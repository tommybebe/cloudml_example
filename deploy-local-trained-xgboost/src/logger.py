import os
from dotenv import load_dotenv


load_dotenv()


def make_logger(name):
    if os.getenv('DEV_MODE') == 'dev':
        import logging
        logger = logging.getLogger(name)
        return logger.warning
    else:
        from google.cloud import logging
        log_client = logging.Client()
        logger = log_client.logger(name)
        return logger.log_text
