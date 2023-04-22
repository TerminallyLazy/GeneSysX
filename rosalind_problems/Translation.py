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

with open('rosalind_prot.txt', 'r') as file:
    contents = file.read()
    print(contents)


def translation(dna):
    # Loops through the DNA sequence and separated them into codons
    separated_codons = []
    for i in range(0, len(dna), 3):
        codon = dna[i:i+3]
        separated_codons.append(codon)

    # remove the last element from separated_codons
    separated_codons.pop()
    # print(separated_codons)

    # Loops through the dictionary to find the AA for a given codon
    AA_seq = ""
    for codon in separated_codons:
        AA = codon_table[codon]
        # print(AA)
        AA_seq += AA
    print(AA_seq)


translation(contents)
