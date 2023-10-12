import pytest
import os
from genesys.DNAToolKit import *
from genesys.visuals import *

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
    expected_result = {'MJ712037.1': 'GGCCUAACUCUCUGAAACGAUGAAUUACACAAGUUUUAUUUUCGCUUUUCAGCUUUGCAUAAUUUUGUGUUCUUCUGGUUGUUACUGUCAGGCCAUGUUUUUUAAAGAAAUAGAAGAGCUAAAGGGAUAUUUUAAUGCAAGUAAUCCAGAUGUAGCAGAUGGUGGGUCGCUUUUCGUAGACAUUUCAAAGAACUGGAAAGAGGAGAGUGAUAAAACAAUAAUUCAAAGCCAAAUUGUGAAUUCCUCCUUCUACUUGAAAAUGUUUGAAAACCUGAAAGAUGAUGACCAGCGCAUUCAAAGGAACAUGGACACCAUCAAGGAAGACAUGCUUGAUAAGUUGUUAAAUACCAGCUCCAGUAAACGGGAUGACUUCCUCAAGCUGAUUCAAAUCCCUGUGAAUGAUCUGCAGGUCCAGCGCAAAGCAAUAAAUGAACUCUUCAAAGUGAUGAACGAUCUCUCACCAAGAUCUAACCUGAGGAAGCGGAAAAGGAGUCAGAAUCUGUUUCGAGGCCGUAGAGCAUCGAAAUAAAGCUUAUGGUCGUCCUGCCUGCAAUAUUUG',
                       'LJ712037.1': 'GGCCUAACUCUCUGAAACGAUGAAUUACACAAGUUUUAUUUUCGCUUUUCAGCUUUGCAUAAUUUUGUGUUCUUCUGGAAUUCGUUGUUACUGUCAGGCCAUGUUUUUUAAAGAAAUAGAAGAGCUAAAGGGAUAUUUUAAUGCAAGUAAUCCAGAUGUAGCAGAUGGUGGGUCGCUUUUCGUAGACAUUUCAAAGAACUGGAAAGAGGAGAGUGAUAAAACAAUAAUUCAAAGCCAAAUUGUCUCCUUCUACUUGAAAAUGUUUGAAAACCUGAAAGAUGAUGAC', 'FK712037.1': 'UAAAACAAUAAUUCAAAGCCAAAUUGUCUCCUUCUACUUGAAAAUGUUUGAGAAUUCAAACCUGAAAGAUGAUGACCAGCGCAUUCAAAGGAACAUGGACACCAUCAAGGAAGACAUGCUUGAUAAGUUGUUAAAUACCAGCUCCAGUAAACGGGAUGACUUCGAAUUCCUCAAGCUGAUUGAAUUCCAAAUCCCUGUGAAUGAUGAAUUCCUGCAGGUCCAGCGCAAAGCAAUAAAUGAACUCGAAUUCUUCAAAGUGAUGAACGAUCUCUCACCAAGAUCUAACCUGAGGAAGCGGAAAAGGAGUCAGAAUCUGUUUCGAGGCCGUAGAGCAUCGAAAUGAAUUCAAUGGUCGUCCUGCCUGCAAUAUUUG'}
    assert result == expected_result


def test_transcription_PROTEIN():
    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    with pytest.raises(ValueError, match="Unable to perform operation: Not a DNA sequence"):
        transcription(fasta_file)


def test_transcription_RNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "random_rna.fasta")
    with pytest.raises(ValueError, match="The sequence is already RNA"):
        transcription(fasta_file)


