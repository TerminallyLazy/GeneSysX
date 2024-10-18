# GeneSysX: Genomic Data Analysis Gradio App Documentation

## Overview
This document provides detailed instructions for the entire Gradio app build process for GeneSysX, including recent fixes and updates. The app consists of three main functionalities: File Processing, Q&A, and Protein Visualization.

## Prerequisites
- Python 3.10 or higher
- Gradio library
- Other required libraries (biopython, py3Dmol, etc.)

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/TerminallyLazy/GeneSysX.git
   cd GeneSysX
   ```
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## App Structure
The main application is contained in `app.py`, with supporting modules in the `genesys` directory.

### File Processing
- Handles FASTA file uploads
- Processes genomic sequences
- Outputs sequence information and statistics

### Q&A
- Allows users to ask questions about uploaded genomic data
- Utilizes AI to provide relevant answers

### Protein Visualization
- Accepts PDB file uploads
- Visualizes protein structures using py3Dmol
- Customizable visualization options (background color, style, spin)

## Recent Updates and Fixes
1. Updated Gradio client URL in test scripts
2. Improved error handling in file processing
3. Enhanced Q&A functionality
4. Optimized protein visualization performance
5. Added comprehensive test suite (`verify_functionality.py`, `test_file_processing.py`)

## Running the App
To start the Gradio app:
```
python app.py
```
The app will be accessible at `http://localhost:7860` by default.

## Testing
Run the verification script to ensure all functionalities are working:
```
python verify_functionality.py
```

## Deployment
The app is currently deployed and accessible at: https://02910c43ac5541ad74.gradio.live/

## Troubleshooting
- If facing issues with Gradio version compatibility, check and update using `pip install gradio --upgrade`
- Ensure all dependencies are correctly installed and up-to-date
- For visualization issues, verify that py3Dmol is properly installed and configured

## Future Improvements
- Implement user authentication for secure access
- Expand Q&A capabilities with more advanced AI models
- Add support for additional file formats in protein visualization

## Contributing
Please refer to CONTRIBUTING.md for guidelines on how to contribute to this project.
