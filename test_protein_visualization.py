import gradio as gr
from app import visualize_protein
import os
import tempfile

def test_visualize_protein():
    # Create a temporary file with sample PDB content
    sample_pdb_content = """ATOM      1  N   ALA A   1      -0.525   1.362   0.000  1.00  0.00           N
ATOM      2  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C
ATOM      3  C   ALA A   1       1.520   0.000   0.000  1.00  0.00           C
ATOM      4  O   ALA A   1       2.197   0.995   0.000  1.00  0.00           O
ATOM      5  CB  ALA A   1      -0.507  -0.785  -1.207  1.00  0.00           C
END
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as temp_file:
        temp_file.write(sample_pdb_content)
        temp_file_path = temp_file.name

    # Create a Gradio File object with the temporary file
    file = gr.File(value=temp_file_path)

    # Call visualize_protein with the file object
    result = visualize_protein(file, 'white', 'cartoon', True)

    print(f'Visualization result type: {type(result)}')
    print(f'Visualization result length: {len(result)}')
    print(f'Visualization result preview: {result[:500]}...')

    # Clean up the temporary file
    os.unlink(temp_file_path)

if __name__ == "__main__":
    test_visualize_protein()
