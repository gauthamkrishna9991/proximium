from typing import List, Union
from fastapi import APIRouter, HTTPException
from proximium.models.user import User, UserCreate
from proximium.schema.user import User as UserSchema
from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST
import bcrypt

user_router = APIRouter(prefix="/user")


@user_router.post("/", response_model=User)
def create(new_user: UserCreate):
    # Check whether there is a username with the given name
    user_exists: UserSchema | None = UserSchema.objects(
        UserSchema.username == new_user.username
    ).first()
    # If user exists, then respond with a 409 Conflict.
    if user_exists is not None:
        raise HTTPException(HTTP_409_CONFLICT, "User Exists")
    pw_salt = bcrypt.gensalt()
    u: UserSchema | None = UserSchema.create(
        username=new_user.username,
        password_hash=bcrypt.hashpw(
            password=bytes(new_user.password, encoding="utf-8"), salt=pw_salt
        ),
        password_salt=pw_salt,
    )
    if u is None:
        raise HTTPException(HTTP_400_BAD_REQUEST, "User wasn't created.")
    return u
