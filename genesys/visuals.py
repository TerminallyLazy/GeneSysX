import logging
logging.basicConfig(level=logging.INFO)
import streamlit as st
from stmol import showmol
import py3Dmol
from . import DNAToolKit
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import Phylo
import matplotlib.pyplot as plt

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


def render_protein_file(pdb_file_content):
    pdbview = py3Dmol.view(width=400, height=400)
    pdbview.addModel(pdb_file_content, 'pdb')
    bcolor = st.sidebar.color_picker('Pick A Background Color', '#FFFFFF')
    style = st.sidebar.selectbox('style',['cartoon','line','cross','stick','sphere'])
    spin = st.sidebar.checkbox('Spin', value = True)
    pdbview.setStyle({style:{'color':'spectrum'}})
    pdbview.setBackgroundColor(bcolor)
    if spin:
        pdbview.spin(True)
    else:
        pdbview.spin(False)
    pdbview.zoomTo()
    showmol(pdbview,height=500,width=800)

def render_mol(xyz):
    xyzview = py3Dmol.view(width=400,height=400)
    xyzview.addModel(xyz,'xyz')
    xyzview.setStyle({'stick':{}})
    xyzview.setBackgroundColor('white')#('0xeeeeee')
    xyzview.zoomTo()
    showmol(xyzview, height = 500,width=800)

