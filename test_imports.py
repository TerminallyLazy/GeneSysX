import sys
print("Python version:", sys.version)
print("Python path:", sys.path)

try:
    from genesys.tools.sequence import multiple_sequence_alignment
    print("Successfully imported multiple_sequence_alignment")
except ImportError as e:
    print("Failed to import multiple_sequence_alignment:", str(e))

try:
    from genesys.ai import run_conversation
    print("Successfully imported run_conversation")
except ImportError as e:
    print("Failed to import run_conversation:", str(e))

try:
    from genesys import toolkit
    print("Successfully imported toolkit")
except ImportError as e:
    print("Failed to import toolkit:", str(e))

print("All import tests completed")
