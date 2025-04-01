from pydantic import BaseModel


class UserDataForEmail(BaseModel):
    first_name: str
    email: str
