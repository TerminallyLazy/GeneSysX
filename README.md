# Bioinformatics
This is my attempt at learning Bioinformatics using Python and solving the Rosalind problems


# Day 1: MCAT Biochemistry Review + Some Code

## Completed:
- Validating and Counting the number of nucleotides in a DNA string
- Transcription: Essentially transcribing a DNA seq to it's RNA version
- Reverse Complementary Strands: Finds the complement strand and reverses it
- GC Content: Computes the GC content of a given strand (COME BACK)

Link to the problems: 
- https://rosalind.info/problems/dna/
- https://rosalind.info/problems/rna/
- https://rosalind.info/problems/revc/
- https://rosalind.info/problems/gc/


# Day 2: Busy Day
## Completed:
- GC Content: Computes the GC content of a given strand.
    - Solved the Rosalind problem code that finds the maximum GC content of a given FASTA file
- Translation: Given a DNA sequence, translate it into it's respective AA sequence

Link to the problems: 
- https://rosalind.info/problems/gc/
- https://rosalind.info/problems/prot/


# Day 3: Becoming more Algorithm based Problems
 ## Completed
 - Calculate the Protein Mass of a given protein sequence
 - Calculating Point Mutations: Wrote a function that calculates the hamming distance between two DNA sequences

 Link to the problems:
- https://rosalind.info/problems/prtm/
    - https://rosalind.info/glossary/monoisotopic-mass-table/
- https://rosalind.info/problems/hamm/


# We back:

Output:

Random DNA Sequence: AACGAA
Validated DNA Sequence: AACGAA
Nucleotide Count: {'A': 4, 'C': 1, 'G': 1}
Transcribed DNA Sequence: AACGAA
Complementary DNA Sequence: TTGCTT
Reverse Complementary DNA Sequence: TTCGTT
GC Content: 33.33333333333333
GC Content: None
Translated Sequence: NE
Protein Mass: 243.08551999999997
Hamming Distance: 5
Open Reading Frames: ('NE', 'T', 'R')


## Purpose of BLAST:

Sequence Alignment: BLAST is primarily used for sequence alignment, which is the process of finding regions of similarity or homology between two or more sequences. It can align a query sequence against a database of known sequences to identify regions where they match.

Identifying Homologous Sequences: BLAST can identify sequences in a database that are evolutionarily related to the query sequence. This is crucial for understanding the function and evolutionary history of genes and proteins.

Function Prediction: By identifying similar sequences in databases, BLAST can help predict the function of an unknown sequence based on the functions of the known homologous sequences. This is especially important for annotating newly sequenced genomes and genes.

Finding Orthologs and Paralogs: BLAST can distinguish between orthologous and paralogous genes. Orthologs are genes in different species that evolved from a common ancestral gene and typically have similar functions, while paralogs are genes in the same species that arose through gene duplication and may have diverged in function.

Database Searches: Researchers can use BLAST to search various sequence databases, such as GenBank, Swiss-Prot, or custom databases, to find sequences related to their query. This is essential for conducting comparative genomics and functional genomics studies.

Primer Design: BLAST can be used to design specific primers for PCR (Polymerase Chain Reaction) experiments. It helps ensure that the primers are specific to the target sequence and do not anneal to unintended sequences in the genome.

Phylogenetic Analysis: BLAST results can be used as a basis for constructing phylogenetic trees, which depict the evolutionary relationships between different species or genes.

Drug Discovery: BLAST can be employed in drug discovery and development to identify potential drug targets by finding homologous proteins in pathogenic organisms or identifying similar protein structures that can be targeted by drugs.


## More on BLAST:

### BLASTn:
This is used for nucleotide-nucleotide sequence comparisons. It's commonly used to compare DNA sequences against DNA databases. BLASTn can identify similar regions or sequences, which is useful for tasks like identifying homologous genes or regulatory elements.

### BLASTp: 
BLASTp is used for protein-protein sequence comparisons. It's used to compare a protein sequence against a protein sequence database. BLASTp is often used to find similar protein sequences, which can help researchers infer the function of a newly discovered protein.

### BLASTx: 
BLASTx is used to search a nucleotide sequence (usually a DNA sequence) against a protein database. It translates the nucleotide sequence in all six reading frames and then compares those translations to known protein sequences. This can be useful when you have a nucleotide sequence but want to find similar proteins.

### tBLASTn: 
tBLASTn is the reverse of BLASTx. It's used to search a protein sequence against a nucleotide database. This is often used when you have a protein sequence and want to identify nucleotide sequences that code for it.

### tBLASTx:
tBLASTx is a combination of the tBLASTn and BLASTx approaches. It translates both the query and database sequences in all six reading frames and compares them. This is useful when you're trying to find distant homologs.

### BLAST2Seq:
BLAST2Seq is used to compare two sequences, one as the query and the other as the subject. It's useful when you want to see the degree of similarity between two specific sequences.