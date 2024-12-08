import requests
import json
import os

# Scopus API Key
SCOPUS_API_KEY = "cb62daa8ea38b5a3f59f0d3f53c7b3f4"

# Base URL
BASE_URL = "https://api.elsevier.com/content/search/scopus"

# Headers
headers = {
    "X-ELS-APIKey": SCOPUS_API_KEY,
    "Accept": "application/json"
}

# Function to fetch data for a specific year
def fetch_and_save_for_year(year):
    start = 0
    all_results = []
    
    while True:
        query_params = {
            "query": f"TITLE-ABS-KEY(engineering) AND PUBYEAR IS {year}",  # Query for a specific year
            "count": 25,
            "start": start
        }
        try:
            # API request
            response = requests.get(BASE_URL, headers=headers, params=query_params)
            print(f"Fetching data for year {year}, starting from index {start}...")
            
            # Check response status
            response.raise_for_status()

            # Parse JSON
            data = response.json()
            entries = data.get("search-results", {}).get("entry", [])

            # Break if no more data
            if not entries:
                print(f"No more results for year {year}.")
                break

            # Save entries for this batch
            all_results.extend(entries)

            # Stop loop if fewer than 25 entries returned
            if len(entries) < 25:
                break

            # Update start index for pagination
            start += 25

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for year {year}: {e}")
            break

    # Save results for this year
    if all_results:
        year_folder = f"data_by_year/{year}"
        os.makedirs(year_folder, exist_ok=True)

        # Save each entry as a JSON file
        for entry in all_results:
            title = entry.get("dc:title", "No title available")
            doi = entry.get("prism:doi", "No DOI available").replace("/", "_") if entry.get("prism:doi") else "unknown"
            filename = f"{year_folder}/{doi}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=4)
            print(f"Saved: {filename}")

# Fetch data for each year
for year in range(2013, 2018):  # Years 2013 to 2017
    fetch_and_save_for_year(year)
