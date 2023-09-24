import streamlit as st
from st_display import st_display

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

    # Use st_display to display the HTML in Streamlit
    st_display(html, width=600, height=400)

# Fake PDB string for testing
pdb_string = """
HEADER    WATER                                24-FEB-07   1WAT              
CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1          
ATOM      1  O   HOH A   1       0.000   0.000   0.000  1.00 20.00           O  
ATOM      2  H1  HOH A   1       0.000   0.740   0.587  1.00 20.00           H  
ATOM      3  H2  HOH A   1       0.000   0.740  -0.587  1.00 20.00           H  
END
"""
display_structure(pdb_string)