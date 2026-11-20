import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

es = Elasticsearch(
    os.environ["ELASTICSEARCH_URL"],
    api_key=os.environ["ELASTICSEARCH_API_KEY"],
)

INDEX = "rxsearch_prescriptions"

# Same medication dictionary used by spaCy
MEDICATIONS = {
    "stelara": "ustekinumab",
    "humira": "adalimumab",
    "entyvio": "vedolizumab",
    "remicade": "infliximab",
    "cosentyx": "secukinumab",
}

def normalise_medication(name):
    """Convert a brand or generic name to its ingredient."""
    name = name.strip().lower()
    return MEDICATIONS.get(name, name)


def search_prescriptions(name):
    ingredient = normalise_medication(name)

    response = es.search(
        index=INDEX,
        size=10,
        track_total_hits=True,
        query={
            "nested": {
                "path": "medications",
                "query": {
                    "term": {
                        "medications.ingredient": ingredient
                    }
                }
            }
        },
    )

    total = response["hits"]["total"]["value"]

    # NEW: Compare raw text search with enriched search
    raw_total = search_raw_text(name)

    print(f"\nRaw text matches: {raw_total}")
    print(f"Enriched matches: {total}\n")

    # Display the matching prescriptions
    for hit in response["hits"]["hits"]:
        prescription = hit["_source"]

        print(f"ID: {prescription['prescription_id']}")
        print(f"Text: {prescription['prescription_text']}")
        print(f"Extracted: {prescription['medications']}")
        print("-" * 50)

def search_raw_text(name):
    response = es.search(
        index=INDEX,
        size=0,
        track_total_hits=True,
        query={
            "match": {
                "prescription_text": name
            }
        }
    )

    return response["hits"]["total"]["value"]


if __name__ == "__main__":
    print("RxSearch — Medication Search")
    print("Type 'quit' to exit.\n")

    while True:
        name = input("Search medication: ").strip()

        if name.lower() == "quit":
            break

        if not name:
            continue

        search_prescriptions(name)