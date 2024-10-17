import logging
logging.basicConfig(level=logging.INFO)
import gradio as gr
import py3Dmol
from . import DNAToolKit
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Phylo
import matplotlib.pyplot as plt
import io

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

    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    img_buf.seek(0)

    return tree, img_buf

def render_protein_file(pdb_file_content, style, bcolor, spin):
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

def create_visuals_interface():
    with gr.Blocks() as interface:
        gr.Markdown("# Protein and Molecule Visualization")

        with gr.Tab("Protein Visualization"):
            pdb_input = gr.File(label="Upload PDB file")
            style_input = gr.Dropdown(choices=['cartoon','line','cross','stick','sphere'], label="Style", value='cartoon')
            color_input = gr.ColorPicker(label="Background Color", value='#FFFFFF')
            spin_input = gr.Checkbox(label="Spin", value=True)
            protein_output = gr.HTML(label="Protein Visualization")
            render_protein_button = gr.Button("Render Protein")
            render_protein_button.click(
                lambda file, style, color, spin: render_protein_file(file.read().decode("utf-8"), style, color, spin),
                inputs=[pdb_input, style_input, color_input, spin_input],
                outputs=[protein_output]
            )

        with gr.Tab("Molecule Visualization"):
            xyz_input = gr.Textbox(label="Enter XYZ coordinates")
            mol_output = gr.HTML(label="Molecule Visualization")
            render_mol_button = gr.Button("Render Molecule")
            render_mol_button.click(render_mol, inputs=[xyz_input], outputs=[mol_output])

        with gr.Tab("Phylogenetic Tree"):
            fasta_input = gr.File(label="Upload FASTA file")
            tree_output = gr.Image(label="Phylogenetic Tree")
            construct_tree_button = gr.Button("Construct Phylogenetic Tree")
            construct_tree_button.click(
                lambda file: construct_phylogenetic_tree(file.name)[1],
                inputs=[fasta_input],
                outputs=[tree_output]
            )

    return interface
