from Bio import SeqIO
def fasta_to_string(fasta_file):
    """
    Reads a .fasta file and returns the sequences as a single string.

    Args:
        fasta_file (str): The path to the .fasta file.

    Returns:
        str: A string containing all sequences concatenated together.
    """
    sequences = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences.append(str(record.seq))

    dnaSeq = "".join(sequences)
    
    return dnaSeq
