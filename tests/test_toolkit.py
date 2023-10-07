import pytest

from genesys import DNAToolKit

def test_count_nucleotides():
    print("Running test_count_nucleotides()...")
    ret = DNAToolKit.count_occurences("tests/fixtures/msa.fasta")
    print(ret)

def test_sequence_type():
    print("Running test_sequence_type()...")
    ret = DNAToolKit.sequence_type("tests/fixtures/msa.fasta")
    print(ret)

def test_transcribe_rna():
    with pytest.raises(ValueError):
        DNAToolKit.transcription("tests/fixtures/msa.fasta")

def test_complementary():
    print("Running test_complementary()...")
    ret = DNAToolKit.complementary("tests/fixtures/sequence.fasta")
    print(ret)