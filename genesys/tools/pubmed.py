import requests
import xml.etree.ElementTree as ET

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def _parse_search_results(search_result: str) -> list[str]:
    """
    Parses the XML response from PubMed's ESearch API and returns a list of PMIDs.
    """
    root = ET.fromstring(search_result)
    return [id_tag.text for id_tag in root.findall('.//IdList/Id')]

def fetch_papers(query: str, max_results: int = 10) -> list:
    """
    Fetches a list of papers from PubMed based on the given query.
    This function now also returns the abstract of each paper.
    """

    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmode=xml"
    search_response = requests.get(search_url)
    id_list = _parse_search_results(search_response.text)

    ids = ','.join(id_list[:max_results])
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={ids}&retmode=xml"
    fetch_response = requests.get(fetch_url)
    root = ET.fromstring(fetch_response.text)

    papers = []
    for article in root.findall('.//PubmedArticle'):
        pmid = article.find('.//PMID').text
        title = article.find('.//ArticleTitle').text

        abstract = article.find('.//Abstract/AbstractText')
        abstract_text = abstract.text if abstract is not None else "No abstract available"
        papers.append((pmid, title, abstract_text))

    return papers