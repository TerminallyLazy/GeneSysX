def dna_to_binary(dna_sequence):
    # Define a dictionary to map nucleotides to binary representations
    nucleotide_to_binary = {
        'A': '00',
        'T': '01',
        'C': '10',
        'G': '11'
    }
    
    # Initialize an empty string to store the binary representation
    binary_sequence = ''
    
    # Iterate through each character in the input DNA sequence
    for base in dna_sequence:
        # Check if the base is a valid nucleotide
        if base in nucleotide_to_binary:
            # Append the binary representation of the nucleotide to the result
            binary_sequence += nucleotide_to_binary[base]
        else:
            # Handle invalid characters (e.g., N, X, etc.) if needed
            # You can add error handling or simply skip invalid characters.
            pass
    
    return binary_sequence

# Example usage:
dna_sequence = "ATCGATCG"
binary_representation = dna_to_binary(dna_sequence)
print(binary_representation)
