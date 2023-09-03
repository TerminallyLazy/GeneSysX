# Generate a random DNA sequence
random_sequence = randomDNA(10)
print("Random DNA Sequence:", random_sequence)

# Validate whether the sequence is DNA
validated_dna = validateDNA(dna)
print("Validated DNA Sequence:", validated_dna)

# Count the number of each nucleotide in the DNA sequence
nucleotide_count = countNucleotides(dna)
print("Nucleotide Count:", nucleotide_count)

# Transcribe the DNA sequence
transcribed_dna = transcription(dna)
print("Transcribed DNA Sequence:", transcribed_dna)

# Find the complementary DNA sequence
complementary_dna = complementary(transcribed_dna)
print("Complementary DNA Sequence:", complementary_dna)

# Find the reverse complementary DNA sequence
reverse_complementary_dna = reverseComplementary(dna)
print("Reverse Complementary DNA Sequence:", reverse_complementary_dna)

# Calculate the GC content
gc_content = GC_Content_combined(dna)
print("GC Content:", gc_content)

# Translate the DNA sequence
translated_sequence = translation(transcribed_dna)
print("Translated Sequence:", translated_sequence)

# Calculate the protein mass
protein_mass_value = protein_mass(translated_sequence)
print("Protein Mass:", protein_mass_value)

# Calculate the Hamming distance between two DNA sequences
dna2 = "ATGCGGCGTGACUGA"  # A different DNA sequence for comparison
hamming_dist = hamming_distance(dna, dna2)
print("Hamming Distance:", hamming_dist)

# Find open reading frames
orf_frames = open_reading_frames(dna)
print("Open Reading Frames:", orf_frames)