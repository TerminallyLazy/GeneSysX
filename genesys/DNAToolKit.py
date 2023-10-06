import random
import collections
import json
from Bio import Phylo
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

# Generates a random DNA sequence with a specified length


def randomDNA(length_of_DNA):
    randDNA = ""
    for i in range(length_of_DNA):
        randNuc = random.choice(nucleotides)
        randDNA += randNuc
    return randDNA

# Validates whether a sequence is a DNA sequence or not


def validateDNA(dna):
    dna_seq = dna.upper()
    replaced_seq = ""

    for nucleotide in dna_seq:
        if nucleotide == 'N':
            # Replace 'N' with a random nucleotide
            random_nucleotide = random.choice(nucleotides)
            replaced_seq += random_nucleotide
        elif nucleotide not in nucleotides:
            return False
        else:
            replaced_seq += nucleotide

    return replaced_seq


# Count the number of each nucleotide in a given DNA sequence
def countNucleotides(dna):
    count_dict = dict(collections.Counter(dna))
    count_json = json.dumps(count_dict)
    return count_json

# Gives the complementary DNA sequence to a given DNA seq

def transcription(dna):
    transcribedSeq = dna.replace("T", "U")
    return transcribedSeq


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


def multiple_sequence_alignment(fasta_files):
    text_file = StringIO(fasta_files)
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

