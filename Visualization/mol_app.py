import logging
logging.basicConfig(level=logging.INFO)

import gradio as gr
import py3Dmol

def render_mol(xyz):
    xyzview = py3Dmol.view(width=400,height=400)
    xyzview.addModel(xyz,'xyz')
    xyzview.setStyle({'stick':{}})
    xyzview.setBackgroundColor('white')#('0xeeeeee')
    xyzview.zoomTo()
    return xyzview.render()

def render_protein(protein, style, bcolor, spin):
    xyzview = py3Dmol.view(query='pdb:' + protein)
    xyzview.setStyle({style: {'color': 'spectrum'}})
    xyzview.setBackgroundColor(bcolor)
    xyzview.spin(spin)
    xyzview.zoomTo()
    return xyzview.render()

def render_protein_file(pdb_file_content, style, bcolor, spin):
    pdbview = py3Dmol.view(width=400, height=400)
    pdbview.addModel(pdb_file_content, 'pdb')
    pdbview.setStyle({style:{'color':'spectrum'}})
    pdbview.setBackgroundColor(bcolor)
    pdbview.spin(spin)
    pdbview.zoomTo()
    return pdbview.render()

def process_file(file):
    if file is not None:
        extension = file.name.split('.')[-1]
        file_data = file.read().decode("utf-8")

        # TODO: Give user options for different file types.

        # TODO: Asynchronously Upload Uploaded Data to S3 Data Lake.

        if extension == "pdb":
            return file_data
    return None

def create_mol_interface():
    with gr.Blocks() as interface:
        gr.Markdown("# Molecule and Protein Visualization")

        with gr.Tab("Render Molecule"):
            xyz_input = gr.Textbox(label="Enter XYZ coordinates")
            mol_output = gr.HTML(label="Molecule Visualization")
            render_mol_button = gr.Button("Render Molecule")
            render_mol_button.click(render_mol, inputs=[xyz_input], outputs=[mol_output])

        with gr.Tab("Show Proteins"):
            prot_str='1A2C,1BML,1D5M,1D5X,1D5Z,1D6E,1DEE,1E9F,1FC2,1FCC,1G4U,1GZS,1HE1,1HEZ,1HQR,1HXY,1IBX,1JBU,1JWM,1JWS'
            prot_list = prot_str.split(',')
            protein_input = gr.Dropdown(choices=prot_list, label="Select protein")
            style_input = gr.Dropdown(choices=['cartoon', 'line', 'cross', 'stick', 'sphere'], label="Style")
            color_input = gr.ColorPicker(label="Background Color", value='#FFFFFF')
            spin_input = gr.Checkbox(label="Spin", value=True)
            protein_output = gr.HTML(label="Protein Visualization")
            render_protein_button = gr.Button("Render Protein")
            render_protein_button.click(render_protein, inputs=[protein_input, style_input, color_input, spin_input], outputs=[protein_output])

        with gr.Tab("Upload PDB File"):
            file_input = gr.File(label="Upload your biological Data!")
            pdb_style_input = gr.Dropdown(choices=['cartoon', 'line', 'cross', 'stick', 'sphere'], label="Style")
            pdb_color_input = gr.ColorPicker(label="Background Color", value='#FFFFFF')
            pdb_spin_input = gr.Checkbox(label="Spin", value=True)
            pdb_output = gr.HTML(label="PDB Visualization")
            render_pdb_button = gr.Button("Render PDB")
            render_pdb_button.click(
                lambda file, style, color, spin: render_protein_file(process_file(file), style, color, spin),
                inputs=[file_input, pdb_style_input, pdb_color_input, pdb_spin_input],
                outputs=[pdb_output]
            )

    return interface

if __name__ == "__main__":
    interface = create_mol_interface()
    interface.launch()
