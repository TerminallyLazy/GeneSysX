import os
from genesys.tools.sequence import multiple_sequence_alignment

def test_msa():
    test_files = [
        '/home/ubuntu/attachments/covid_sequences.fasta',
        '/home/ubuntu/GeneSysX/tests/fixtures/covid_sequences.fasta',
        '/home/ubuntu/GeneSysX/tests/fixtures/primer.fasta',
        '/home/ubuntu/GeneSysX/tests/fixtures/rand_gen.fasta'
    ]

    for file_path in test_files:
        print(f"\nTesting file: {file_path}")
        try:
            result = multiple_sequence_alignment(file_path)
            print(f"Alignment result:\n{result[:500]}...")  # Print first 500 characters of the result
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_msa()
