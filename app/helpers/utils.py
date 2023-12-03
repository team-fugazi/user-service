from typing import Any, Dict, Optional
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer , OAuth2AuthorizationCodeBearer# 👈 new imports
from ..core.auth_config import get_settings
import jwt

class UnauthorizedException(HTTPException):
    def __init__(self,  detail: str, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication")



class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self):
        self.config = get_settings()


        jwks_url = f'https://{self.config.auth0_domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(self, request: Request, security_scopes: SecurityScopes, token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())):
        if token is None:
            raise UnauthenticatedException
        try: 
            signing_key = self.jwks_client.get_signing_key_from_jwt(token.credentials).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))
        
        try:
            payload = jwt.decode(token.credentials, 
                                 signing_key, 
                                 algorithms=self.config.auth0_algorithms, 
                                 audience=self.config.auth0_api_audience, 
                                 issuer=self.config.auth0_issuer, 
                                 options={"verify_iat":False})
            
        except Exception as error:
            raise UnauthorizedException(str(error))
        request.token_payload = payload
        return payload