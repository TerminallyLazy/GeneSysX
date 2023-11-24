import collections
import re

from typing import Annotated
from typing_extensions import Doc

from Bio import AlignIO, Restriction, SeqIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import gc_fraction
from Bio.SeqUtils.IsoelectricPoint import IsoelectricPoint as IP
from Bio.SeqUtils.ProtParam import molecular_weight


def sequence_type(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
    """Determine the type of sequence in a FASTA file."""
    try:
        with open(filepath, "r") as f:
            first = list(SeqIO.parse(f, "fasta"))[0]
            seq = str(first.seq)

            if set(seq.upper()) <= set("ATGC"):
                return "DNA"
            elif set(seq.upper()) <= set("AUGC"):
                return "RNA"
            else:
                return "Protein"

    except FileNotFoundError:
        return f"File not found: {filepath}"


def count_occurences(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
    """Count the number of nucleotides for each DNA/RNA sequence or amino acids for each protein in a FASTA file.

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


def transcription(filepath: Annotated[str, Doc("Path to the FASTA file.")]):

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


def complementary(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
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

        if sequence_type(filepath) == "DNA":
            sequence = seq_record.seq
        elif sequence_type(filepath) == "RNA":
            sequence = seq_record.seq.back_transcribe()
        else:
            raise ValueError("Unable to perform operation: Uncompatible sequence type")
        complementary_sequence = str(sequence.complement())
        complementary_sequences[seq_id] = complementary_sequence

    return complementary_sequences


# Gives the reverse complementary DNA sequence to a given DNA seq

def reverseComplementary(filepath: Annotated[str, Doc("Path to the FASTA file.")]):

    if sequence_type == "DNA" or "RNA":
        reverseSeq = complementary(filepath)
    else:
        raise ValueError("Unable to perform operation: Uncompatible sequence type")

    # Convert dictionary to list of tuples, reverse the list, and convert back to dictionary
    reverseSeq = dict(reversed(list(reverseSeq.items())))

    return reverseSeq

# The combined above two functions into one GC content calculator


def gc_content(filepath: Annotated[str, Doc("Path to the FASTA file.")]):

    sequences = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))
    gc_contents = {}

    for seq_id, seq_record in sequences.items():
        if sequence_type(filepath) == "Protein":
            raise ValueError("Unable to perform operation: Not a DNA sequence")

        sequence = seq_record.seq
        gc_content = round(gc_fraction(sequence) * 100, 2)
        gc_contents[seq_id] = gc_content

    return gc_contents


def translation(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
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
        if sequence_type(filepath) == "Protein":
            raise ValueError("Unable to perform operation: Not a DNA sequence")
        elif sequence_type(filepath) == "RNA":
            sequence = seq_record.seq
        elif sequence_type(filepath) == "DNA":
            sequence = seq_record.seq.transcribe()

        num_n_to_add = 3 - (len(sequence) % 3)
        sequence = sequence + Seq("N" * num_n_to_add)

        translated_sequence = str(sequence.translate())
        translated_sequences[seq_id] = translated_sequence

    return translated_sequences


def find_invalid_amino_acid(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
    invalid_positions = []
    for i, aa in enumerate(sequence):
        if aa not in "ACDEFGHIKLMNPQRSTVWY":
            invalid_positions.append((aa, i))
    return invalid_positions


def mass_calculator(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
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
                masses[seq_id] = molecular_weight(sequence, "DNA")
            elif seq_type == "RNA":
                masses[seq_id] = molecular_weight(sequence, "RNA")
            elif seq_type == "Protein":
                invalid_positions = find_invalid_amino_acid(sequence)
                if invalid_positions:
                    error_message = f"Ambiguous amino acid(s) found in sequence {seq_id}: {', '.join(f'{aa} at position {pos}' for aa, pos in invalid_positions)}"
                    raise ValueError(error_message)
                masses[seq_id] = molecular_weight(sequence, "protein")
        except ValueError as e:
            masses[seq_id] = str(e)

    return masses

# TO DO : revist this function

def open_reading_frames(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
    """
    Find and translate all open reading frames (ORFs) in a DNA sequence.

    Parameters:
    - filepath: Path to the FASTA file containing the DNA sequence.

    Returns:
    - A dictionary where keys are sequence IDs and values are dictionaries with ORF information.
    """
    
    orfs_results = {}  # Dictionary to store results for multiple sequences
    for record in SeqIO.parse(filepath, "fasta"):
        sequence = record.seq
        sequence_name = record.id

        def find_orfs(sequence):
            orfs = []
            for i in range(len(sequence) - 2):
                if sequence[i:i+3] == 'ATG':
                    orf = 'ATG'
                    x = 3
                    while i+x < len(sequence) and sequence[i+x:i+3+x] not in ['TAG', 'TAA', 'TGA']:
                        orf += sequence[i+x:i+3+x]
                        x += 3
                    if len(orf) > 90:
                        orfs.append((i, orf, len(orf)))
            return orfs

        forward_orfs = find_orfs(sequence)
        reverse_sequence = sequence.reverse_complement()
        reverse_orfs = find_orfs(reverse_sequence)

        all_orfs = forward_orfs + [(len(sequence) - info[0] - info[2], info[1], info[2]) for info in reverse_orfs]

        orfs_dict = {}
        for idx, orf_info in enumerate(all_orfs, start=1):
            sequence_number = idx
            start_position = orf_info[0]
            frame = ((start_position % 3) + 1) if sequence_number <= len(forward_orfs) else ((len(sequence) - start_position - orf_info[2]) % 3) + 1
            sequence = orf_info[1]
            length = orf_info[2]

            orf_seq = Seq(sequence)
            protein_seq = orf_seq.translate()

            # Determine if it's a forward or reverse ORF
            orf_type = "Forward" if sequence_number <= len(forward_orfs) else "Reverse"

            orfs_dict[sequence_number] = {
                "Start position": start_position,
                "Frame": frame,
                "Sequence": sequence,
                "Length": length,
                "Protein Sequence": str(protein_seq),
                "Sequence ID": sequence_name,  # Include the sequence ID
                "ORF Type": orf_type  # Add forward/reverse information
            }

        if sequence_name in orfs_results:
            orfs_results[sequence_name].update(orfs_dict)
        else:
            orfs_results[sequence_name] = orfs_dict

    return orfs_results



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


def restriction_sites(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
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

def isoelectric_point(filepath: Annotated[str, Doc("Path to the FASTA file.")]):

    sequences = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))
    isoelectric_points = {}

    for seq_id, seq_record in sequences.items():
        sequence = seq_record.seq
        seq_type = sequence_type(filepath)

        if seq_type == "Protein":
            isoelectric_points[seq_id] = IP(sequence).pi()
        elif seq_type == "DNA":
            isoelectric_points[seq_id] = IP(sequence.translate()).pi()
        elif seq_type == "RNA":
            isoelectric_points[seq_id] = IP(sequence.translate()).pi()
        
    return isoelectric_points

def multiple_sequence_alignment(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
    """
    Perform multiple sequence alignment on a FASTA file.

    Parameters:
    - filepath: Path to the FASTA file containing the sequences to align.

    Returns:
    - A MultipleSeqAlignment object containing the aligned sequences.
    """
    with open(filepath, "r") as text_file:
        alignment = AlignIO.read(text_file, "fasta")

    aligned_seqs = []

    for record in alignment:
        if sequence_type(filepath) == "Protein":
            aligned_seqs.append(record)
        elif sequence_type(filepath) == "DNA":
            aligned_seqs.append(SeqRecord(record.seq.translate(), id=record.id))
            

    return MultipleSeqAlignment(aligned_seqs)

# REVISIT THIS FUNCTION WITH CHARLIE


def detect_snps(filepath: Annotated[str, Doc("Path to the FASTA file.")]):
    """
    Detect singular nucleotide polymorphisms (SNPs) between multiple DNA sequences in a FASTA file.

    Parameters:
    - filepath: Path to the FASTA file containing DNA sequences to compare.

    Returns:
    - Dictionary where the keys are sequence IDs and values are dictionaries of SNP positions and nucleotides.
    """

    # Parse sequences from the FASTA file
    records = list(SeqIO.parse(filepath, "fasta"))
    sequences = [str(record.seq) for record in records]
    sequence_ids = [record.id for record in records]

    # Ensure all sequences are of the same length
    seq_length = len(sequences[0])
    if not all(len(seq) == seq_length for seq in sequences):
        raise ValueError("All sequences should be of the same length.")

    # Detect SNPs for each sequence
    snps = collections.defaultdict(dict)

    for i in range(seq_length):
        nucleotides = [seq[i] for seq in sequences]
        if len(set(nucleotides)) > 1:
            for j, seq_id in enumerate(sequence_ids):
                snps[seq_id][f"position {i}"] = nucleotides[j]

    return snps

def find_motifs(
    filepath: Annotated[str, Doc("Path to the FASTA file.")],
    motif: Annotated[str, Doc("Motif to search for.")]
):
    """Find the given motif in the sequences in the FASTA files."""
    motif_positions = {}

    for record in SeqIO.parse(filepath, "fasta"):
        sequence_str = str(record.seq)
        matches = [match.start() for match in re.finditer(motif, sequence_str)]
        motif_positions[record.id] = matches

    return motif_positions
