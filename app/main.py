from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import origins, details
from models.user_model import User
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


# demo route
@app.get("/demo")
def read_demo() -> list[User]:
    users = [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@doe.com"
        },
        {
            "id": 2,
            "name": "Jane Doe",
            "email": "jane@doe.com"
        },
    ]

    return users



# def main():
#     print("Hello World!")

# if __name__ == "__main__":
#     main()
