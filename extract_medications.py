import json
from pathlib import Path

import spacy

# Create a blank English NLP pipeline
nlp = spacy.blank("en")

# Add a rule-based entity recogniser
ruler = nlp.add_pipe("entity_ruler")

# Define our medication vocabulary
medications = {
    "Stelara": "ustekinumab",
    "Humira": "adalimumab",
    "Entyvio": "vedolizumab",
    "Remicade": "infliximab",
    "Cosentyx": "secukinumab",
}

# Add patterns for both brand and generic names
patterns = []

for brand, generic in medications.items():
    patterns.append({
        "label": "MEDICATION",
        "pattern": [{"LOWER": brand.lower()}],
        "id": generic,
    })
    patterns.append({
        "label": "MEDICATION",
        "pattern": [{"LOWER": generic.lower()}],
        "id": generic,
    })

ruler.add_patterns(patterns)

# Load the synthetic prescriptions
with open("data/prescriptions.json") as f:
    prescriptions = json.load(f)

# Extract medication entities
enriched = []

for prescription in prescriptions:
    doc = nlp(prescription["prescription_text"])

    extracted = [
        {
            "text": ent.text,
            "ingredient": ent.ent_id_,
        }
        for ent in doc.ents
        if ent.label_ == "MEDICATION"
    ]

    enriched.append({
        "prescription_id": prescription["prescription_id"],
        "prescription_text": prescription["prescription_text"],
        "medications": extracted,
    })

# Save the enriched data
Path("data").mkdir(exist_ok=True)

with open("data/enriched_prescriptions.json", "w") as f:
    json.dump(enriched, f, indent=2)

print(f"Processed {len(enriched)} prescriptions.")
print("Example:")
print(json.dumps(enriched[0], indent=2))