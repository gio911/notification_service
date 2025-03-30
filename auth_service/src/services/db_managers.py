from datetime import datetime, timedelta
from typing import List, Optional, Any
from uuid import UUID
import uuid
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt
from sqlalchemy import select, delete
from jose import jwt
from sqlalchemy.exc import SQLAlchemyError

class AuthenticationError(Exception):
    """Исключение для ошибок аутентификации"""
    pass
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"  # Секретный ключ для подписи токенов
ALGORITHM = "HS256"  # Алгоритм шифрования токена
class PostgresManager:
    
    def __init__(self, session:AsyncSession):
        self.session=session
    
    async def get_by_id(self, model, id):
        stmt = select(model).where(model.id==id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        return user
