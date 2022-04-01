from pydantic import BaseModel


class AuthenticationRequest(BaseModel):
    username: str
    password: str
