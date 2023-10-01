import httpx as requests # httpx runs async while requests doesn't. 
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def upload_content_to_s3(presigned_url:str, content:str) -> int:
    http_response = requests.put(presigned_url, data=content)

    
    # If successful, the response status code should be 200
    if http_response.status_code == 200:
        logging.info("Successfully uploaded content to S3")
        
    else:
        logging.error(http_response.status_code)
        logging.error(f"Failed to upload content. HTTP Response Code: {http_response.status_code}")
    
    return http_response.status_code

def get_s3_url(user_id:str="test_user", filename:str="test_file") -> str:
    request_url = "https://omqjp5gczd.execute-api.us-east-1.amazonaws.com/TestStage"
    params = {
        "user_id": user_id,
        "token": "test_user_5124kaf",
        "filename": filename
    }

    response = requests.get(request_url, params=params)
    logging.info(response)
    presigned_url = response.json()['upload_url']
    return presigned_url


if __name__ == "__main__":
    
    print("testing")
    upload_content_to_s3(get_s3_url(), "abcde")