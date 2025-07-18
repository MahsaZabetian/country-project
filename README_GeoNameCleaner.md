
# Geo Name Cleaner

**Version:** 1.0.1 
 Author: Mahsa Zabetian 
 License: MIT 
 Status: Production-ready 

A Python-based tool to detect and correct typos in country names using a combination of:

- Alternate name mappings 
- Fuzzy matching (via [RapidFuzz](https://github.com/maxbachmann/RapidFuzz)) 
- Official country list from the [GeoNames.org](https://www.geonames.org/) API 

---

## Features

- Detects and corrects typos in country names (e.g. "Untied States" → "United States")
- Supports official and alternate names (e.g. "UK" → "United Kingdom")
- Uses fuzzy string matching for approximate correction
- Exports results to a structured JSON file

---

## Project Structure

```
geo_name_cleaner/
├── run_cleaner.py              # Main script
├── get_country_typos.py        # Helper to generate typo dictionary
├── country_typo_data.json      # Predefined alternate/typo mappings (optional)
├── corrected_countries.json    # Output file
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

##  Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/geo_name_cleaner.git
cd geo_name_cleaner
```

### 2. Install dependencies

Make sure you have Python 3.6+, then run:

```bash
pip install -r requirements.txt
```

### 3. Configure GeoNames

Open `run_cleaner.py` and replace the placeholder `USERNAME` with your actual [GeoNames.org](https://www.geonames.org/login) username.

```python
GEONAMES_USERNAME = "mahsazabetian"
```

### 4. Run the script

```bash
python run_cleaner.py
```

---

##  Example Input and Output

Input countries:

```python
TEST_INPUTS = [
    "Untied States",
    "UK",
    "Russsia",
    "Venzuela",
    "South Corea"
]
```

Output (`corrected_countries.json`):

```json
[
  { "original": "Untied States", "corrected": "United States" },
  { "original": "UK", "corrected": "United Kingdom" },
  { "original": "Russsia", "corrected": "Russian Federation" },
  { "original": "Venzuela", "corrected": "Venezuela" },
  { "original": "South Corea", "corrected": "South Korea" }
]
```

---

##  How It Works

1. Downloads the official list of countries from the GeoNames API.
2. Checks if each input country matches an alternate name or known typo.
3. If no match is found, applies fuzzy matching (RapidFuzz).
4. Returns the closest official country name, or `"Not Found"` if unmatched.
5. Outputs results in a JSON format.

---

## `requirements.txt`

Make sure this file includes:

```text
requests
rapidfuzz
```

Install with:

```bash
pip install -r requirements.txt
```

---

##  Example Code Snippet

### `run_cleaner.py` 

```python
from get_country_typos import get_country_typos
from rapidfuzz import process
import requests, json

GEONAMES_USERNAME = "your_username_here"

def get_country_list():
    url = f"http://api.geonames.org/countryInfoJSON?username={GEONAMES_USERNAME}"
    response = requests.get(url)
    return [c['countryName'] for c in response.json()['geonames']]

def correct_country_name(name, countries, typo_dict):
    if name in typo_dict:
        return typo_dict[name]
    match, score, _ = process.extractOne(name, countries)
    return match if score > 80 else "Not Found"

def main():
    inputs = ["Untied States", "UK", "Russsia"]
    typo_dict = get_country_typos()
    countries = get_country_list()

    results = []
    for name in inputs:
        corrected = correct_country_name(name, countries, typo_dict)
        results.append({"original": name, "corrected": corrected})
        print(f"{name} -> {corrected}")

    with open("corrected_countries.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
```

---

## Future Improvements

- Expand typo support to cities, provinces, or regions
- Add unit tests for fuzzy match scoring
- Develop a simple web-based interface
- Store correction logs and confidence scores

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

##  Author

Mahsa Zabetian 
Feel free to contact me or fork this project for your own geographic data-cleaning tasks!
