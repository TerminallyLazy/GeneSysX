import requests

# URL of the NCBI BLAST Common URL API
api_url = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi"

# Parameters for submitting a BLAST search
blast_params = {
    "CMD": "Put",
    "PROGRAM": "blastn",
    "DATABASE": "nt",
    "QUERY": "ATCGATCGATCG",
    "FORMAT_TYPE": "JSON"
}

# Send a POST request to submit the BLAST search
response = requests.post(api_url, data=blast_params)
response_data = response.json()

# Get the RID (Request ID) from the response
rid = response_data["RID"]
print("Search submitted. RID:", rid)

# Now, let's check the status of the search
status_params = {
    "CMD": "Get",
    "RID": rid
}

# Send a POST request to check the search status
status_response = requests.post(api_url, data=status_params)
status_data = status_response.json()

# Print the status of the search
print("Search Status:", status_data["status"])

print(response.content)
