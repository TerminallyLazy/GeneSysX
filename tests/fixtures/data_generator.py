# tests/fixtures/data_generator.py

import random
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

num_sequences = 5
sequence_length = 50

def generate_random_rna_sequence(length):
    return ''.join(random.choice('AUGC') for _ in range(length))

sequences = [SeqRecord(Seq(generate_random_rna_sequence(sequence_length)), id=f"RNA_{i+1}") for i in range(num_sequences)]

output_file = "tests/fixtures/random_rna.fasta"

with open(output_file, "w") as f:
    SeqIO.write(sequences, f, "fasta")

print(f"Random RNA FASTA file '{output_file}' has been generated with {num_sequences} sequences of length {sequence_length}.")
