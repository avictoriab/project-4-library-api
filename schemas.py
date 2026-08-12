from pydantic import BaseModel, ValidationError

class BookSchema(BaseModel):
    title: str
    author: str

class UserSchema(BaseModel):
    username: str
    password: str