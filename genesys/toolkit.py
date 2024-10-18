# Import necessary libraries
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction
from Bio.SeqUtils import molecular_weight
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio import Align
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

# Define functions that are called in ai.py

def sequence_type(filepath):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            seq = record.seq.upper()
            if set(seq).issubset({'A', 'C', 'G', 'T'}):
                return {"sequence_type": "DNA"}
            elif set(seq).issubset({'A', 'C', 'G', 'U'}):
                return {"sequence_type": "RNA"}
            else:
                return {"sequence_type": "Protein"}

def count_occurences(filepath):
    counts = {}
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            seq = record.seq.upper()
            for char in set(seq):
                if char not in counts:
                    counts[char] = 0
                counts[char] += seq.count(char)
    return counts

def transcription(filepath):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            return str(record.seq.transcribe())

def complementary(filepath):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            return str(record.seq.complement())

def reverseComplementary(filepath):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            return str(record.seq.reverse_complement())

def gc_content(filepath):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            return gc_fraction(record.seq) * 100

def translation(filepath):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            return str(record.seq.translate())

def mass_calculator(filepath):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            return molecular_weight(record.seq)

def restriction_sites(filepath):
    return "Restriction sites analysis not implemented yet."

def isoelectric_point(filepath):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            protparam = ProteinAnalysis(str(record.seq))
            return protparam.isoelectric_point()

def multiple_sequence_alignment(filepath):
    aligner = Align.MultipleSeqAlignment()
    with open(filepath, 'r') as file:
        sequences = list(SeqIO.parse(file, 'fasta'))
        aligner.add_sequences(sequences)
    return str(aligner)

def construct_phylogenetic_tree(filepath):
    with open(filepath, 'r') as file:
        sequences = list(SeqIO.parse(file, 'fasta'))

    aligner = Align.MultipleSeqAlignment()
    aligner.add_sequences(sequences)

    calculator = DistanceCalculator('identity')
    dm = calculator.get_distance(aligner)

    constructor = DistanceTreeConstructor()
    tree = constructor.upgma(dm)

    return tree.as_phyloxml()

def open_reading_frames(filepath):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            orfs = []
            seq = record.seq
            for strand, nuc in [(+1, seq), (-1, seq.reverse_complement())]:
                for frame in range(3):
                    for pro in nuc[frame:].translate().split("*"):
                        if len(pro) >= 100:
                            orfs.append(f"{pro}")
    return orfs

def detect_snps(filepath):
    return "SNP detection requires multiple sequences or a reference sequence."

def find_motifs(filepath, motif):
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            seq = str(record.seq)
            positions = [i for i in range(len(seq)) if seq.startswith(motif, i)]
            return positions

def extract_sequence_ids(file_input):
    sequence_ids = []
    try:
        # Try to open as a file path
        with open(file_input, 'r') as file:
            for record in SeqIO.parse(file, 'fasta'):
                sequence_ids.append(record.id)
    except (TypeError, IOError):
        # If not a file path, treat as StringIO object
        for record in SeqIO.parse(file_input, 'fasta'):
            sequence_ids.append(record.id)
    return sequence_ids
