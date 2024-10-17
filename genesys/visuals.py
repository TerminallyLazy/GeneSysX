import logging
logging.basicConfig(level=logging.INFO)
import py3Dmol
from . import DNAToolKit
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Phylo
import matplotlib.pyplot as plt
import gradio as gr

def count_clades(tree):
    terminals = tree.get_terminals()
    clade_names = set()
    for terminal in terminals:
        clade = tree.common_ancestor([terminal])
        clade_names.add(clade.name)

    return len(clade_names)

def construct_phylogenetic_tree(filepath):
    """
    Construct a phylogenetic tree from a FASTA file.

    Parameters:
    - filepath: Path to the FASTA file containing the sequences to align.

    Returns:
    - A Phylo.Tree object representing the phylogenetic tree.
    """

    aligned_seqs = DNAToolKit.multiple_sequence_alignment(filepath)
    calculator = DistanceCalculator("identity")
    constructor = DistanceTreeConstructor(calculator)
    tree = constructor.build_tree(aligned_seqs)


    if count_clades(tree) <= 25:
        fig, ax = plt.subplots(figsize=(100, 50))
    elif 25 < count_clades(tree) <= 50:
        fig, ax = plt.subplots(figsize=(100, 250))
    elif 50 < count_clades(tree) <= 100:
        fig, ax = plt.subplots(figsize=(100, 500))

    Phylo.draw(tree, axes=ax)

    fig.savefig("phylogenetic_tree.png")


    return tree


def render_protein_file(pdb_file_content, bcolor='#FFFFFF', style='cartoon', spin=True):
    pdbview = py3Dmol.view(width=400, height=400)
    pdbview.addModel(pdb_file_content, 'pdb')
    pdbview.setStyle({style:{'color':'spectrum'}})
    pdbview.setBackgroundColor(bcolor)
    pdbview.spin(spin)
    pdbview.zoomTo()
    return pdbview.render()

def render_mol(xyz):
    xyzview = py3Dmol.view(width=400,height=400)
    xyzview.addModel(xyz,'xyz')
    xyzview.setStyle({'stick':{}})
    xyzview.setBackgroundColor('white')#('0xeeeeee')
    xyzview.zoomTo()
    return xyzview.render()

def create_protein_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Protein Visualization")
        with gr.Row():
            pdb_input = gr.File(label="Upload PDB file")
            protein_output = gr.HTML(label="Protein Visualization")
        with gr.Row():
            bcolor_input = gr.ColorPicker(label="Background Color", value='#FFFFFF')
            style_input = gr.Dropdown(label="Style", choices=['cartoon','line','cross','stick','sphere'], value='cartoon')
            spin_input = gr.Checkbox(label="Spin", value=True)
        visualize_button = gr.Button("Visualize Protein")

        def visualize_protein(file, bcolor, style, spin):
            if file is not None:
                pdb_content = file.read().decode("utf-8")
                return render_protein_file(pdb_content, bcolor, style, spin)
            return "No file uploaded"

        visualize_button.click(visualize_protein, inputs=[pdb_input, bcolor_input, style_input, spin_input], outputs=protein_output)

    return demo
