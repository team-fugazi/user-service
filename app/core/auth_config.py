from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field
class Settings(BaseSettings):
    auth0_domain: str = Field(validation_alias='AUTH0_DOMAIN')
    auth0_api_audience: str = Field(validation_alias='AUTH0_API_AUDIENCE')
    auth0_issuer: str = Field(validation_alias='AUTH0_ISSUER')
    auth0_algorithms: str = Field(validation_alias='AUTH0_ALGORITHMS')

    class Config:
        env_file = ".env"
        extra = "allow"
        

@lru_cache()
def get_settings():
    return Settings()