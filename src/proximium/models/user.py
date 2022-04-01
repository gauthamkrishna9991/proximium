from pydantic import BaseModel, UUID4

class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: UUID4
    
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
