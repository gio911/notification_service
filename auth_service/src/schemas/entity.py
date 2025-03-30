from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

class User(BaseModel):
    user_id:str
    
    class Config:
        orm_mode = True 


class UserForNotification(BaseModel):
    id: UUID
    login: str
    first_name: str
    last_name: str
    email: str
    
    class Config:
        orm_mode = True 
    
