from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import ast

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://samimagine.github.io/munich"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        raw_state = option["state"]

        if raw_state.startswith("[") and raw_state.endswith("]"):  
            try:
                parsed_state = ast.literal_eval(raw_state)
                state_cleaned = parsed_state[0] if isinstance(parsed_state, list) else parsed_state
            except (SyntaxError, ValueError):
                state_cleaned = raw_state
        else:
            state_cleaned = raw_state

        option["state"] = state_cleaned

        areas = option["areas"]

        if request.state == "bundesweit":
            state_match = "bundesweit" in state_cleaned
        else:
            state_match = request.state == state_cleaned or "bundesweit" in state_cleaned

        company_size_match = request.company_size == option["company_size"]
        areas_match = any(area in areas for area in request.areas)
        grant_match = request.grant <= option["grant_volume"]
        revenue_match = request.revenue <= option["revenue_max"]

        debug_message = {
            "funding_option": option["funding option"],
            "state_match": state_match,
            "company_size_match": company_size_match,
            "areas_match": areas_match,
            "grant_match": grant_match,
            "revenue_match": revenue_match
        }
        debug_info.append(debug_message)

        if all([state_match, company_size_match, areas_match, grant_match, revenue_match]):
            matching_options.append(option)

    sorted_options = sorted(
        matching_options,
        key=lambda x: (-x["benefit_cost_score"], -x["approval_rate"], x["time_required"]),
    )

    if not sorted_options:
        raise HTTPException(status_code=404, detail="No matching funding options found.")

    return sorted_options