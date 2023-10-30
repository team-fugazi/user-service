from pydantic import BaseModel, Field
from datetime import datetime


class Verification(BaseModel):
    verification_id: str = Field(..., description="Unique verification identifier")
    user_id: str = Field(..., description="User's ID for whom the verification is")
    verification_code: str = Field(..., description="Verification code or token")
    expiration_date: datetime = Field(..., description="Expiration date of the verification code")
    is_verified: bool = Field(False, description="Flag indicating whether the user is verified")

    class Config:
        schema_extra = {
            "example": {
                "verification_id": "unique_verification_id",
                "user_id": "google-oauth2|115381085628553582032",
                "verification_code": "random_verification_token",
                "expiration_date": "2023-10-30T23:59:59",
                "is_verified": False
            }
        }