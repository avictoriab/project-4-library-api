from pydantic import BaseModel, ValidationError

class BookSchema(BaseModel):
    title: str
    author: str