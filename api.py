from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from search import (
    es,
    INDEX,
    normalise_medication,
    search_raw_text,
)

# Create the FastAPI application ONCE
app = FastAPI(title="RxSearch API")

# Allow React to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://rxsearch.netlify.app",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to RxSearch",
        "status": "running",
    }


@app.get("/search")
def search(medication: str = Query(min_length=1)):
    ingredient = normalise_medication(medication)

    try:
        # Search using the normalised ingredient
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
                    },
                }
            },
        )

        enriched_total = response["hits"]["total"]["value"]

        # Compare against ordinary text search
        raw_total = search_raw_text(medication)

        prescriptions = [
            hit["_source"]
            for hit in response["hits"]["hits"]
        ]

        return {
            "query": medication,
            "normalised_ingredient": ingredient,
            "raw_matches": raw_total,
            "enriched_matches": enriched_total,
            "prescriptions": prescriptions,
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Elasticsearch search is currently unavailable.",
        )