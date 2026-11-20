import json
import random
from pathlib import Path

random.seed(42)

medications = [
    ("Stelara", "ustekinumab"),
    ("Humira", "adalimumab"),
    ("Entyvio", "vedolizumab"),
    ("Remicade", "infliximab"),
    ("Cosentyx", "secukinumab"),
]

templates = [
    "{name} prescribed for ongoing treatment.",
    "Patient commenced on {name}.",
    "Repeat prescription for {name}.",
    "Medication order: {name}.",
    "Continue treatment with {name}.",
]

prescriptions = []

for i in range(1, 1001):
    brand, generic = random.choice(medications)

    # Sometimes use brand, sometimes generic
    name = random.choice([brand, generic])

    text = random.choice(templates).format(name=name)

    prescriptions.append({
        "prescription_id": f"RX{i:04d}",
        "prescription_text": text,
        "expected_ingredient": generic,
        "expected_brand": brand,
    })

Path("data").mkdir(exist_ok=True)

with open("data/prescriptions.json", "w") as f:
    json.dump(prescriptions, f, indent=2)

print(f"Generated {len(prescriptions)} synthetic prescriptions.")