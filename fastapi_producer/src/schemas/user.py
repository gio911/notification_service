from pydantic import BaseModel


class User(BaseModel):
    user_id: str


class NewUser(BaseModel):
    name: str
    email: str
