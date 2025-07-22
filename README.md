
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

## How It Works

This tool combines three key strategies:

1. fetch_provinces_from_geonames(username)
Fetches first-order administrative divisions (provinces) from GeoNames and caches them locally.

2. build_alternate_country_map()
Builds a dictionary of alternate country names using country_converter, extended with common abbreviations (e.g., "UAE", "DRC").

3. load_reference_list(filepath)
Loads standardized country names from a local .tsv file (from BOLD).

4. classify_and_correct(...)
Classifies user-entered names by:

First checking the alternate name map

Then using rapidfuzz to find a fuzzy match in both country and province lists

5. clean_all_files(...)
Runs the full cleaning pipeline on all .tsv files in the input folder and saves them to the output folder with a standardized_value column.

## Function Overview

** build_alternate_country_map()
  . Builds a map of alternate or informal country names to standardized ones. 
  . Uses country_converter + custom logic.

** load_reference_list(filepath)
. Loads official country names from a BOLD .tsv file.

** fetch_provinces_from_geonames(username)
. Fetches provinces via GeoNames and caches the result.

** classify_and_correct(...)
. Core classifier: returns "Canada (country)", "Ontario (province)", or "Not Found".

** clean_all_files(...)
. Batch processes all raw .tsv files and saves the corrected versions.



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

4)Apply to any BCDM field to prepare datasets for BOLD, GBIF, etc.

. This makes the tool a flexible framework for data standardization in biodiversity informatics.


## License

MIT License
