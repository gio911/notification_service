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
ACCESS_TOKEN_EXPIRE_MINUTES = 1  # Время жизни токена в минутах
REFRESH_TOKEN_EXPIRE_DAYS = 7

class PostgresManager:
    
    def __init__(self, session:AsyncSession):
        self.session=session
    
    async def get_by_id(self, model, id):
        stmt = select(model).where(model.id==id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        # print(f"User found: {user}")  # ✅ Проверяем, что объект найден

        return user
