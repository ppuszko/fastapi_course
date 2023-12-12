from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
#pydantic model (also known as schema) creates the pattern of data that we want to be sent by user, the data provided by pydantic Post model is then 
# sent to the database table which is defined by a SQLAlchemy model
# so in conclusion, Post object is needed to provide a variable, that would be put in the database


class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = True
    

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_orm = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_orm = True
    
class PostOut(BaseModel):   
    Posts: Post   
    votes: int
     
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_orm = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)