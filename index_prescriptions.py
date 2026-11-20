import json
import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

# 1. Connect to Elasticsearch
load_dotenv()

es = Elasticsearch(
    os.environ["ELASTICSEARCH_URL"],
    api_key=os.environ["ELASTICSEARCH_API_KEY"],
)

print("Connected:", es.ping())

# 2. Load the enriched prescriptions
with open("data/enriched_prescriptions.json") as f:
    prescriptions = json.load(f)

# 3. Create the index with explicit field mappings
index_name = "rxsearch_prescriptions"

if not es.indices.exists(index=index_name):
    es.indices.create(
        index=index_name,
        mappings={
            "properties": {
                "prescription_id": {"type": "keyword"},
                "prescription_text": {"type": "text"},
                "medications": {
                    "type": "nested",
                    "properties": {
                        "text": {"type": "keyword"},
                        "ingredient": {"type": "keyword"},
                    },
                },
            }
        },
    )

# 4. Prepare documents for Elasticsearch
actions = [
    {
        "_index": index_name,
        "_id": prescription["prescription_id"],
        "_source": prescription,
    }
    for prescription in prescriptions
]

# 5. Upload all 1,000 documents
success, errors = helpers.bulk(
    es,
    actions,
    refresh="wait_for",
    raise_on_error=False,
)

print(f"Indexed {success} prescriptions.")
print(f"Errors: {len(errors)}")