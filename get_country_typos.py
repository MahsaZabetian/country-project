import requests
from rapidfuzz import process

# Your GeoNames username
username = "mahsazabetian"

# Function to fetch valid country names
def fetch_country_names(username):
    url = f"http://api.geonames.org/countryInfoJSON?username={username}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [item["countryName"] for item in data.get("geonames", [])]
    except Exception as e:
        print("Error fetching data:", e)
        return []

# Function to correct typos
def correct_country(name, valid_names, threshold=80):
    if not valid_names:
        return "Country list empty"
    match = process.extractOne(name, valid_names)
    if match and match[1] >= threshold:
        return match[0]
    return "Not Found"

# Main entry point
if __name__ == "__main__":
    country_list = fetch_country_names(username)

    test_inputs = [
        "Untied States", "Cannda", "Sout Korea",
        "UK", "Venzuela", "Germny", "Ukrine"
    ]

    print("\nCorrected Country Names:\n")
    for name in test_inputs:
        corrected = correct_country(name, country_list)
        print(f"{name} → {corrected}")

