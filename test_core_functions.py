import os
from app import process_file, answer_question, visualize_protein

def test_file_processing():
    print("Testing file processing...")
    test_file_path = "/home/ubuntu/GeneSysX/test_sequences.fasta"
    result = process_file(test_file_path)
    print(f"File processing result: {result}")

def test_qa():
    print("Testing Q&A functionality...")
    test_file_path = "/home/ubuntu/GeneSysX/test_sequences.fasta"
    question = "What are the sequence IDs in this file?"
    result = answer_question(question, test_file_path)
    print(f"Q&A result: {result}")

def test_protein_visualization():
    print("Testing protein visualization...")
    test_pdb_path = "/home/ubuntu/GeneSysX/sample.pdb"
    result = visualize_protein(test_pdb_path, "white", "cartoon", True)
    print(f"Protein visualization result: {result[:100]}...")  # Print first 100 characters

if __name__ == "__main__":
    test_file_processing()
    test_qa()
    test_protein_visualization()
