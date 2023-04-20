import random
import collections

# Counting DNA Nucleotides

nucleotides = ['A', 'C', 'T', 'G']

def randomDNA(length_of_DNA):
    randDNA = ""
    for i in range(length_of_DNA):
        randNuc = random.choice(nucleotides)
        randDNA += randNuc
    return randDNA

def validateDNA(dna):
    dna_seq = dna.upper()
    for i in dna_seq:
        if i not in nucleotides:
            return False
    return dna_seq

def countNucleotides(dna):
    #nucleotides = {"A": 0, "T": 0, "C": 0, "G": 0}
    #for base in dna:
    #    if base in nucleotides:
    #        nucleotides[base] += 1
    #count_strs = [f"{n}: {c}" for n, c in nucleotides.items()]
    #return ", ".join(count_strs) 
    
    return dict(collections.Counter(dna))    # Optimized way 

