import os
import json
import openai
from openai import OpenAI
from . import eventcreator as ec
from . import DNAToolKit as toolkit
from .env import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = "Be a bioinformatician who answers questions about a FASTA file with the given path."

functions = [
    {
        "name": "sequence_type",
        "description": "Get the type of sequences in a FASTA file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                }
            },
            "required": ["filepath"]
        },
        "returns": {
            "type": "object",
            "properties": {
                "sequence_type": {
                    "type": "string",
                    "enum": ["DNA", "RNA", "Protein"],
                }
            },
        }
    },
    {
        "name": "count_occurences",
        "description": "Count the number of nucleotides for each DNA/RNA sequence or amino acids for each protein in a FASTA file",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "transcription",
        "description": "Transcribe a DNA sequence to RNA.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "complementary",
        "description": "Find the complementary DNA sequence to a given DNA sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "reverseComplementary",
        "description": "Find the reverse complementary of a sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "gc_content",
        "description": "Calculate the GC content of a DNA/RNA sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "translation",
        "description": "Translate a DNA sequence to a protein sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "mass_calculator",
        "description": "Calculate the molecular mass of a DNA, RNA or protein sequence",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "restriction_sites",
        "description": "Find the restriction sites of a DNA sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "isoelectric_point",
        "description": "Calculate the isoelectric point of a protein sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The protein sequence."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "multiple_sequence_alignment",
        "description": "Perform multiple sequence alignment using a FASTA file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "construct_phylogenetic_tree",
        "description": "Construct a phylogenetic tree using a FASTA file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "open_reading_frames",
        "description": "Finds the forward and reverse open reading frames",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "detect_snps",
        "description": "Detect single nucleotide polymorphisms (SNPs)",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "find_motifs",
        "description": "Find motifs in a DNA sequence",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                },
                "motif": {
                    "type": "string",
                }
            },
            "required": ["filepath", "motif"]
        }
    }
]

def run_conversation(question, file_path, timeout=30):
    import logging
    import os
    from io import StringIO
    from Bio import SeqIO
    import json
    from openai import OpenAI
    from genesys import toolkit
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Starting run_conversation with question: {question}, file_path: {file_path}")

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Extract sequence IDs
        sequence_ids = [record.id for record in SeqIO.parse(StringIO(file_content), "fasta")]
        logging.debug(f"Extracted sequence IDs: {sequence_ids}")

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        messages = [
            {"role": "system", "content": "You are a helpful assistant for analyzing genomic data."},
            {"role": "user", "content": f"Here's the content of a genomic file:\n\n{file_content}\n\nQuestion: {question}"}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            timeout=timeout
        )

        answer = response.choices[0].message.content
        logging.info(f"Final answer: {answer}")

        # Check if the answer is about sequence IDs and ensure it's clear and concise
        if "sequence ID" in question.lower() and not any(id in answer for id in sequence_ids):
            answer = f"The sequence IDs in the uploaded FASTA file are: {', '.join(sequence_ids)}. {answer}"

        return answer

    except Exception as e:
        logging.error(f"An error occurred in run_conversation: {str(e)}", exc_info=True)
        # Fallback mechanism to return extracted sequence IDs if the API call fails or times out
        if "sequence ID" in question.lower():
            return f"An error occurred while processing your request, but I can tell you that the sequence IDs in the uploaded FASTA file are: {', '.join(sequence_ids)}."
        else:
            return f"An error occurred: {str(e)}"
