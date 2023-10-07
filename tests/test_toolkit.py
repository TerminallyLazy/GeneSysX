import pytest
import os
from genesys.DNAToolKit import count_occurences, sequence_type, transcription

# Define the path to the test FASTA files
TEST_DATA_DIR = "tests/fixtures"

def test_sequence_type_DNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "sequence.fasta")
    result = sequence_type(fasta_file)
    expected_result = "DNA"
    assert result == expected_result

def test_sequence_type_PROTEIN():
    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    result = sequence_type(fasta_file)
    expected_result = "Protein"
    assert result == expected_result

def test_count_occurences_PROTEIN():
    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    result = count_occurences(fasta_file)
    expected_result = {
        'QJF75467.1': {'L': 108, 'S': 99, 'V': 97, 'T': 97, 'N': 87, 'G': 82, 'A': 79, 'F': 77, 'I': 76, 'Q': 62, 'D': 62, 'K': 61, 'P': 58, 'Y': 54, 'E': 48, 'R': 42, 'C': 40, 'H': 17, 'M': 14, 'W': 12, 'B': 1},
        'QII57278.1': {'L': 109, 'S': 99, 'V': 97, 'T': 97, 'N': 88, 'G': 82, 'A': 79, 'F': 76, 'I': 76, 'Q': 62, 'D': 62, 'K': 61, 'P': 58, 'Y': 54, 'E': 48, 'R': 42, 'C': 40, 'H': 17, 'M': 14, 'W': 12},
        'YP_009724390.1': {'L': 108, 'S': 99, 'V': 97, 'T': 97, 'N': 88, 'G': 82, 'A': 79, 'F': 77, 'I': 76, 'Q': 62, 'D': 62, 'K': 61, 'P': 58, 'Y': 54, 'E': 48, 'R': 42, 'C': 40, 'H': 17, 'M': 14, 'W': 12},
        'QJF77846.1': {'L': 108, 'S': 99, 'V': 97, 'T': 97, 'N': 88, 'G': 82, 'A': 79, 'F': 77, 'I': 76, 'Q': 62, 'D': 62, 'K': 61, 'P': 58, 'Y': 53, 'E': 48, 'R': 42, 'C': 40, 'H': 18, 'M': 14, 'W': 12},
        'QIZ16509.1': {'L': 108, 'S': 99, 'T': 97, 'V': 96, 'N': 88, 'G': 82, 'A': 79, 'F': 77, 'I': 77, 'Q': 62, 'D': 62, 'K': 61, 'P': 58, 'Y': 54, 'E': 48, 'R': 42, 'C': 40, 'H': 17, 'M': 14, 'W': 12}
    }
    assert result == expected_result

def test_count_occurences_DNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "sequence.fasta")
    result = count_occurences(fasta_file)
    expected_result = {
        'MJ712037.1': {'A': 182, 'T': 155, 'G': 119, 'C': 103},
        'LJ712037.1': {'T': 93, 'A': 92, 'G': 58, 'C': 43},
        'FK712037.1': {'A': 129, 'T': 92, 'C': 77, 'G': 75}
    }
    assert result == expected_result

def test_transcription_DNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "sequence.fasta")
    result = transcription(fasta_file)
    expected_result = {'MJ712037.1': 'GGCCUAACUCUCUGAAACGAUGAAUUACACAAGUUUUAUUUUCGCUUUUCAGCUUUGCAUAAUUUUGUGUUCUUCUGGUUGUUACUGUCAGGCCAUGUUUUUUAAAGAAAUAGAAGAGCUAAAGGGAUAUUUUAAUGCAAGUAAUCCAGAUGUAGCAGAUGGUGGGUCGCUUUUCGUAGACAUUUCAAAGAACUGGAAAGAGGAGAGUGAUAAAACAAUAAUUCAAAGCCAAAUUGUGAAUUCCUCCUUCUACUUGAAAAUGUUUGAAAACCUGAAAGAUGAUGACCAGCGCAUUCAAAGGAACAUGGACACCAUCAAGGAAGACAUGCUUGAUAAGUUGUUAAAUACCAGCUCCAGUAAACGGGAUGACUUCCUCAAGCUGAUUCAAAUCCCUGUGAAUGAUCUGCAGGUCCAGCGCAAAGCAAUAAAUGAACUCUUCAAAGUGAUGAACGAUCUCUCACCAAGAUCUAACCUGAGGAAGCGGAAAAGGAGUCAGAAUCUGUUUCGAGGCCGUAGAGCAUCGAAAUAAAGCUUAUGGUCGUCCUGCCUGCAAUAUUUG', 'LJ712037.1': 'GGCCUAACUCUCUGAAACGAUGAAUUACACAAGUUUUAUUUUCGCUUUUCAGCUUUGCAUAAUUUUGUGUUCUUCUGGAAUUCGUUGUUACUGUCAGGCCAUGUUUUUUAAAGAAAUAGAAGAGCUAAAGGGAUAUUUUAAUGCAAGUAAUCCAGAUGUAGCAGAUGGUGGGUCGCUUUUCGUAGACAUUUCAAAGAACUGGAAAGAGGAGAGUGAUAAAACAAUAAUUCAAAGCCAAAUUGUCUCCUUCUACUUGAAAAUGUUUGAAAACCUGAAAGAUGAUGAC', 'FK712037.1': 'UAAAACAAUAAUUCAAAGCCAAAUUGUCUCCUUCUACUUGAAAAUGUUUGAGAAUUCAAACCUGAAAGAUGAUGACCAGCGCAUUCAAAGGAACAUGGACACCAUCAAGGAAGACAUGCUUGAUAAGUUGUUAAAUACCAGCUCCAGUAAACGGGAUGACUUCGAAUUCCUCAAGCUGAUUGAAUUCCAAAUCCCUGUGAAUGAUGAAUUCCUGCAGGUCCAGCGCAAAGCAAUAAAUGAACUCGAAUUCUUCAAAGUGAUGAACGAUCUCUCACCAAGAUCUAACCUGAGGAAGCGGAAAAGGAGUCAGAAUCUGUUUCGAGGCCGUAGAGCAUCGAAAUGAAUUCAAUGGUCGUCCUGCCUGCAAUAUUUG'}
    assert result == expected_result

def test_transcription_PROTEIN():
    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    with pytest.raises(ValueError, match="Unable to perform operation: Not a DNA sequence"):
        transcription(fasta_file)

def test_transcription_RNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "rna.fasta")
    with pytest.raises(ValueError, match="The sequence is already RNA"):
        transcription(fasta_file)

if __name__ == "__main__":
    pytest.main([__file__])
