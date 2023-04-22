def GC_Content(dna):
    total_GC = dna.count('G') + dna.count('C')
    GC_percentage = (total_GC / len(dna)) * 100
    return GC_percentage

with open('rosalind_gc.txt', 'r') as file:
    contents = file.read()
    cleaned_data = contents.replace(">", "")
    
sequences = {}
lines = cleaned_data.split("\n")
i = 0
while i < len(lines):
    name = lines[i]
    i += 1
    sequence = ""
    while i < len(lines) and not lines[i].startswith("Rosalind"):
        sequence += lines[i]
        i += 1
    sequences[name] = sequence

GC_Content_Percentages = []
for FASTA_tag, DNA_Seq in sequences.items():
    GC_Content_Percentages.append(GC_Content(DNA_Seq))
    print(f"The GC Content for {FASTA_tag}: {GC_Content(DNA_Seq)}")
    
max_GC = max(GC_Content_Percentages)
max_GC_index = GC_Content_Percentages.index(max_GC)
max_GC_FASTA_tag = list(sequences.keys())[max_GC_index]

print(f"The DNA Sequence with the maximum GC Content is {max_GC_FASTA_tag} with a GC Content of {max_GC}%")



