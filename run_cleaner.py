# -*- coding: utf-8 -*-

import json
from geo_name_cleaner.corrector import fetch_country_names, correct_country_name

USERNAME = "mahsazabetian"
VALID_COUNTRIES = fetch_country_names(USERNAME)

TEST_INPUTS = ['Untied States', 'UK', 'Russsia', 'Venzuela', 'South Corea']

results = []
for name in TEST_INPUTS:
    corrected = correct_country_name(name, VALID_COUNTRIES)
    print(f"{name} → {corrected}")
    results.append({"original": name, "corrected": corrected})

with open("corrected_countries.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

