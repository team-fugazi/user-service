from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class Ban(BaseModel):
    ban_id: str = Field(..., description="Reference to a ban document")
    start_date: datetime = Field(..., description="Start date of the ban")
    end_date: datetime = Field(..., description="End date of the ban")

class User(BaseModel):
    auth0_user_id: str = Field(..., description="Auth0 user_id")
    username: str
    email: str
    first_name: str
    last_name: str
    profile_picture: str
    created_at: datetime = Field(..., description="Timestamp of user registration")
    updated_at: datetime = Field(..., description="Timestamp of the last update")
    verification_id: str = Field(..., description="Reference to a verification document")
    bans: List[Ban] = Field([], description="List of user bans")
