import logging
logging.basicConfig(level=logging.INFO)
import streamlit as st
from stmol import showmol
import py3Dmol

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