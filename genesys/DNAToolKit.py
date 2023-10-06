import random
import collections
import json
from Bio import Phylo, SeqIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Align import MultipleSeqAlignment
from Bio import AlignIO
from io import StringIO
import matplotlib.pyplot as plt

# Counting DNA Nucleotides

nucleotides = ['A', 'C', 'T', 'G']
complementary_nucleotides = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

codon_table = {
    "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L", "CUU": "L", "CUC": "L",
    "CUA": "L", "CUG": "L", "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V", "UCU": "S", "UCC": "S",
    "UCA": "S", "UCG": "S", "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T", "GCU": "A", "GCC": "A",
    "GCA": "A", "GCG": "A", "UAU": "Y", "UAC": "Y", "UAA": "*", "UAG": "*",
    "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q", "AAU": "N", "AAC": "N",
    "AAA": "K", "AAG": "K", "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "UGU": "C", "UGC": "C", "UGA": "*", "UGG": "W", "CGU": "R", "CGC": "R",
    "CGA": "R", "CGG": "R", "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
}

aa_protein_mass = {'A': 71.03711,
                   'C': 103.00919,
                   'D': 115.02694,
                   'E': 129.04259,
                   'F': 147.06841,
                   'G': 57.02146,
                   'H': 137.05891,
                   'I': 113.08406,
                   'K': 128.09496,
                   'L': 113.08406,
                   'M': 131.04049,
                   'N': 114.04293,
                   'P': 97.05276,
                   'Q': 128.05858,
                   'R': 156.10111,
                   'S': 87.03203,
                   'T': 101.04768,
                   'V': 99.06841,
                   'W': 186.07931,
                   'Y': 163.06333}


def sequence_type(filepath):
    """ Determine the type of sequence in a FASTA file.

    Args:
        filepath (str): Path to the FASTA file.
    """

    with open(filepath, "r") as f:
        for seq in SeqIO.parse(f, "fasta"):
            seq_str = str(seq.seq)
            if set(seq_str.upper()) <= set("ATGC"):
                return "DNA"
            elif set(seq_str.upper()) <= set("AUGC"):
                return "RNA"
            elif set(seq_str.upper()) <= set("ARNDCEQGHILKMFPSTWYV"):
                return "Protein"
    return "Unknown sequence type"
    

def count_occurences(filepath):
    """ Count the number of nucleotides for each DNA/RNA sequence or amino acids for each protein in a FASTA file.

    Args:
        filepath (str): Path to the FASTA file.
    
    Returns:
        dict: Dictionary with sequence IDs as keys and a Counter object as number of occurences.
    """

    if sequence_type(filepath) == "Unknown sequence type":
        raise ValueError("Unable to perform operation: Unknown sequence type")
    
    sequences_dict = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))

    ret = {}

    for seq_id, seq in sequences_dict.items():
        seq_str = str(seq.seq)
        ret[seq_id] = collections.Counter(seq_str)

    return ret

# Gives the complementary DNA sequence to a given DNA seq

def transcription(filepath):
    
    if sequence_type(filepath) == "RNA":
        raise ValueError("The sequence is already RNA")
    elif sequence_type(filepath) != "DNA":
        raise ValueError("Unable to perform operation: Not a DNA sequence")
    
    sequences_dict = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))

    ret = {}

    for seq_id, seq in sequences_dict.items():
        seq_str = str(seq.seq)
        ret[seq_id] = seq_str.replace("T", "U")
    
    return ret

# Transcripts a given DNA sequence (gives the RNA version)
def complementary(dna):
    dna = dna.replace("T", "U")
    compSeq = ''
    for i in dna:
        if i == 'A':
            compSeq += 'T'
        elif i == 'U':
            compSeq += 'A'
        elif i == 'C':
            compSeq += 'G'
        elif i == 'G':
            compSeq += 'C'
        else:
            compSeq += i
    
    return compSeq

