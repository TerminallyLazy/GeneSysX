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
    logging.info(f"Rendering protein file with parameters: bcolor={bcolor}, style={style}, spin={spin}")
    try:
        pdbview = py3Dmol.view(width=400, height=400)
        logging.info("py3Dmol view created successfully")
        pdbview.addModel(pdb_file_content, 'pdb')
        logging.info("Model added to view")
        pdbview.setStyle({style:{'color':'spectrum'}})
        logging.info(f"Style set to {style}")
        pdbview.setBackgroundColor(bcolor)
        logging.info(f"Background color set to {bcolor}")
        pdbview.spin(spin)
        logging.info(f"Spin set to {spin}")
        pdbview.zoomTo()
        logging.info("Zoom applied")
        rendered_html = pdbview._make_html()
        logging.info(f"Protein rendered successfully. HTML content generated.")
        return rendered_html
    except Exception as e:
        logging.error(f"Error in render_protein_file: {str(e)}", exc_info=True)
        raise

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
            logging.info(f"Visualize protein called with file: {file}, bcolor: {bcolor}, style: {style}, spin: {spin}")
            try:
                import py3Dmol
                logging.info("py3Dmol imported successfully")
            except ImportError as e:
                logging.error(f"Error importing py3Dmol: {str(e)}")
                return "Error: py3Dmol is not properly installed or accessible. Please check your installation."

            if file is not None:
                try:
                    logging.info(f"Attempting to open file: {file.name}")
                    with open(file.name, 'r') as f:
                        pdb_content = f.read()
                    logging.info(f"File read successfully. Content length: {len(pdb_content)} characters")

                    logging.info(f"Rendering protein with parameters: bcolor={bcolor}, style={style}, spin={spin}")
                    rendered_protein = render_protein_file(pdb_content, bcolor, style, spin)
                    logging.info(f"Protein rendered successfully. Rendered content length: {len(rendered_protein)} characters")

                    iframe_content = f'<iframe id="protein-viz" style="width:100%; height:400px; border:none;" srcdoc="{rendered_protein}"></iframe>'
                    logging.info(f"Created iframe content. Length: {len(iframe_content)} characters")
                    return iframe_content
                except FileNotFoundError:
                    error_msg = f"Error: File {file.name} not found. Please ensure the file exists and you have permission to read it."
                    logging.error(error_msg)
                    return error_msg
                except IOError as e:
                    error_msg = f"Error reading file {file.name}: {str(e)}"
                    logging.error(error_msg)
                    return error_msg
                except Exception as e:
                    error_msg = f"Unexpected error processing file {file.name}: {str(e)}"
                    logging.error(error_msg, exc_info=True)
                    return error_msg
            else:
                logging.warning("No file uploaded.")
                return "No file uploaded. Please upload a PDB file."

        visualize_button.click(visualize_protein, inputs=[pdb_input, bcolor_input, style_input, spin_input], outputs=protein_output)

    return demo
