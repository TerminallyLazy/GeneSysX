import os
import logging
from pathlib import Path
import re

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# TODO: Generate the random a

TEMP_STORAGE_DIR = Path("/tmp/genesysx_storage")

def ensure_temp_dir():
    TEMP_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def upload_content_to_local(filename: str, content: str) -> bool:
    ensure_temp_dir()
    file_path = TEMP_STORAGE_DIR / filename
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        logging.info(f"Successfully uploaded content to local storage: {file_path}")
        return True
    except IOError as e:
        logging.error(f"Failed to upload content to local storage: {str(e)}")
        return False

def download_content_from_local(filename: str) -> str:
    file_path = TEMP_STORAGE_DIR / filename
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        logging.info(f"Successfully downloaded content from local storage: {file_path}")
        return content
    except IOError as e:
        logging.error(f"Failed to download content from local storage: {str(e)}")
        return ""

def sanitize_filename(filename: str) -> str:
    # Remove any non-alphanumeric characters except for underscores and hyphens
    return re.sub(r'[^\w\-_\.]', '_', filename)

def upload_s3(content:str, user_id:str="test_user", filename:str="test_file", data_file:str="Text"):
    ensure_temp_dir()
    filename = Path(filename).name  # Extract only the filename, not the full path
    sanitized_filename = sanitize_filename(filename)
    full_filename = f"{user_id}_{sanitized_filename}_{data_file}"
    return upload_content_to_local(full_filename, content)

def download_s3(user_id:str="test_user", filename:str="test_file", data_file:str="Text"):
    sanitized_filename = sanitize_filename(filename)
    full_filename = f"{user_id}_{sanitized_filename}_{data_file}"
    return download_content_from_local(full_filename)

if __name__ == "__main__":
    logging.info("Testing")

    logging.info("Doing an upload")
    upload_s3("abcde", user_id="Charlie-Test", filename="test_file", data_file="Text")

    logging.info("Doing a Download")
    content = download_s3(user_id="Charlie-Test", filename="test_file", data_file="Text")
    logging.info(f"Downloaded content: {content}")
