from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: str
    email: str
    created_at: str

    class Config:
        orm_mode = True

class ModuleCreate(BaseModel):
    name: str

class ModuleAssign(BaseModel):
    email: str
    module: str