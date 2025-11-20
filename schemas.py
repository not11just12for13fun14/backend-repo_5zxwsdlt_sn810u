"""
Database Schemas

Define MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Class name lowercased = collection name

Example: class User -> collection "user"
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Inquiry(BaseModel):
    """
    Collection: "inquiry"
    Stores booking inquiries for the Vivo Pizza Event Service.
    """
    name: str = Field(..., min_length=2, max_length=120, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., min_length=5, max_length=40, description="Phone number")
    event_date: str = Field(..., description="Event date (ISO or human-readable)")
    guests: int = Field(..., ge=1, le=1000, description="Estimated number of guests")
    location: str = Field(..., min_length=2, max_length=200, description="Event location / city")
    event_type: str = Field(..., min_length=2, max_length=100, description="Event type (wedding, corporate, birthday, private)")
    message: Optional[str] = Field(None, max_length=2000, description="Additional details")

# You can add more collections as needed, e.g. Review, Region, etc.
