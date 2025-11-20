import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# Database helpers (provided in environment)
from database import create_document, get_documents

app = FastAPI(title="Vivo Pizza Event Service API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models (API layer)
class InquiryModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(..., min_length=5, max_length=40)
    event_date: str
    guests: int = Field(..., ge=1, le=1000)
    location: str = Field(..., min_length=2, max_length=200)
    event_type: str = Field(..., min_length=2, max_length=100)
    message: Optional[str] = Field(None, max_length=2000)

class InquiryResponse(BaseModel):
    id: str
    status: str

REGIONS: List[str] = [
    "Bregenz", "Dornbirn", "Feldkirch", "Bludenz", "Montafon", "Bregenzerwald"
]

@app.get("/")
def root():
    return {"status": "ok", "service": "Vivo Pizza Event Service API", "regions": REGIONS}

@app.get("/regions", response_model=List[str])
def get_regions():
    return REGIONS

@app.post("/inquiry", response_model=InquiryResponse)
async def create_inquiry(payload: InquiryModel):
    try:
        doc = payload.model_dump()
        doc["status"] = "new"
        doc["created_at"] = datetime.utcnow().isoformat()
        created = await create_document("inquiry", doc)
        # create_document returns inserted document with _id or id
        inserted_id = str(created.get("_id") or created.get("id") or "")
        if not inserted_id:
            raise ValueError("No ID returned from database")
        return {"id": inserted_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store inquiry: {str(e)[:200]}")

# Optional diagnostic
@app.get("/test")
def test():
    return {"backend": "running", "regions": REGIONS}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
