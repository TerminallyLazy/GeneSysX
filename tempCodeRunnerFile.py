dna = "ATCGG"
compDNA = "TAGCC"

# Iterate through the sequences
for i in range(len(dna)):
    print(dna[i], compDNA[i])
    if i < len(dna) - 1:
        print(" |")
