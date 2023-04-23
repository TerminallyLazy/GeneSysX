import unittest
from DNAToolKit import *

class TestDNAFunctions(unittest.TestCase):

    def test_randomDNA(self):
        seq = randomDNA(10)
        self.assertEqual(len(seq), 10)
        self.assertTrue(set(seq).issubset(set(nucleotides)))

    def test_validateDNA(self):
        valid_dna = 'ATCG'
        invalid_dna = 'XYZ'
        self.assertEqual(validateDNA(valid_dna), 'ATCG')
        self.assertFalse(validateDNA(invalid_dna))

    def test_countNucleotides(self):
        dna = 'ATCGATCGATCG'
        expected_output = {'A': 3, 'T': 3, 'C': 3, 'G': 3}
        self.assertEqual(countNucleotides(dna), expected_output)

    def test_transcription(self):
        dna = 'ATCG'
        expected_output = 'AUCG'
        self.assertEqual(transcription(dna), expected_output)

    def test_complementary(self):
        dna = 'ATCG'
        expected_output = 'TAGC'
        self.assertEqual(complementary(dna), expected_output)

    def test_reverseComplementary(self):
        dna = 'ATCG'
        expected_output = 'CGAT'
        self.assertEqual(reverseComplementary(dna), expected_output)

    def test_GC_Content_combined(self):
        dna = 'ATCG'
        expected_output = 50.0
        self.assertAlmostEqual(GC_Content_combined(dna), expected_output)

        dna = 'ATCGATCGATCG'
        k = 3
        expected_output = 'Subsection: ATC - GC Content: 33.33333333333333\nSubsection: GAT - GC Content: 66.66666666666666\nSubsection: CGA - GC Content: 66.66666666666666\nSubsection: TCG - GC Content: 0.0'
        self.assertEqual(GC_Content_combined(dna, k), expected_output)


if __name__ == '__main__':
    unittest.main()
