# -*- coding: utf-8 -*-
import requests
import json
from rapidfuzz import process

# Common country names that may be used interchangeably
ALTERNATE_NAMES = {
    "UK": "United Kingdom",
    "USA": "United States",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "Russia": "Russian Federation",
    # etc.
}

def fetch_country_names(username):
    """
    Fetches official country names from GeoNames API.
    
    Args:
        username (str): GeoNames API username.
    
    Returns:
        list: List of country names.
    """
    try:
        url = f"http://api.geonames.org/countryInfoJSON?username={username}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [item['countryName'] for item in data.get('geonames', [])]
    except Exception as e:
        print(f"Error fetching country names: {e}")
        return []

def correct_typo(name, valid_names, threshold=85):
    """
    Corrects typos or variations in country names.
    
    Args:
        name (str): The country name to correct.
        valid_names (list): List of valid country names.
        threshold (int): Minimum similarity score to accept a match.
    
    Returns:
        str: Corrected country name or "Not Found".
    """
    if name in ALTERNATE_NAMES:
        return ALTERNATE_NAMES[name]
    
    best_match = process.extractOne(name, valid_names)
    if best_match and best_match[1] >= threshold:
        return best_match[0]
    return "Not Found"

if __name__ == "__main__":
    username = "mahsazabetian"  # This could become an environment variable or input parameter
    valid_countries = fetch_country_names(username)

    test_inputs = ['Untied States', 'UK', 'Russsia', 'Venzuela', 'South Corea']

    results = []

    for name in test_inputs:
        corrected = correct_typo(name, valid_countries)
        results.append({
            "original": name,
            "corrected": corrected
        })
        print("{} → {}".format(name, corrected))

    with open("corrected_countries.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print("Results saved to corrected_countries.json")
