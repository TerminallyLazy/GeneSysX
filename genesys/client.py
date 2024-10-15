import httpx as requests # httpx runs async while requests doesn't. 
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# TODO: Generate the random a


def upload_content_to_s3(presigned_url: str, content: str) -> int:
    with requests.Client(timeout=60) as client:
        http_response = client.put(presigned_url, content=content)

    if http_response.status_code == 200:
        logging.info("Successfully uploaded content to S3")
    else:
        logging.error(http_response.status_code)
        logging.error(f"Failed to upload content. HTTP Response Code: {http_response.status_code}")
    return http_response.status_code

def download_content_from_s3(presigned_url:str):
    with requests.Client(timeout=60) as client:
        http_response = client.get(presigned_url)

    if http_response.status_code == 200:
        logging.info("Successfully obtained s3 url from lambda.")
    else:
        logging.error(http_response.status_code)
        logging.error(f"Failed to Download content. HTTP Response Code: {http_response.status_code}")
    
    return http_response.content

def get_s3_upload_url(user_id:str="test_user", filename:str="test_file", data_file:str="Text") -> str:
    request_url = "https://omqjp5gczd.execute-api.us-east-1.amazonaws.com/TestStage"
    params = {
        "user_id": user_id,
        "token": "test_user_5124kaf",
        "filename": filename,
        "load_type": 'upload',
        "data_file": data_file
    }

    response = requests.get(request_url, params=params)
    logging.info(response)
    presigned_url = response.json()['upload_url']
    return presigned_url

def get_s3_download_url(user_id:str="test_user", filename:str="test_file", data_file:str="Text") -> tuple:
    request_url = "https://omqjp5gczd.execute-api.us-east-1.amazonaws.com/TestStage"
    params = {
        "user_id": user_id,
        "token": "test_user_5124kaf",
        "filename": filename,
        "load_type": 'download',
        "data_file": data_file
    }

    response = requests.get(request_url, params=params)
    logging.info(response)
    presigned_url = response.json()['upload_url']

    if data_file == "session-group":
        session_group_exists = response.json()['session_group_exists']
        return (presigned_url, session_group_exists)

    return (presigned_url)


def upload_s3(content:str, user_id:str="test_user", filename:str="test_file", data_file:str="Text"):
    url = get_s3_upload_url(user_id, filename, data_file)
    upload_content_to_s3(url, content)

def download_s3(user_id:str="test_user", filename:str="test_file", data_file:str="Text"):
    result = get_s3_download_url(user_id, filename, data_file)
    file_content = download_content_from_s3(result[0])
    return file_content


if __name__ == "__main__":
    logging.info("Testing")

    logging.info("Doing an upload")
    upload_content_to_s3(get_s3_upload_url(user_id="Charlie-Test"), "abcde")

    logging.info("Doing a Download")
    download_url, *_ = get_s3_download_url(user_id="Charlie-Test")
    download_content_from_s3(download_url)
    # download_content_from_s3()