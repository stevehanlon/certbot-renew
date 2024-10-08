#!/usr/bin/env python3

import requests
import sys
import os
import configparser
import logging
from logging.handlers import RotatingFileHandler


# Setup logging
log_file_path = "certs_logfile.log"  # Adjust the log file path as needed
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

log_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=4)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

logger.debug("Initialised")


# Load configuration from config.ini
config = configparser.ConfigParser()
config_filename = os.getenv('RENEW_CONFIG')
if config_filename:
    logger.debug(f"Config filename: {config_filename}")
    config.read(config_filename)
else:
    logger.debug(f"Reading default config.ini")
    config.read('config.ini')  

# Extract constants from the config file
DOMAIN = config.get('wordpress', 'domain')
USERNAME = config.get('wordpress', 'username')
APPLICATION_PASSWORD = config.get('wordpress', 'application_password')

logger.info(f"Uploading auth for {DOMAIN}")

def send_challenge(filename, content, use_https=True):
    protocol = 'https' if use_https else 'http'
    url = f"{protocol}://{DOMAIN}/wp-json/certbot/v1/challenge"
    
    payload = {
        'filename': filename,
        'content': content
    }

    try:
        # Attempt the request, ignoring SSL errors by setting verify=False
        logger.debug(f'REST endpoint: {url}')
        logger.debug(f'Payload: {payload}')
        response = requests.post(url, json=payload, auth=(USERNAME, APPLICATION_PASSWORD), verify=False)
        logger.debug(f'Response status code: {response.status_code}')
        if response.status_code == 200:
            logger.info("Challenge file updated successfully.")
        else:
            logger.error(f"Failed to update challenge file: {response.content.decode()}")
    except requests.exceptions.SSLError:
        logger.error("SSL error occurred, even after fallback.")

if __name__ == "__main__":
    # Use environment variables for Certbot challenge token and validation
    filename = os.getenv('CERTBOT_TOKEN')
    content = os.getenv('CERTBOT_VALIDATION')

    if not filename or not content:
        logger.error("Environment variables CERTBOT_TOKEN or CERTBOT_VALIDATION not set")
        sys.exit(1)

    # Call the function to send the challenge
    send_challenge(filename, content)

