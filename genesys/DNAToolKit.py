import collections
from Bio import Phylo, SeqIO
from Bio.SeqUtils.ProtParam import molecular_weight
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Restriction
from Bio.Align import MultipleSeqAlignment
from Bio import AlignIO
import matplotlib.pyplot as plt


def sequence_type(filepath):
    """ Determine the type of sequence in a FASTA file.

    Args:
        filepath (str): Path to the FASTA file.
    """
    try:
        with open(filepath, "r") as f:
            first = list(SeqIO.parse(f, "fasta"))[0]
            seq = str(first.seq)

            if set(seq.upper()) <= set("ATGC"):
                return "DNA"
            elif set(seq.upper()) <= set("AUGC"):
                return "RNA"
            elif set(seq.upper()) <= set("ARNDCEQGHILKMFPSTWYV"):
                return "Protein"
            else:
                return "Invalid"

    except FileNotFoundError:
        return f"File not found: {filepath}"


def count_occurences(filepath):
    """ Count the number of nucleotides for each DNA/RNA sequence or amino acids for each protein in a FASTA file.

    Args:
        filepath (str): Path to the FASTA file.

    Returns:
        dict: Dictionary with sequence IDs as keys and a Counter object as number of occurences.
    """

    if sequence_type(filepath) == "Unknown sequence type":
        raise ValueError("Unable to perform operation: Unknown sequence type")

    sequences_dict = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))

    ret = {}

    for seq_id, seq in sequences_dict.items():
        seq_str = str(seq.seq)
        ret[seq_id] = collections.Counter(seq_str)

    return ret

# Gives the complementary DNA sequence to a given DNA seq


def transcription(filepath):

    if sequence_type(filepath) == "RNA":
        raise ValueError("The sequence is already RNA")
    elif sequence_type(filepath) != "DNA":
        raise ValueError("Unable to perform operation: Not a DNA sequence")

    sequences_dict = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))

    ret = {}

    for seq_id, seq in sequences_dict.items():
        seq_str = str(seq.seq)
        ret[seq_id] = seq_str.replace("T", "U")

    return ret

# Transcripts a given DNA sequence (gives the RNA version)


def complementary(filepath):
    """
    Find the complementary DNA sequence to a given DNA sequence.

    Parameters:
    - filepath: Path to the FASTA file containing the DNA sequence.

    Returns:
    - A string containing the complementary DNA sequence.
    """
    sequences = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))
    complementary_sequences = {}

    for seq_id, seq_record in sequences.items():

        if sequence_type(filepath) != "DNA":
            raise ValueError("Unable to perform operation: Not a DNA sequence")

        sequence = seq_record.seq
        complementary_sequence = str(sequence.complement())
        complementary_sequences[seq_id] = complementary_sequence

    return complementary_sequences


# Gives the reverse complementary DNA sequence to a given DNA seq

def reverseComplementary(dna):
    reverseSeq = complementary(dna)

    return reverseSeq[::-1]

# The combined above two functions into one GC content calculator


def gc_content(filepath):

    sequences = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))
    gc_contents = {}

    for seq_id, seq_record in sequences.items():
        if sequence_type(filepath) == "Protein":
            raise ValueError("Unable to perform operation: Not a DNA sequence")

        sequence = seq_record.seq
        gc_content = round(gc_fraction(sequence) * 100, 2)
        gc_contents[seq_id] = gc_content

    return gc_contents


def translation(filepath):
    """
    Translate a DNA sequence to its protein sequence.

    Parameters:
    - filepath: Path to the FASTA file containing the DNA sequence.

    Returns:
    - A string containing the protein sequence.
    """

    sequences = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))
    translated_sequences = {}

    for seq_id, seq_record in sequences.items():
        if sequence_type(filepath) != "DNA":
            raise ValueError("Unable to perform operation: Not a DNA sequence")

        sequence = seq_record.seq
        num_n_to_add = 3 - (len(sequence) % 3)
        sequence = sequence + Seq("N" * num_n_to_add)

        translated_sequence = str(sequence.translate())
        translated_sequences[seq_id] = translated_sequence

    return translated_sequences


def find_invalid_amino_acid(sequence):
    invalid_positions = []
    for i, aa in enumerate(sequence):
        if aa not in "ACDEFGHIKLMNPQRSTVWY":
            invalid_positions.append((aa, i))
    return invalid_positions


