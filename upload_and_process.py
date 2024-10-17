import gradio_client
import os

def upload_and_process_file(file_path):
    try:
        client = gradio_client.Client("http://127.0.0.1:7868")  # Use local URL since share=True is not set

        # Upload and process file
        with open(file_path, 'rb') as file:
            result = client.predict(
                file_path,  # name
                file,  # file
                api_name="/process_file"
            )
        print(f"Process file result: {result}")

        # Perform multiple sequence alignment
        question = "Perform a multiple sequence alignment"
        with open(file_path, 'rb') as file:
            result = client.predict(
                question,
                file_path,  # name
                file,  # file
                api_name="/answer_question"
            )
        print(f"Multiple sequence alignment result: {result}")
    except gradio_client.exceptions.AppError as e:
        print(f"Gradio API error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def test_multiple_files():
    test_files = [
        '/home/ubuntu/attachments/covid_sequences.fasta',
        '/home/ubuntu/GeneSysX/tests/fixtures/covid_sequences.fasta',
        '/home/ubuntu/GeneSysX/tests/fixtures/primer.fasta',
        '/home/ubuntu/GeneSysX/tests/fixtures/rand_gen.fasta'
    ]

    for file_path in test_files:
        print(f"\nTesting file: {file_path}")
        upload_and_process_file(file_path)

if __name__ == "__main__":
    test_multiple_files()
