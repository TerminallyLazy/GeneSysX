import logging
logging.basicConfig(level=logging.DEBUG)
from genesys.ai import run_conversation

question = 'What are the sequence IDs in the uploaded FASTA file?'
file_path = '/tmp/gradio/830786ed162059d66bc9bb17217ca8f87f118e506102ee5213a93c77ff64ee7e/sample.fasta'

print('Debug: Starting run_conversation')
result = run_conversation(question, file_path)
print(f'Debug: Result from run_conversation: {result}')
