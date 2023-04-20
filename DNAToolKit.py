# Import necessary modules
import random
import collections

# Counting DNA Nucleotides

nucleotides = ['A', 'C', 'T', 'G']
complementary_nucleotides = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

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
    for i in dna_seq:
        if i not in nucleotides:
            return False
    return dna_seq


# Count the number of each nucleotide in a given DNA sequence
def countNucleotides(dna):
    # nucleotides = {"A": 0, "T": 0, "C": 0, "G": 0}
    # for base in dna:
    #    if base in nucleotides:
    #        nucleotides[base] += 1
    # count_strs = [f"{n}: {c}" for n, c in nucleotides.items()]
    # return ", ".join(count_strs)

    return dict(collections.Counter(dna))    # Optimized way

# Transcripts a given DNA sequence (gives the RNA version)
def transcription(dna):
    transcribedSeq = dna.replace("T", "U")
    return transcribedSeq

# Gives the complementary DNA sequence to a given DNA seq
def complementary(dna):
    compSeq = ''
    if validateDNA != False:
        for i in dna:
            compSeq += complementary_nucleotides[i]
    return compSeq

# Gives the reverse complementary DNA sequence to a given DNA seq
def reverseComplementary(dna):
    reverseSeq = complementary(dna)
    
    return reverseSeq[::-1]