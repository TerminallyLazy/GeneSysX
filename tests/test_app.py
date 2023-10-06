from Bio import SeqIO

records = list(SeqIO.parse("tests/fixtures/msa.fasta", "fasta"))
print(records[2].id)
print(records[2].seq) 