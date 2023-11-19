import requests
import xml.etree.ElementTree as ET

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def parse_search_results(search_result):
    root = ET.fromstring(search_result)
    return [id_tag.text for id_tag in root.findall('.//IdList/Id')]

def fetch_papers(query: str , max_results=10) -> list:
    # Search for papers
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmode=xml"
    search_response = requests.get(search_url)
    id_list = parse_search_results(search_response.text)

    # Fetch paper details
    ids = ','.join(id_list[:max_results])
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={ids}&retmode=xml"
    fetch_response = requests.get(fetch_url)
    root = ET.fromstring(fetch_response.text)

    papers = []
    for article in root.findall('.//PubmedArticle'):
        pmid = article.find('.//PMID').text
        title = article.find('.//ArticleTitle').text
        papers.append((pmid, title))
    
    return papers

print(fetch_papers("genomics, cancer, crispr"))