"""
This testing module is to make sure that the prompts and the function
descriptions defined in `tools.pubmed` results in the behavior that we expect.
"""

import os
import pytest
import openai
from genesys import tools
from genesys.tools.pubmed import fetch_papers
import time
import pytest

def test_perform_search():
    time.sleep(1)
    query = "genomics"
    result = fetch_papers(query=query)

    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, tuple)
    
def test_perform_search_multiple_queries():
    time.sleep(1)
    query = "genomics, cancer, crispr"
    result = fetch_papers(query=query)

    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, tuple)

def test_perform_search_with_assistant():
    pass

if __name__ == "__main__":
    pytest.main()