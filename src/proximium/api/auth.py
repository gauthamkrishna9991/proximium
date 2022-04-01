#!/usr/bin/env python3

# -- IMPORT: LIBRARIES

# - bcrypt
from urllib.request import Request
import bcrypt

# - FastAPI
from fastapi import APIRouter, HTTPException, Response
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

# - JWT
from jwcrypto import jwt

# -- IMPORT: SELF

# - Auth Model
from proximium.models.auth import AuthenticationRequest

# - User Schema
from proximium.schema.user import User as UserSchema

# - JWT Key Import
from proximium.jwt import key


# - Create Router
auth_router = APIRouter(prefix="/auth")


@auth_router.post("/")
def authenticate(response: Response, auth_req: AuthenticationRequest):
    # Get Users
    u: UserSchema | None = UserSchema.objects(
        UserSchema.username == auth_req.username
    ).first()
    if u is None:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with username '{auth_req.username}' not found."
        )
    # JWT Token
    token = jwt.JWT(header={"alg": "HS256"}, claims=auth_req.json())
    # Sign token with the key
    token.make_signed_token(key)
    # Encrypted JWT Token
    enc_token = jwt.JWT(
        header={"alg": "A256KW", "enc": "A256CBC-HS512"}, claims=token.serialize()
    )
    # Encrypt JWT Token
    enc_token.make_encrypted_token(key)
    # Set Authentication Cookie
    response.set_cookie(
        key="Authentication",
        value="Bearer enc_token.serialize()",
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return {
        "status": bcrypt.checkpw(
            bytes(auth_req.password, encoding="utf-8"), u.password_hash
        )
    }


class JWTAuth(SecurityBase):
    def __init__(self, scheme_name: str | None = None, auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> str | None:
        authorization = request.get_header(request.headers.get("Authentication"))
        scheme, token_param = get_authorization_scheme_param(
            authorization_header_value=authorization
        )
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(HTTP_403_FORBIDDEN, detail="Not Authenticated")
            else:
                return None
        encrypted_token = jwt.JWT(key=key, jwt=token_param)
        signed_token = jwt.JWT(key=key, jwt=encrypted_token.claims)
        return signed_token.claims