def test_complementary_DNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "sequence.fasta")
    result = complementary(fasta_file)
    expected_result = {'MJ712037.1': 'CCGGATTGAGAGACTTTGCTACTTAATGTGTTCAAAATAAAAGCGAAAAGTCGAAACGTATTAAAACACAAGAAGACCAACAATGACAGTCCGGTACAAAAAATTTCTTTATCTTCTCGATTTCCCTATAAAATTACGTTCATTAGGTCTACATCGTCTACCACCCAGCGAAAAGCATCTGTAAAGTTTCTTGACCTTTCTCCTCTCACTATTTTGTTATTAAGTTTCGGTTTAACACTTAAGGAGGAAGATGAACTTTTACAAACTTTTGGACTTTCTACTACTGGTCGCGTAAGTTTCCTTGTACCTGTGGTAGTTCCTTCTGTACGAACTATTCAACAATTTATGGTCGAGGTCATTTGCCCTACTGAAGGAGTTCGACTAAGTTTAGGGACACTTACTAGACGTCCAGGTCGCGTTTCGTTATTTACTTGAGAAGTTTCACTACTTGCTAGAGAGTGGTTCTAGATTGGACTCCTTCGCCTTTTCCTCAGTCTTAGACAAAGCTCCGGCATCTCGTAGCTTTATTTCGAATACCAGCAGGACGGACGTTATAAAC',
                       'LJ712037.1': 'CCGGATTGAGAGACTTTGCTACTTAATGTGTTCAAAATAAAAGCGAAAAGTCGAAACGTATTAAAACACAAGAAGACCTTAAGCAACAATGACAGTCCGGTACAAAAAATTTCTTTATCTTCTCGATTTCCCTATAAAATTACGTTCATTAGGTCTACATCGTCTACCACCCAGCGAAAAGCATCTGTAAAGTTTCTTGACCTTTCTCCTCTCACTATTTTGTTATTAAGTTTCGGTTTAACAGAGGAAGATGAACTTTTACAAACTTTTGGACTTTCTACTACTG', 'FK712037.1': 'ATTTTGTTATTAAGTTTCGGTTTAACAGAGGAAGATGAACTTTTACAAACTCTTAAGTTTGGACTTTCTACTACTGGTCGCGTAAGTTTCCTTGTACCTGTGGTAGTTCCTTCTGTACGAACTATTCAACAATTTATGGTCGAGGTCATTTGCCCTACTGAAGCTTAAGGAGTTCGACTAACTTAAGGTTTAGGGACACTTACTACTTAAGGACGTCCAGGTCGCGTTTCGTTATTTACTTGAGCTTAAGAAGTTTCACTACTTGCTAGAGAGTGGTTCTAGATTGGACTCCTTCGCCTTTTCCTCAGTCTTAGACAAAGCTCCGGCATCTCGTAGCTTTACTTAAGTTACCAGCAGGACGGACGTTATAAAC'}
    assert result == expected_result


def test_complementary_PROTEIN():
    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    with pytest.raises(ValueError, match="Unable to perform operation: Not a DNA sequence"):
        complementary(fasta_file)


def test_complementary_RNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "random_rna.fasta")
    with pytest.raises(ValueError, match="Unable to perform operation: Not a DNA sequence"):
        complementary(fasta_file)


def test_GC_content_DNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "sequence.fasta")
    result = gc_content(fasta_file)
    expected_result = {'MJ712037.1': 39.71,
                       'LJ712037.1': 35.31, 'FK712037.1': 40.75}
    assert result == expected_result


def test_GC_content_DNA2():
    fasta_file = os.path.join(TEST_DATA_DIR, "random_dna.fasta")
    result = gc_content(fasta_file)
    expected_result = {'DNA_1': 50.0, 'DNA_2': 47.2,
                       'DNA_3': 53.0, 'DNA_4': 51.6, 'DNA_5': 49.8}
    assert result == expected_result


def test_GC_content_PROTEIN():
    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    with pytest.raises(ValueError, match="Unable to perform operation: Not a DNA sequence"):
        gc_content(fasta_file)


def test_GC_content_RNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "sequence.fasta")
    result = gc_content(fasta_file)
    expected_result = {'MJ712037.1': 39.71,
                       'LJ712037.1': 35.31, 'FK712037.1': 40.75}
    assert result == expected_result


def test_translation_DNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "sequence.fasta")
    result = translation(fasta_file)
    expected_result = {'MJ712037.1': 'GLTL*NDELHKFYFRFSALHNFVFFWLLLSGHVF*RNRRAKGIF*CK*SRCSRWWVAFRRHFKELERGE**NNNSKPNCEFLLLLENV*KPER**PAHSKEHGHHQGRHA**VVKYQLQ*TG*LPQADSNPCE*SAGPAQSNK*TLQSDERSLTKI*PEEAEKESESVSRP*SIEIKLMVVLPAIFX',
                       'LJ712037.1': 'GLTL*NDELHKFYFRFSALHNFVFFWNSLLLSGHVF*RNRRAKGIF*CK*SRCSRWWVAFRRHFKELERGE**NNNSKPNCLLLLENV*KPER**X', 'FK712037.1': '*NNNSKPNCLLLLENV*EFKPER**PAHSKEHGHHQGRHA**VVKYQLQ*TG*LRIPQAD*IPNPCE**IPAGPAQSNK*TRILQSDERSLTKI*PEEAEKESESVSRP*SIEMNSMVVLPAIFX'}
    assert result == expected_result


