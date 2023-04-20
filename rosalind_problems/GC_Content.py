


def GC_Content(dna):
    total_GC = dna.count('G') + dna.count('C')
    GC_percentage = (total_GC / len(dna)) * 100
    return GC_percentage
