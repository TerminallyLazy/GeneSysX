# Gradio Conversion Plan for GeneSysX

## 1. Setup and Environment

1.1. Ensure Python 3.10 or higher is installed
1.2. Install Gradio: `pip install gradio`
1.3. Update requirements.txt to include Gradio and remove Streamlit

## 2. Main Application (app.py)

2.1. Replace Streamlit imports with Gradio:
   ```python
   import gradio as gr
   ```

2.2. Create a main Gradio interface:
   ```python
   def main():
       with gr.Blocks() as demo:
           # Add components here
       return demo

   if __name__ == "__main__":
       main().launch()
   ```

2.3. Convert file upload functionality:
   - Use `gr.File()` for FASTA, CSV, and PDB file uploads
   - Implement file processing functions

2.4. Implement user authentication (if needed):
   - Use Gradio's `gr.Auth()` for basic authentication

2.5. Convert CSV data querying:
   - Implement text input for queries using `gr.Textbox()`
   - Use `gr.DataFrame()` to display results

2.6. Add logging functionality:
   - Implement custom logging to file or console

## 3. Environment Variables (env.py)

3.1. Replace Streamlit secrets with environment variables:
   - Use `os.environ` or `dotenv` library for managing environment variables

3.2. Update `load_dotenv()` function to work with Gradio

## 4. Visualizations (visuals.py)

4.1. Convert molecular and phylogenetic visualizations:
   - Use `gr.Plot()` for displaying matplotlib figures
   - Implement custom components for 3D molecular rendering (py3Dmol, stmol)

4.2. Create functions for visualization outputs:
   - Implement clade counting, phylogenetic tree construction, and protein structure visualization

4.3. Save visualization outputs:
   - Use Gradio's file download functionality to save PNG files

## 5. Visualization Directory Files

5.1. Combine functionality from main.py, ngl_app.py, and mol_app.py into a single Gradio application:
   - Use `gr.Tabs()` to organize different visualization types

5.2. Implement file upload for PDB files:
   - Use `gr.File()` for PDB file uploads

5.3. Create customization options:
   - Use `gr.Dropdown()`, `gr.Slider()`, and `gr.Checkbox()` for visualization options

5.4. Integrate py3Dmol, stmol, and NGL libraries:
   - Use `gr.HTML()` or custom components to render 3D visualizations

## 6. Testing and Debugging

6.1. Implement unit tests for core functions
6.2. Create integration tests for the Gradio interface
6.3. Test file upload and processing with various file types and sizes
6.4. Verify visualization outputs and interactivity

## 7. Documentation and README Update

7.1. Update project documentation to reflect Gradio usage
7.2. Provide instructions for running the Gradio application
7.3. Document any changes in functionality or user interaction

## 8. Deployment Considerations

8.1. Update deployment scripts or configurations for Gradio
8.2. Consider using `share=True` in `launch()` for easy sharing during development
8.3. Plan for proper storage management of generated visualizations

## 9. Future Enhancements

9.1. Support for additional file types
9.2. Implement asynchronous uploads to an S3 Data Lake
9.3. Enhance error handling and user feedback

This plan outlines the steps to convert the GeneSysX project from Streamlit to Gradio, maintaining existing functionality while leveraging Gradio's features for creating interactive web interfaces and visualizations.
