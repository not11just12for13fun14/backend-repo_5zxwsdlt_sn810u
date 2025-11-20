from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Vivo Pizza Event Service API", version="1.0.0")

# CORS for frontend usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Inquiry(BaseModel):
    name: str = Field(..., min_length=2)
    email: str
    phone: str
    event_date: str
    guests: int
    location: str
    event_type: str
    message: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Vivo Pizza Event Service API is running"}


@app.post("/inquiry")
async def create_inquiry(inquiry: Inquiry):
    # In a real app we would store to DB. For now just echo back success.
    return {"status": "ok", "received": inquiry.model_dump()}


@app.get("/regions")
async def get_regions() -> List[str]:
    return [
        "Vorarlberg",
        "Bregenz",
        "Dornbirn",
        "Feldkirch",
        "Bludenz",
        "Montafon",
        "Bregenzerwald",
    ]
