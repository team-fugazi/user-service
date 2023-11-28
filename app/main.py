from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
# Config and Routes
from .core.config import origins, details
from .helpers.utils import VerifyToken
# Routes
from .routers.v1.users import router as user_v1
from .routers.v1.actions import router as action_v1


app = FastAPI(
    title=details["title"],
    description=details["description"],
    version=details["version"],
    contact=details["contact"],
)


auth = VerifyToken()


# Add CORS to app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(user_v1, prefix="/v1", dependencies=[Security(auth.verify)])
app.include_router(action_v1, prefix="/v1")


# Root route
@app.get("/")
def read_root():
    return {"ping": "pong"}
