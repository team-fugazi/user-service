from fastapi import APIRouter, status, HTTPException
from datetime import datetime
from bson import ObjectId

# Helpers
from ...helpers.meta_generator import generate_meta


# Models
from ...models.user import User
from ...models.moderation import Moderation

# Database connection
from ...database.mongodb import database as db

router = APIRouter(prefix="/actions", tags=["actions"])


@router.post("/{profile_id}", tags=["Moderation"])
def add_user_moderation(profile_id: str, moderation: Moderation):
    # Convert partial response body to dict
    mod_dict = moderation.model_dump()

    # Add metadata
    mod_dict["id"] = None
    mod_dict["created_at"] = datetime.now()
    mod_dict["updated_at"] = None
    mod_dict["deleted_at"] = None

    # Validate and create a Moderation instance
    mod_full = Moderation(**mod_dict)

    # Insert moderation into the database
    result_mod = db.moderations.insert_one(
        mod_full.model_dump(by_alias=True, exclude=["id"])
    )

    # Check if moderation was created
    if not result_mod.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Moderation could not be created",
        )

    # Add moderation to user profile
    result_mod = db.profiles.update_one(
        {"_id": ObjectId(profile_id)},
        {"$push": {"bans": result_mod.inserted_id}},
    )

    return {
        "status": status.HTTP_201_CREATED,
        "meta": generate_meta(),
        "message": "Comment created successfully",
        "updated": f"profile with id {profile_id}",
    }


@router.delete("/{profile_id}/{moderation_id}", tags=["Moderation"])
def remove_user_moderation(profile_id: str, moderation_id: str):
    # Remove comment reference from the report document
    result = db.profiles.update_one(
        {"_id": ObjectId(profile_id)},
        {"$pull": {"bans": ObjectId(moderation_id)}},
    )

    # Check if the comment reference was found and removed
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moderation not found in the user profile",
        )

    # Delete the comment itself
    mod_result = db.moderations.delete_one({"_id": ObjectId(moderation_id)})

    # Check if the comment was deleted
    if mod_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moderation not found in the database",
        )

    return {
        "status": status.HTTP_202_ACCEPTED,
        "meta": generate_meta(),
        "message": "Moderation deleted successfully",
        "deleted_count": mod_result.deleted_count,
    }
