from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import origins, details
from models.user import User
from database.mongodb import client
from routers.router_v1 import router as user_v1


app = FastAPI(
    title=details["title"],
    description=details["description"],
    version=details["version"],
    contact=details["contact"],
)

# Add CORS to app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root route
@app.get("/")
def read_root():
    return {"ping": "pong"}

# random dict




# @app.post("/v1/auth/createuser")
# def read_demo(user:User):

#     print(user)


app.include_router(user_v1, prefix="/v1")

