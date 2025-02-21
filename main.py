from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://samimagine.github.io/munich"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load JSON Data
with open("data_funded.json", "r", encoding="utf-8") as f:
    FUNDING_DATA = json.load(f)

class FundingRequest(BaseModel):
    state: str
    company_size: str
    areas: List[str]
    grant: int
    revenue: int

@app.post("/find-best-funding")
def find_best_funding(request: FundingRequest):
    print("🔍 Received request:", request.dict())
    matching_options = []
    debug_info = []

    for option in FUNDING_DATA:
        states = option["state"]  # Already a list
        areas = option["areas"]  # Already a list

        # ✅ Handle State Selection Logic
        if request.state == "bundesweit":
            state_match = True  # Ignore state, include all states
        else:
            state_match = request.state in states  # Exact match for state

        # ✅ Other filters (company size, areas, grant, revenue)
        company_size_match = request.company_size == option["company_size"]
        areas_match = any(area in areas for area in request.areas)
        grant_match = request.grant <= option["grant_volume"]
        revenue_match = request.revenue <= option["revenue_max"]

        # ✅ Debugging info
        debug_message = {
            "funding_option": option["funding option"],
            "state_match": state_match,
            "company_size_match": company_size_match,
            "areas_match": areas_match,
            "grant_match": grant_match,
            "revenue_match": revenue_match
        }
        debug_info.append(debug_message)

        # ✅ Add matching options
        if all([state_match, company_size_match, areas_match, grant_match, revenue_match]):
            matching_options.append(option)

    # ✅ Now add bundesweit grants for specific states
    if request.state != "bundesweit":
        for option in FUNDING_DATA:
            if "bundesweit" in option["state"]:  # Only bundesweit grants
                company_size_match = request.company_size == option["company_size"]
                areas_match = any(area in areas for area in request.areas)
                grant_match = request.grant <= option["grant_volume"]
                revenue_match = request.revenue <= option["revenue_max"]

                # ✅ Add bundesweit grants that match all other criteria
                if all([company_size_match, areas_match, grant_match, revenue_match]):
                    matching_options.append(option)

    # ✅ Sort by best scoring options
    sorted_options = sorted(
        matching_options,
        key=lambda x: (-x["benefit_cost_score"], -x["approval_rate"], x["time_required"]),
    )

    # ✅ Handle No Results Case
    if not sorted_options:
        raise HTTPException(status_code=404, detail="No matching funding options found.")

    return sorted_options