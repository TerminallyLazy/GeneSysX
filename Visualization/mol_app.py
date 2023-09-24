import logging
logging.basicConfig(level=logging.INFO)

import streamlit as st
from stmol import showmol
import py3Dmol

def render_mol(xyz):
    xyzview = py3Dmol.view(width=400,height=400)
    xyzview.addModel(xyz,'xyz')
    xyzview.setStyle({'stick':{}})
    xyzview.setBackgroundColor('white')#('0xeeeeee')
    xyzview.zoomTo()
    showmol(xyzview, height = 500,width=800)

def render_protein():
    # TODO: This is to be deleted.
    st.sidebar.title('Show Proteins')
    prot_str='1A2C,1BML,1D5M,1D5X,1D5Z,1D6E,1DEE,1E9F,1FC2,1FCC,1G4U,1GZS,1HE1,1HEZ,1HQR,1HXY,1IBX,1JBU,1JWM,1JWS'
    prot_list=prot_str.split(',')
    bcolor = st.sidebar.color_picker('Pick A Color', '#FFFFFF')
    protein=st.sidebar.selectbox('select protein',prot_list)
    style = st.sidebar.selectbox('style',['cartoon','line','cross','stick','sphere'])
    spin = st.sidebar.checkbox('Spin', value = True)
    xyzview = py3Dmol.view(query='pdb:'+protein)
    xyzview.setStyle({style:{'color':'spectrum'}})
    xyzview.setBackgroundColor(bcolor)
    if spin:
        xyzview.spin(True)
    else:
        xyzview.spin(False)
    xyzview.zoomTo()
    showmol(xyzview,height=500,width=800)

def render_protein_file(pdb_file_content):
    xyzview = py3Dmol.view(width=400, height=400)
    xyzview.addModel(pdb_file_content, 'pdb')
    bcolor = st.sidebar.color_picker('Pick A Color', '#FFFFFF')
    style = st.sidebar.selectbox('style',['cartoon','line','cross','stick','sphere'])
    spin = st.sidebar.checkbox('Spin', value = True)
    xyzview.setStyle({style:{'color':'spectrum'}})
    xyzview.setBackgroundColor(bcolor)
    if spin:
        xyzview.spin(True)
    else:
        xyzview.spin(False)
    xyzview.zoomTo()
    showmol(xyzview,height=500,width=800)

uploaded_files = st.sidebar.file_uploader("Upload your biological Data!", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    # Get File Extension
    extension = uploaded_file.name.split('.')[-1]
    

    

    file_data = uploaded_file.getvalue().decode("utf-8")

    # TODO: Give user options for different file types.
    
    # TODO: Asynchronously Upload Uploaded Data to S3 Data Lake.
    

    if extension == "pdb":
        render_protein_file(file_data)
    