from gradio_client import Client
import base64
import os
import traceback
import tempfile
import requests

def upload_and_process_file(file_path):
    try:
        client = Client('https://250e359484d4dc5e0e.gradio.live')
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Gradio server: {str(e)}")
        return
    try:
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
            with open(file_path, 'rb') as original_file:
                temp_file.write(original_file.read())
            temp_file_path = temp_file.name

        result = client.predict(
            temp_file_path,  # Pass the temporary file path
            api_name='/process_file_wrapper'
        )
        print(result)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
    finally:
        if 'temp_file_path' in locals():
            os.unlink(temp_file_path)

def answer_question(file_path, question):
    try:
        client = Client('https://250e359484d4dc5e0e.gradio.live')
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Gradio server: {str(e)}")
        return
    try:
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
            with open(file_path, 'rb') as original_file:
                temp_file.write(original_file.read())
            temp_file_path = temp_file.name

        result = client.predict(
            temp_file_path,  # Pass the temporary file path
            question,
            api_name='/answer_question_wrapper'
        )
        print(result)
    except Exception as e:
        print(f"Error answering question: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
    finally:
        if 'temp_file_path' in locals():
            os.unlink(temp_file_path)

if __name__ == "__main__":
    file_path = "test_sequences.fasta"
    print("Processing file:")
    upload_and_process_file(file_path)

    print("\nAsking a question:")
    question = "What are the sequence IDs in the uploaded file?"
    answer_question(file_path, question)
