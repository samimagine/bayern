import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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

@app.get("/")
def home():
    return {"message": "Welcome to the Funding Options API"}

@app.get("/funding-options")
def get_funding_options():
    """Returns all funding options from the JSON file."""
    return FUNDING_DATA

@app.get("/funding-options/{funding_option}")
def get_funding_option(funding_option: str):
    """Returns a specific funding option by name."""
    for option in FUNDING_DATA:
        if option["funding_option"].lower() == funding_option.lower():
            return option
    return {"error": "Funding option not found"}

@app.get("/funding-options/state/{state_name}")
def get_funding_by_state(state_name: str):
    """Returns funding options available in a specific state."""
    result = [option for option in FUNDING_DATA if state_name in option["state"]]
    return result if result else {"error": "No funding options found for this state"}

@app.get("/funding-options/company-size/{company_size}")
def get_funding_by_company_size(company_size: str):
    """Returns funding options for a specific company size."""
    result = [option for option in FUNDING_DATA if option["company_size"].lower() == company_size.lower()]
    return result if result else {"error": "No funding options found for this company size"}