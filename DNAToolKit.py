# Import necessary modules
import random
import collections

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

# Computes the GC content of a given DNA sequence

# def GC_Content(dna):
#    total_GC = dna.count('G') + dna.count('C')
#    GC_percentage = (total_GC / len(dna)) * 100
#    return GC_percentage


# k = the number of nucleotides for each subsection
# def GC_Content_subsections(dna, k=5):

#    subsections = []
#    for i in range(0, len(dna) - k + 1, k):
#        subsections.append(dna[i:i+k])

#    for i in range(len(subsections)):
#        total_GC = subsections[i].count('G') + subsections[i].count('C')
#        GC_percentage = 100 * (total_GC / len(subsections[i]))
#        result = print(f"Subsection: {subsections[i]} - GC Content: {GC_percentage}")

#    return result

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
    # Loops through the DNA sequence and separated them into codons
    separated_codons = []
    for i in range(0, len(dna), 3):
        codon = dna[i:i+3]
        separated_codons.append(codon)

    # print(separated_codons)

    # Loops through the dictionary to find the AA for a given codon
    for codon in separated_codons:
        AA = codon_table[codon]
        print(AA)


translation("AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA")
