def hamming_distance(dna1, dna2):
    hammingDist = 0
    for i in range(len(dna1)):
        if dna1[i] != dna2[i]:
            hammingDist += 1

    return hammingDist

