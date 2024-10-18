import gradio as gr
from app import create_interface

if __name__ == "__main__":
    iface = create_interface()
    iface.launch(share=True)