def test_translation_DNA2():
    fasta_file = os.path.join(TEST_DATA_DIR, "random_dna.fasta")
    result = translation(fasta_file)
    expected_result = {'DNA_1': 'PTCPFAAKRHGTKSKLESVKQVQSQSLTTRSLS*RGSLHCRADCVGLPKPRQVRVKCNSLCYFNPTT*K*QNRKCTL*ARSISVTRRTRSARLRIQLVI*KVT*MHYLGRMNTWIITQIYQVCHRATPRLKSCSLAIRKRYSAMCGPSSKIGSQPFRRPPEVLQA*L', 'DNA_2': 'SQ*QQNRYVELAESLSL*LPHRPEFRTLIISGTP*YCNARVGETLMLVVDVPLPNGIGLIIEIP*KTGCPCRDRACGILRWELDDRSLKRQLEVIASN*YGKNVSLFRDGNTSRKHSVVQPLKNLQINDSRILWVIGATCHGADSSFTGPSALRVVVSSQNAGVRYV',
                       'DNA_3': 'DVPSDPNRHEQGEQNYFSR*ALHFAFGNQRGDYSH*PEVGSTPRGGVALWPDRRIITMELFKSLVYLVGPGQGTDACLSSDQYSTGGLATSVLASLLGASLASGQRIGRMQVECTMCLRIWVYGPPRSRQSINSLTLCLSKCYDHLGAQHYDARNVHLMGEPETMYR', 'DNA_4': 'KSVTKTR*ARLLDTSRDVLRNVCTITTRWSSVWWKSLLLYTPSPCGASPRPFSLYIV*GV*GRSTERSHCV*MDY*VATICTNCSKGEWVVGAGR*AGCFLFRYSCW*RKKRGCLHVKTLDDRIRETIGYPCQVAL*PVNTLSREKYIISEVSFGPFQERCYVIVAA', 'DNA_5': 'RRIDMATG*TRVLNGECRKGESHDESGLQSQASRGTGIPDVT*YITQFGPNER*PDSQWSFHTLDFLLVILPYLPILGHDEGETYDDPKRLKSGLAQLYVDTIQLPVVCTPGRAHMPLEETPLLNALRVAFSTIVC*SQS*TVIGSHY*SNHLNSASYGELPE*TGX'}
    assert result == expected_result


def test_translation_PROTEIN():
    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    with pytest.raises(ValueError, match="Unable to perform operation: Not a DNA sequence"):
        translation(fasta_file)


def test_translation_RNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "random_rna.fasta")
    with pytest.raises(ValueError, match="Unable to perform operation: Not a DNA sequence"):
        translation(fasta_file)


def test_mass_calculator_DNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "sequence.fasta")
    result = mass_calculator(fasta_file)
    expected_result = {'MJ712037.1': 173132.77179999973,
                       'LJ712037.1': 88651.7404999999, 'FK712037.1': 115364.86929999982}
    assert result == expected_result


def test_mass_calculator_PROTEIN():
    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    result = mass_calculator(fasta_file)
    expected_result = {'QJF75467.1': 'Ambiguous amino acid(s) found in sequence QJF75467.1: B at position 353', 'QII57278.1': 141142.79980000042,
                       'YP_009724390.1': 141176.8160000004, 'QJF77846.1': 141150.7821000004, 'QIZ16509.1': 141190.8426000004}
    assert result == expected_result


def test_restriction_sites_DNA():
    fasta_file = os.path.join(TEST_DATA_DIR, "random_dna.fasta")
    result = restriction_sites(fasta_file)
    expected_result = {'DNA_1': {'HindIII': [(44, Seq('GCTTGA')), (91, Seq('GCTTGT'))], 'BamHI': [(107, Seq('ATCCCT'))]}, 'DNA_2': {
        'SalI': [(146, Seq('CGACGT'))]}, 'DNA_4': {'KpnI': [(391, Seq('CCTGTC'))]}, 'DNA_5': {'SalI': [(299, Seq('CGACAC'))]}}
    assert result == expected_result


def test_multiple_sequence_alignment():
    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    result = multiple_sequence_alignment(fasta_file)

    expected_result = (
        "Alignment with 5 rows and 1273 columns\n"
        "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFR...HYT QJF75467.1\n"
        "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFR...HYT QII57278.1\n"
        "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFR...HYT YP_009724390.1\n"
        "MFVFLVLLPLVSSQCVNLTTRTQLPPAHTNSFTRGVYYPDKVFR...HYT QJF77846.1\n"
        "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFR...HYT QIZ16509.1\n"
    )

    # Just removes all the fancy styling to you can actually compare 2 strings normally lol
    result_str = str(result)
    expected_result = expected_result.rstrip()

    assert result_str == expected_result


def test_construct_phylogenetic_tree():

    fasta_file = os.path.join(TEST_DATA_DIR, "msa.fasta")
    tree = construct_phylogenetic_tree(fasta_file)

    # Check if the result is of type Phylo.BaseTree.Tree --> I used ChatGPT for this lol
    assert isinstance(tree, Phylo.BaseTree.Tree)


if __name__ == "__main__":
    pytest.main()
