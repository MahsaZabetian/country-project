# country-project
 Country Name Standardizer

This project provides a simple Python tool to **automatically correct typos and standardize country names**, using official data from the [GeoNames API](https://www.geonames.org/). It supports:
- Typo correction using fuzzy string matching
- Mapping of alternate names (e.g. "UK", "USA", "Russia") to their standardized forms
- Output to a clean, corrected JSON format

---

## Problem Statement

In many datasets—especially global biodiversity and geospatial data—country names may contain:
- Typos (e.g. `"Untied States"`)
- Informal abbreviations (e.g. `"UK"`, `"South Korea"`)
- Historical or non-standard variants (e.g. `"Russia"` instead of `"Russian Federation"`)

This tool automates the correction and standardization of such country names using:
- A dynamic list of valid countries from the **GeoNames API**
- Predefined aliases for common name variants
- Fuzzy string matching via **RapidFuzz**

---

## Installation

You need Python 3.7+ installed.

1. **Clone this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or manually:
   ```bash
   pip install rapidfuzz requests
   ```

---

## How to Use

1. Register for a free GeoNames account:  
   https://www.geonames.org/login

2. Update the `username` variable in the script with your GeoNames username.

3. Run the script:
   ```bash
   python country_standardizer.py
   ```

4. Results are printed and also saved to `corrected_countries.json`.

---

## How It Works

This tool combines three key strategies:

1. **Dynamic list of valid names**:  
   Using the GeoNames API, it fetches the latest list of official country names.

2. **Alternate name mapping**:  
   A dictionary (`ALTERNATE_NAMES`) maps informal or common variants (like `"UK"`, `"USA"`) to their official equivalents.

3. **Fuzzy matching with RapidFuzz**:  
   If the name isn’t a direct match or in the alias list, we use [`rapidfuzz.process.extractOne`](https://maxbachmann.github.io/RapidFuzz/Usage/fuzz.html#rapidfuzz.process.extractOne) to find the closest match above a confidence threshold (default: 85%).

---

## How the Functions Work Together

### `fetch_country_names(username)`
- Pulls a dynamic list of official country names from GeoNames.
- Keeps the solution up-to-date and globally consistent.

### `correct_typo(name, valid_names, threshold)`
- First checks if the input name is a known alternate (like `"UK"`).
- If not, applies fuzzy string matching using RapidFuzz to find the closest match.
- Returns the corrected country name or `"Not Found"`.

The script then loops through test names, applies the correction logic, and stores results in a JSON file.

---

## Generalization to Other BCDM Fields

This tool is designed for **controlled vocabulary correction**, which is a core principle in the [BCDM (Biodiversity Contextual Data Model)](https://github.com/BOLDSystems/bcdm) project. Here's how you can generalize it:

- Replace the list of country names with any other controlled vocabulary (e.g. **sampling protocols**, **tissue types**, **collection methods**, etc.)
- Expand the `ALTERNATE_NAMES` dictionary for common informal variants
- Reuse the `correct_typo()` function for fuzzy correction

This modular structure allows you to:
- Easily standardize other fields defined in the [BCDM GitHub repo](https://github.com/BOLDSystems/bcdm/tree/main/controlled_vocabularies)
- Clean and validate user-entered data in scientific datasets

---

## Output Example

```json
[
    {
        "original": "Untied States",
        "corrected": "United States"
    },
    {
        "original": "UK",
        "corrected": "United Kingdom"
    },
    {
        "original": "Russsia",
        "corrected": "Russian Federation"
    },
    {
        "original": "Venzuela",
        "corrected": "Venezuela"
    },
    {
        "original": "South Corea",
        "corrected": "South Korea"
    }
]
```

---

## his tool can be expanded to correct any BOLD field with a controlled vocabulary, such as:

continent

habitat

collection_method

tissue_type

The BOLD Controlled Data Model (BCDM) defines all standard fields and valid values. You can follow the same structure: fetch controlled terms → apply fuzzy matching → correct values.

---

## License

MIT License
