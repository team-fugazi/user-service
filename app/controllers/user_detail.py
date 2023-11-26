from fastapi import HTTPException, status
from bson import ObjectId

# models
from ..models.user import User


class UserDetailRoutes:
    def __init__(self, db):
        self.db = db

    # Queries a single user in registry by ID
    def get_user(self, id: str) -> User:
        user = self.db.find_one(ObjectId(id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error: No document found with id: {id}",
            )

        return User(**user)

    # Queries and updates a single user in registry by ID
    def update_user(self, id: str, user: User) -> dict:
        if not self.db.find_one(ObjectId(id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        filtered_doc = {"_id": ObjectId(id)}
        user_dict = {"$set": user.dict()}
        result = self.db.update_one(filtered_doc, user_dict)

        return {
            "status": status.HTTP_200_OK,
            "Document Modified": id,
            "Documents Modified": str(result.modified_count),
        }

    # Queries and removes a single user in registry by ID
    def delete_user(self, id: str) -> dict:
        if not self.db.find_one(ObjectId(id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        result = self.db.delete_one({"_id": ObjectId(id)})

        return {
            "status": status.HTTP_200_OK,
            "Document Modified": id,
            "Documents Modified": str(result.deleted_count),
        }