# Gives the reverse complementary DNA sequence to a given DNA seq   

def reverseComplementary(dna):
    reverseSeq = complementary(dna)

    return reverseSeq[::-1]

# The combined above two functions into one GC content calculator

def GC_Content_combined(dna, k=None):
    if k is None:
        total_GC = dna.count('G') + dna.count('C')
        GC_percentage = (total_GC / len(dna)) * 100
        result = print(f"GC Content: {GC_percentage}")
    else:
        subsections = []
        for i in range(0, len(dna) - k + 1, k):
            subsections.append(dna[i:i+k])

        for i in range(len(subsections)):
            total_GC = subsections[i].count('G') + subsections[i].count('C')
            GC_percentage = 100 * (total_GC / len(subsections[i]))
            result = print(
                f"Subsection: {subsections[i]} - GC Content: {GC_percentage}")

    return result


def translation(dna):

    dna = transcription(dna)

    if len(dna) == 0:
        return ""
    
    translated_seq = ""

    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i+3]

        if codon in codon_table:
            amino_acid = codon_table[codon]
            
            # Check if the amino acid is a stop codon
            if amino_acid == "*":
                break 
            else:
                translated_seq += amino_acid
        else:
            translated_seq += '?'

    return translated_seq



def protein_mass(dna):
    
    prot_mass = 0
    for aa in dna:
        if aa in aa_protein_mass:
            prot_mass += aa_protein_mass[aa]
        else:
            print(f"Warning: Unknown amino acid '{aa}' encountered.")
    
    return str(prot_mass)



def hamming_distance(dna1, dna2):
    if len(dna1) != len(dna2):
        raise ValueError("Input sequences must have the same length")

    hammingDist = 0
    for i in range(len(dna1)):
        if dna1[i] != dna2[i]:
            hammingDist += 1

    return hammingDist


def open_reading_frames(dna):
    seq1 = dna
    seq2 = dna[1:]
    seq3 = dna[2:]

    frame1 = translation(seq1)
    frame2 = translation(seq2)
    frame3 = translation(seq3)

    # Concatenate the protein sequences into a single string
    combined_frames = frame1 + frame2 + frame3

    return combined_frames


def restriction_sites(dna):
    reverse_palindromes = []
    
    for length in range(4, 13):
        for i in range(len(dna) - length + 1):
            subsequence = dna[i:i+length]
            complement = reverseComplementary(subsequence)
            
            if subsequence == complement:
                reverse_palindromes.append(subsequence)

    reverse_palindromes_str = ', '.join(reverse_palindromes)
    
    return reverse_palindromes_str


def multiple_sequence_alignment(dna):
    text_file = StringIO(dna)
    alignment = AlignIO.read(text_file, "fasta")
    aligned_seqs = MultipleSeqAlignment(alignment)

    return str(aligned_seqs)

def construct_phylogenetic_tree(aligned_seqs):
    calculator = DistanceCalculator("identity")
    constructor = DistanceTreeConstructor(calculator)
    tree = constructor.build_tree(aligned_seqs)
    
    fig, ax = plt.subplots(figsize=(10, 20))
    Phylo.draw(tree, axes=ax)
    
    fig.savefig("phylogenetic_tree.png")
    
    return tree

def detect_snps(seq1, seq2):
    """
    Detect singular nucleotide polymorphisms (SNPs) between two DNA sequences.
    
    Parameters:
    - seq1, seq2: strings representing the DNA sequences to compare. They should be of the same length.

    Returns:
    - List of tuples (position, nucleotide_from_seq1, nucleotide_from_seq2) representing the SNPs.
    """
    
    # Ensure both sequences are of the same length
    if len(seq1) != len(seq2):
        raise ValueError("The sequences should be of the same length.")
    
    # Detect SNPs
    snps = [(i, seq1[i], seq2[i]) for i in range(len(seq1)) if seq1[i] != seq2[i]]

    return snps
