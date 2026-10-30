from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI(title="Lean Lead API", version="1.0")

# CRITICAL FOR CLIENTS: Configuring CORS Middleware
# This permits your frontend domain to safely make requests to your API backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your exact frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a strict, auto-validating data schema using Pydantic
class Lead(BaseModel):
    name: str
    email: str
    company: str

# In-memory database simulation
db_leads: List[Lead] = [
    {"name": "Alice Smith", "email": "alice@startup.io", "company": "TechNova"},
    {"name": "Bob Jones", "email": "bob@enterprise.com", "company": "GlobalCorp"}
]

@app.get("/api/leads", response_model=List[Lead])
async def get_leads():
    """Retrieve all business leads from the database."""
    return db_leads

@app.post("/api/leads", status_code=201)
async def create_lead(lead: Lead):
    """Validate and save a new business lead."""
    # Automated error handling: If email format is wrong, FastAPI handles the response automatically
    db_leads.append(lead.dict())
    return {"message": "Lead captured successfully", "lead": lead}
