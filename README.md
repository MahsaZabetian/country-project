
# Country Name Standardizer

This project provides a simple Python tool to automatically correct typos and standardize **country** and **province** names using official data from the [GeoNames API](https://www.geonames.org/).

In addition to GeoNames, it also supports **custom standardization based on BOLD reference data**, stored locally in a `.tsv` file. This file contains the standardized country names used in the BOLD system.

## Problem Statement

In many datasets—especially global biodiversity and geospatial data—country and province names may contain:
- Typos (e.g. "Untied States")
- Informal abbreviations (e.g. "UK", "South Korea")
- Historical or non-standard variants (e.g. "Russia" instead of "Russian Federation")

This tool automates the correction and standardization of such country an d province names using:
- A dynamic list of valid countries from the **GeoNames API**
- The standardized country names used in the BOLD system
- Predefined aliases for common name variants
- Fuzzy string matching via **RapidFuzz**

---

country-project/
│
├── geo_name_cleaner.py # Main script (this file)
├── data/
│ ├── raw/ # Input .tsv files (must contain 'verbatim_value' column)
│ ├── cleaned/ # Output cleaned .tsv files (auto-created)
│ └── BOLD_Geonames_mapping.tsv # Reference file for standard country names
├── province_cache.json # Auto-generated cache of GeoNames provinces



## Installation

You need Python 3.7+ installed.

1. **Clone this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or manually:
  ```bash
  pip install pandas requests tqdm rapidfuzz country_converter
  ---

## How to Use

. Register for a free GeoNames account:
  https://www.geonames.org/login

. Update the username variable in the script with your GeoNames username.

Ensure your BOLD reference file is named and located at:
./data/BOLD_Geonames_mapping.tsv

Place your raw .tsv files (with a column named verbatim_value) inside:
./data/raw/

Run the script:

bash
Copy
Edit
python geo_name_cleaner_realdata_improved.py
Cleaned files will be saved to:
./data/cleaned/

## Usage

Place your raw .tsv files inside data/raw/

Each file should include a column called verbatim_value.

Ensure you have a file called BOLD_Geonames_mapping.tsv in data/

This contains your reference list of standardized country names (one per line).

Run the script:

bash
Copy
Edit
python geo_name_cleaner_realdata_improved.py
Cleaned files will be saved to data/cleaned/

A new column standardized_value will be added to each file.

## How It Works

build_alternate_country_map()
Builds a dictionary of alternate country names using the country_converter library and a few manual mappings (e.g., "U.S.A." → "United States").

fetch_provinces_from_geonames(username)
Fetches official province names using the GeoNames API and caches them in province_cache.json to avoid repeated API calls.

load_reference_list(filepath)
Reads a .tsv file (one name per line) and returns it as a Python list.

classify_and_correct(...)
Classifies each name in the input as either a country or province:

. Checks alternate names

. Uses fuzzy string matching to correct typos

. Returns a label like "Canada (country)" or "Ontario (province)"

clean_one_file(...)
Processes one file: reads verbatim_value, applies correction, and writes output with standardized_value.

clean_all_files(...)
Processes all .tsv files in the data/raw/ folder and writes results to data/cleaned/.

## Example Input/Output

Input (data/raw/sample.tsv):

verbatim_value
USA
British Colmbia
U.A.E
Ontari

## Output (data/cleaned/sample.tsv):

verbatim_value	standardized_value
USA	            United States (country)
British Colmbia	British Columbia (province)
U.A.E	United Arab Emirates (country)
Ontari	Ontario (province)


## Future Improvements

This project currently focuses on country and province name cleaning, but the design is modular and can be generalized to other controlled vocabulary fields in the BCDM model, such as:

.region or continent

. tissue_type

. collection_method

. institution_storing

. identification_method

## Generalization Strategy

1) Replace the .tsv reference file with the appropriate controlled vocabulary.

2) Expand the alternate name dictionary with known informal values.

3) Reuse classify_and_correct() for typo correction and matching.

4) Apply to any BCDM field to prepare datasets for BOLD, GBIF, etc.

. This makes the tool a flexible framework for data standardization in biodiversity informatics.


## License

MIT License
