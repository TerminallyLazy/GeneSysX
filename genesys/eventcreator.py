# Internal Python Modules
import json
from time import time
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# External Python Modules
import pandas as pd

# Library Modules
import genesys.client as client

def create_session(session_id: str, user_id) -> dict:
    """
    Create a new session structure with the given session_id.

    Args:
        session_id (str): Unique identifier for the session.

    Returns:
        dict: Initialized session structure.
    """
    
    new_session = {
        "sessionId": session_id,
        "sessionData": []
    }
    session_group = "session-group"

    result = client.get_s3_download_url(user_id=user_id, data_file=session_group)
    session_group_exists = result[1]
    print("Session Group Exists:", session_group_exists)

    if not session_group_exists:
        json_list = []
        json_list.append(new_session)
        json_data = json.dumps(json_list)
    else:
        logging.info("Session Group Exists")
        logging.info("Downloading Old Session Group")
        content = str(client.download_s3(user_id, data_file=session_group))
        content = content[2:][:-1]
        logging.info("Loading old session group as json")
        json_data = json.loads(content)
        logging.info('Creating Session Data')
        json_data.append(new_session)
        json_data = json.dumps(json_data)
    logging.info("Uploading Session Data to S3")
    client.upload_s3(content=json_data, user_id=user_id, data_file=session_group)
    
    return new_session

def create_csv_metadata(df: pd.DataFrame) -> dict:
    """
    Obtain metadata from a CSV file.

    Args:
        csv_path (str): Path to the CSV file.
        sample_values_count (int, optional): Number of unique sample values to return for each column. 
                                             Defaults to 5.

    Returns:
        dict: Metadata containing column names, data types, and possible values.
    """
    samples = 5 
     
    metadata = {
        "columns": []
    }

    for column in df.columns:
            col_data = {
                "Name": column,
                "Type": str(df[column].dtype)
            }
            unique_values = df[column].dropna().unique()

            if len(unique_values) < samples:
                col_data["possibleValues"] = unique_values.tolist()
            else:
                col_data["possibleValues"] = unique_values[:samples].tolist()

            metadata["columns"].append(col_data)

    return metadata


def create_csv_event(user_id:str, session: dict, filename: str, df: pd.DataFrame) -> None:
    """
    Add a CSV event to the session data.

    Args:
        session (dict): The session to which the CSV event should be added.
        filename (str): The filename of the CSV file.
        unix_time (str): The unix timestamp associated with the event.
        metadata (dict): The metadata for the CSV, including column details.

    Returns:
        None: The function updates the session in-place.
    """
    
    metadata = create_csv_metadata(df)

    unix_time = str(int(time()))

    csv_event = {
        "event": "csv",
        "detail": {
            "fn": filename,
            "uTime": unix_time,
            "meta": metadata
        }
    }

    session["sessionData"].append(csv_event)

    update_session(user_id, session)


def create_message_event(user_id:str, session: dict, message:str) -> None:
    """
    Add a message event to the session data.

    Args:
        session (dict): The session to which the message event should be added.
        unix_time (str): The unix timestamp associated with the event.
        message (str): The message text.

    Returns:
        None: The function updates the session in-place.
    """
    unix_time = str(int(time()))

    
    message_event = {
        "event": "message",
        "detail": {
            "text": message,
            "uTime": unix_time
        }
    }

    session["sessionData"].append(message_event)

    update_session(user_id, session)

def create_response_event(user_id:str, session: dict, response: str, type:str="text", language:str="None") -> None:
    """
    Add a response event from the chatbot to the session data.

    Args:
        session (dict): The session to which the response event should be added.
        unix_time (str): The unix timestamp associated with the event.
        response (str): The response text from the chatbot.

    Returns:
        None: The function updates the session in-place.
    """
    unix_time = str(int(time()))
    
    response_event = {
        "event": "response",
        "detail": {
            "text": response,
            "type": type,
            "language": language,
            "uTime": unix_time
        }
    }

    session["sessionData"].append(response_event)

    update_session(user_id, session)

def display_csv_event(user_id:str, session: dict, filename: str):
    unix_time = str(int(time()))

    csv_event = {
        "event": "csv",
        "detail": {
            "fn": filename,
            "uTime": unix_time
        }
    }
    session["sessionData"].append(csv_event)

    update_session(user_id, session)



def create_pdb_event(user_id:str, session: dict, filename: str, action: str) -> None:
    """
    Add a pdb event to the session data.

    Args:
        session (dict): The session to which the pdb event should be added.
        unix_time (str): The unix timestamp associated with the event.
        filename (str): The filename of the pdb file.
        action (str): The action associated with the pdb file, e.g., "Visualize".

    Returns:
        None: The function updates the session in-place.
    """
    unix_time = str(int(time()))
    
    pdb_event = {
        "event": "pdb",
        "detail": {
            "fn": filename,
            "uTime": unix_time,
            "action": action
        }
    }

    session["sessionData"].append(pdb_event)

    update_session(user_id, session)

def create_fasta_event(user_id:str, session:dict, filename:str, action:str) -> None:
    """
    Add a FASTA event to the session data.

    Args:
        session (dict): The session to which the FASTA event should be added.
        unix_time (str): The unix timestamp associated with the event.
        filename (str): The filename of the FASTA file.
        action (str): The action associated with the FASTA file, e.g., "Analyze", "Visualize"

    Returns:
        None: The function updates the session in-place.
    """
    # TODO: Incorporate the uploading of the file into this function as well. 

    unix_time = str(int(time()))
    
    fasta_event = {
        "event": "fasta",
        "detail": {
            "fn": filename,
            "uTime": unix_time,
            "action": action
        }
    }
    session["sessionData"].append(fasta_event)

    update_session(user_id, session)


def update_session(user_id:str, updated_session:dict):
    session_group = "session-group"
    session_id = updated_session['sessionId']

    json_list = get_session_group(user_id)
    old_session = get_session_dict(user_id, session_id, json_list)
    json_list.remove(old_session)
    
    json_list.append(updated_session)
    json_data = json.dumps(json_list)
    client.upload_s3(content=json_data, user_id=user_id, data_file=session_group)

def get_session_dict(user_id:str, session_id:str, json_list:list) -> dict:
    for sesh in json_list:
        if sesh['sessionId'] == session_id:
            return sesh
        
def get_session_group(user_id:str) -> list:
    session_group = "session-group"
    content = str(client.download_s3(user_id, data_file=session_group))[2:][:-1]
    json_list = json.loads(content)
    return json_list
        
def list_session_ids(user_id:str) -> list:
    json_list = get_session_group(user_id)
    session_ids = []
    for sesh in json_list:
        session_ids.append(sesh['sessionId'])
    return session_ids
    
if __name__ == "__main__":
    session_id = "Test-Session"
    user_id = "Charlie-Test"
    session = create_session(session_id, user_id)
    data = {
    'Name': ['John', 'Jane', 'Tom', 'Alice'],
    'Age': [28, 24, 22, 27],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }

    df = pd.DataFrame(data)
    
    create_csv_event(user_id, session, "test.csv", df)
    

    
