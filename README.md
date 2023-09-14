# GeneSys AI

GeneSys AI is an innovative and versatile tool designed to empower bioinformaticians, researchers, clinicians, and students in their genomics and bioinformatics endeavors. This chatbot harnesses the power of GPT (Generative Pre-trained Transformer) technology to provide a user-friendly, conversational interface for a wide range of genomic analysis tasks.

## Key Features:

FASTA File Processing: Users can easily upload FASTA files containing DNA or protein sequences for various analytical tasks.

FASTA File Processing: Users can easily upload FASTA files containing DNA or protein sequences for various analytical tasks.

Genomic Processing: The chatbot offers an extensive suite of bioinformatics functions, including:

Sequence translation: Converts DNA sequences into protein sequences.
Transcription: Transcribes DNA sequences into RNA sequences.
Restriction site detection: Identifies reverse palindromic DNA sequences, often indicating potential cutting sites for restriction enzymes.
Multiple Sequence Alignment: Aligns multiple sequences for comparative analysis.
SNP detection: Detects Single Nucleotide Polymorphisms (SNPs) in DNA sequences.
Primer Design Automation: Automates the design of primers for PCR experiments.
BLAST searches: Implements various BLAST algorithms for sequence similarity searches.

## General Data (.csv, .pdf, tabulated data, etc):

- [x] Display the dataframe
- [ ] Create and edit dataframes
    - [ ] Creating new columns
    - [ ] Deleting columns
    - [ ] Creating new rows
    - [ ] Deleting rows
    - [ ] Renaming columns
    - [ ] Renaming rows
    - [ ] Merging Dataframes: Implement dataframe merging or joining operations (e.g., inner, outer, left, right joins).
    - [ ] Sorting Dataframes: Allow users to sort dataframes based on one or more columns.
    - [ ] Aggregating Data: Provide functions for data aggregation and group-by operations.
    - [ ] Pivot Tables: Support the creation of pivot tables for summarizing and reshaping data.
    - [ ] Filtering Data: Enable users to filter data based on specific conditions or criteria.
    - [ ] Data Transposition: Allow users to transpose dataframes (rows become columns, and vice versa).
    - [ ] Data Type Conversion: Support conversion between different data types for dataframe columns.
    - [ ] Data Validation: Implement data validation checks to ensure data integrity.
    - [ ] Data Sampling: Allow users to randomly sample data from dataframes.
- [ ] Data Visualization
    - [ ] Implement data visualization tools for exploring and visualizing datasets.
    - [ ] Generate interactive charts and plots.
- [ ] Statistical Analysis
    - [ ] Provide statistical analysis functions for data summary and hypothesis testing.
    - [ ] Calculate descriptive statistics (mean, median, standard deviation, etc.).
- [ ] Export and Import
    - [ ] Enable data export in various formats (CSV, Excel, JSON, etc.).
    - [ ] Support data import from external sources and formats.

### Long Term Implementations:
- [ ] Machine Learning Integration
    - [ ] Incorporate machine learning algorithms for predictive modeling and classification.
    - [ ] Allow users to train and evaluate machine learning models on their data.
- [ ] Data Cleaning
    - [ ] Implement data cleaning and preprocessing functions (e.g., handling missing values, outliers).
    - [ ] Offer data imputation techniques.
- [ ] Time Series Analysis
    - [ ] Provide tools for time series data analysis, including trend analysis and forecasting.
    - [ ] Implement time series decomposition and visualization.


## Genomic Processing
- [x] Implement function calling to call functions from DNA Tool Kit
    - [x] Compute the complementary DNA sequence of a given DNA sequence
    - [x] Implement mRNA transcription
    - [x] Implement mRNA to protein translation
    - [x] Count and return the number of nucleotides
    - [x] Calculate the GC content of a DNA sequence and also calculate the GC content in subsections of the sequence if k is specified
    - [x] Calculate the total mass of a protein sequence based on amino acid masses
    - [x] Compute the Hamming distance between two DNA sequences of the same length
    - [x] Identifiy open reading frames (ORFs) in a DNA sequence and translate them into protein sequences 
    - [x] Implement restriction site detection
        - [ ] Further it by suggesting respective restriction enzymes
    - [ ] Implement Multiple Sequence Alignment
    - [ ] Generate phylogenetic trees from MSA
    - [ ] 3D Protein Structure Visualization
    - [ ] SNP (Single Nucleotide Polymorphism) detection
    - [ ] Primer Design Automation
    - [ ] BLAST implementation
        - [ ] BLASTn
        - [ ] BLASTp
        - [ ] BLASTx
        - [ ] tBLASTn
        - [ ] tBLASTx
        - [ ] BLAST2Seq
    - [ ] Gene Ontology enrichment analysis ?
    - [ ] Allow users to edit the gene sequence

    ### Long Term Implementations:
    - [ ] Predict the pathogenicity of genetic variants associated with diseases
    - [ ] Help users identify potential off-target sites for CRISPR-Cas9 genome editing
    - [ ] Automatically annotate genetic variants with functional consequences
    - [ ] Predict interactions between drugs and target proteins based on genomic data
    - [ ] Calculate allele frequencies of genetic variants within populations or cohorts
    - [ ] Allow users to perform molecular docking simulations for predicting how small molecules interact with proteins
    - [ ] Protein-Protein Interaction Prediction: Implement algorithms to predict protein-protein interactions based on protein sequences or structures
    - [ ] Support analysis of RNA-Seq data, including differential gene expression analysis and transcript quantification
    - [ ] More storage efficient data structures for nucleotide data solution.

