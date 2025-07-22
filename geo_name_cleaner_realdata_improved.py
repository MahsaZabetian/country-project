import os
import json
import logging
import pandas as pd
import requests
from tqdm import tqdm
from rapidfuzz import process
import country_converter as coco

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


# --- Utility Functions ---

def build_alternate_country_map():
    """Automatically build a full map of alternate country names 
    to standard ones using country_converter."""
    cc = coco.CountryConverter()
    df = cc.data
    alt_map = {}

    for _, row in df.iterrows():
        canonical = row["name_short"]
        for val in row:
            if isinstance(val, str) and val.strip():
                alt_map[val.strip()] = canonical

    # Add a few very common abbreviations and edge cases
    alt_map.update({
        "U.S.": "United States",
        "U.S.A.": "United States",
        "UAE": "United Arab Emirates",
        "DRC": "Congo, the Democratic Republic of the"
    })

    return alt_map


def fetch_provinces_from_geonames(username, cache_file="province_cache.json"):
    """Fetch province names from GeoNames API, with local caching."""
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            logging.info("✅ Loaded provinces from cache.")
            return json.load(f)

    logging.info("🌐 Fetching provinces from GeoNames...")
    province_names = set()
    try:
        country_url = f"http://api.geonames.org/countryInfoJSON?username={username}"
        response = requests.get(country_url)
        response.raise_for_status()
        countries = response.json().get("geonames", [])
        for country in countries:
            geoname_id = country.get("geonameId")
            child_url = f"http://api.geonames.org/childrenJSON?geonameId={geoname_id}&username={username}"
            child_resp = requests.get(child_url)
            child_resp.raise_for_status()
            children = child_resp.json().get("geonames", [])
            for child in children:
                name = child.get("name")
                if name:
                    province_names.add(name.strip())
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(sorted(list(province_names)), f, indent=2)
        logging.info("✅ Provinces cached locally.")
    except Exception as e:
        logging.error(f"Error fetching provinces from GeoNames: {e}")
    return list(province_names)


def load_reference_list(filepath):
    """Load reference lists (countries or provinces) from a TSV file."""
    with open(filepath, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def classify_and_correct(name, country_list, province_list, alternate_country_map=None, threshold=85):
    """Unified classifier and typo corrector for mixed data."""
    if not isinstance(name, str) or name.strip().lower() in ["", "nan"]:
        return "Not Found"

    name = name.strip()

    # Check alternate map for countries first
    if alternate_country_map and name in alternate_country_map:
        return alternate_country_map[name] + " (country)"

    # Fuzzy match country
    best_country = process.extractOne(name, country_list)
    if best_country and best_country[1] >= threshold:
        return best_country[0] + " (country)"

    # Fuzzy match province
    best_province = process.extractOne(name, province_list)
    if best_province and best_province[1] >= threshold:
        return best_province[0] + " (province)"

    return "Not Found"


def clean_one_file(filepath, output_folder, country_list, province_list, alternate_country_map):
    """Clean a single file by applying classification and correction."""
    df = pd.read_csv(filepath, sep="\t", dtype=str)

    if "verbatim_value" not in df.columns:
        logging.warning(f"⚠ Skipped file (missing 'verbatim_value'): {filepath}")
        return

    df["standardized_value"] = df["verbatim_value"].apply(
        lambda x: classify_and_correct(x, country_list, province_list, alternate_country_map)
    )

    filename = os.path.basename(filepath)
    output_path = os.path.join(output_folder, filename)
    df.to_csv(output_path, sep="\t", index=False)
    logging.info(f"✔ Cleaned: {filename}")


def clean_all_files(input_folder, output_folder, country_ref_file, username, alternate_country_map):
    """Run batch cleaning on all TSV files in the input folder."""
    country_list = load_reference_list(country_ref_file)
    province_list = fetch_provinces_from_geonames(username)

    os.makedirs(output_folder, exist_ok=True)
    files = [f for f in os.listdir(input_folder) if f.endswith(".tsv")]

    for file in tqdm(files, desc="🧹 Cleaning files"):
        full_path = os.path.join(input_folder, file)
        clean_one_file(full_path, output_folder, country_list, province_list, alternate_country_map)


# --- Main Execution ---

if __name__ == "__main__":
    alternate_country_map = build_alternate_country_map()

    clean_all_files(
        input_folder="./data/raw",
        output_folder="./data/cleaned",
        country_ref_file="./data/BOLD_Geonames_mapping.tsv",
        username="mahsazabetian",
        alternate_country_map=alternate_country_map,
    )
