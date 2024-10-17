import gradio as gr

def display_structure(pdb_string):
    # Create an HTML string that uses NGL to display the PDB
    html = f"""
    <script src="https://unpkg.com/ngl@2.0.0-dev.38/dist/ngl.js"></script>
    <div id="viewport" style="width:100%; height:100%;"></div>
    <script>
        var stage = new NGL.Stage("viewport");
        stage.loadFile("data:text/plain,{pdb_string}", {{ ext: "pdb" }}).then(function (component) {{
            component.addRepresentation("cartoon");
            component.autoView();
        }});
        </script>
        """
    return html

def create_ngl_interface():
    with gr.Blocks() as interface:
        gr.Markdown("# Protein Structure Visualization")
        pdb_input = gr.Textbox(label="Enter PDB string")
        visualize_button = gr.Button("Visualize Structure")
        output = gr.HTML(label="Protein Structure")

        visualize_button.click(display_structure, inputs=[pdb_input], outputs=[output])

    return interface

# Fake PDB string for testing
pdb_string = """
HEADER    WATER                                24-FEB-07   1WAT
CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1
ATOM      1  O   HOH A   1       0.000   0.000   0.000  1.00 20.00           O
ATOM      2  H1  HOH A   1       0.000   0.740   0.587  1.00 20.00           H
ATOM      3  H2  HOH A   1       0.000   0.740  -0.587  1.00 20.00           H
END
"""

if __name__ == "__main__":
    interface = create_ngl_interface()
    interface.launch()
