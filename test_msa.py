import os
from io import StringIO
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
            # Test with file path
            result = multiple_sequence_alignment(file_path)
            print(f"Alignment result (file path):\n{result[:500]}...")  # Print first 500 characters of the result

            # Test with StringIO object
            with open(file_path, 'r') as f:
                content = f.read()
            stringio_obj = StringIO(content)
            result_stringio = multiple_sequence_alignment(stringio_obj)
            print(f"Alignment result (StringIO):\n{result_stringio[:500]}...")  # Print first 500 characters of the result

            # Compare results
            if result == result_stringio:
                print("File path and StringIO results match.")
            else:
                print("Warning: File path and StringIO results do not match.")

        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_msa()
