from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional
from typing_extensions import Annotated
from datetime import datetime

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


# fmt: off
class Moderation(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None, description="ID of the ban")
    reason: str = Field(..., description="Reason for the user moderation")
    created_at: datetime = Field(..., description="Date and time the moderation was created")
    updated_at: Optional[datetime] = Field(None, description="Date and time the modetation was last updated (optional)")
    expires_at: Optional[datetime] = Field(None, description="Date and time the modetation was deleted (optional)")
# fmt: on