def mass_calculator(filepath):
    """
    Calculate the mass of a DNA, RNA, or protein sequence.

    Parameters:
    - filepath (str): Path to the FASTA file containing sequences.

    Returns:
    - A dictionary where keys are sequence IDs and values are the calculated molecular weights or error messages.
    """
    sequences = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))
    masses = {}

    for seq_id, seq_record in sequences.items():
        sequence = seq_record.seq
        seq_type = sequence_type(filepath)

        try:
            if seq_type == "DNA":
                masses[seq_id] = molecular_weight(sequence)
            elif seq_type == "RNA":
                masses[seq_id] = molecular_weight(sequence, "RNA")
            elif seq_type == "Protein":
                invalid_positions = find_invalid_amino_acid(sequence)
                if invalid_positions:
                    error_message = f"Invalid amino acid(s) found in sequence {seq_id}: {', '.join(f'{aa} at position {pos}' for aa, pos in invalid_positions)}"
                    raise ValueError(error_message)
                masses[seq_id] = molecular_weight(sequence, "protein")
        except ValueError as e:
            masses[seq_id] = str(e)

    return masses

# TO DO : revist this function


def open_reading_frames(filepath):
    pass


def find_recognition_sites(dna_sequence, enzyme_name):
    sequence = Seq(dna_sequence)
    enzyme = getattr(Restriction, enzyme_name, None)

    if enzyme is None:
        raise ValueError(
            f"Enzyme '{enzyme_name}' not found in Biopython's Restriction module.")

    cut_sites = enzyme.search(sequence)

    recognition_sites = [(site, sequence[site:site + len(enzyme.site)])
                         for site in cut_sites]
    return recognition_sites


def restriction_sites(filepath):
    enzyme_names = ["EcoRI", "HindIII", "BamHI", "XhoI",
                    "NotI", "SalI", "EcoRV", "PstI", "KpnI", "SmaI"]

    sequences = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))
    result = {}

    if sequence_type(filepath) != "DNA":
        raise ValueError("Unable to perform operation: Not a DNA sequence")

    for seq_id, seq_record in sequences.items():
        dna_sequence = str(seq_record.seq)
        enzyme_sites = {}
        for enzyme_name in enzyme_names:
            sites = find_recognition_sites(dna_sequence, enzyme_name)
            if sites:
                enzyme_sites[enzyme_name] = sites
        if enzyme_sites:
            result[seq_id] = enzyme_sites

    return result


def multiple_sequence_alignment(filepath):
    """
    Perform multiple sequence alignment on a FASTA file.

    Parameters:
    - filepath: Path to the FASTA file containing the sequences to align.

    Returns:
    - A MultipleSeqAlignment object containing the aligned sequences.
    """
    with open(filepath, "r") as text_file:
        alignment = AlignIO.read(text_file, "fasta")

    aligned_seqs = MultipleSeqAlignment(alignment)

    return aligned_seqs


def construct_phylogenetic_tree(filepath):
    """
    Construct a phylogenetic tree from a FASTA file.

    Parameters:
    - filepath: Path to the FASTA file containing the sequences to align.

    Returns:
    - A Phylo.Tree object representing the phylogenetic tree.
    """

    aligned_seqs = multiple_sequence_alignment(filepath)
    calculator = DistanceCalculator("identity")
    constructor = DistanceTreeConstructor(calculator)
    tree = constructor.build_tree(aligned_seqs)

    fig, ax = plt.subplots(figsize=(10, 20))
    Phylo.draw(tree, axes=ax)

    fig.savefig("phylogenetic_tree.png")

    return tree

# REVISIT THIS FUNCTION WITH CHARLIE


def detect_snps(seq1, seq2):
    """
    Detect singular nucleotide polymorphisms (SNPs) between two DNA sequences.

    Parameters:
    - seq1, seq2: strings representing the DNA sequences to compare. They should be of the same length.

    Returns:
    - List of tuples (position, nucleotide_from_seq1, nucleotide_from_seq2) representing the SNPs.
    """

    # Ensure both sequences are of the same length
    if len(seq1) != len(seq2):
        raise ValueError("The sequences should be of the same length.")

    # Detect SNPs
    snps = [(i, seq1[i], seq2[i])
            for i in range(len(seq1)) if seq1[i] != seq2[i]]

    return snps

