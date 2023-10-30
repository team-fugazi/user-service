from typing import List
from fastapi import HTTPException, status

# Models
from ..models.user import User

class UserListRoutes:
    def __init__(self, db):
        self.db = db

    # Returns a list of all Users in registry as JSON
    def get_users(self) -> List[User]:
        users = self.db.find()
        return [User(**user) for user in users]

    # Post Method adding a new user to registry
    def create_user(self, user: User) -> dict:
        user_dict = user.dict()
        result = self.db.insert_one(user_dict)
        return {"status": status.HTTP_201_CREATED, "id": str(result.inserted_id)}

    # Do not allow to UPDATE entire user registry
    def update_user(self) -> HTTPException:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Do not allow to DELETE entire user registry
    def delete_user(self) -> HTTPException:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
