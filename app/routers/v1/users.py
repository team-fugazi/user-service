from fastapi import APIRouter, Header, Request

# Models & Config
from ...models.user import User

# Controllers
from ...controllers.user_list import UserListRoutes
from ...controllers.user_detail import UserDetailRoutes

# Database connection
from ...database.mongodb import database

router = APIRouter(prefix="/users", tags=["users"])

# Controllers
list_routes = UserListRoutes(database.profiles)
detail_routes = UserDetailRoutes(database.profiles)

# Controllers added to Routes
@router.get("/", tags=["List"])
def get_user_list():
    return list_routes.get_users()


@router.post("/", tags=["List"])
def post_user_list(user: User):
    return list_routes.create_user(user)


@router.put("/", tags=["List"])
def put_user_list():
    return list_routes.update_user()


@router.delete("/", tags=["List"])
def delete_user_list():
    return list_routes.delete_user()


@router.post("/{id}", tags=["Detail"])
def post_user_detail():
    return detail_routes.create_user()


# @router.get("/{id:PyObjectId}", tags=["Detail"]) #Conflicts with
# def get_user_detail(id: str):
#     return detail_routes.get_user(id)


@router.put("/{id}", tags=["Detail"])
def put_user_detail(id: str, user: User):
    return detail_routes.update_user(id, user)


@router.delete("/{id}", tags=["Detail"])
def delete_user_detail(id: str):
    return detail_routes.delete_user(id)

@router.get("/me", tags=["Detail"])
def get_user_with_token(request: Request):
    payload = request.token_payload
    return detail_routes.get_user_by_auth0(payload["sub"])
