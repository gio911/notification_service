from functools import lru_cache
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status, Depends
from src.db.postgres import get_session
from .db_managers import PostgresManager
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from src.models.entity import User
from passlib.context import CryptContext
import logging

# Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6ImFkbWluIn0.pr2n_JOQfZVAw1gtL77wDFWb73fVuILG19QdzWUgYu8


SECRET_KEY = "your_secret_key"  # Секретный ключ для подписи токенов
ALGORITHM = "HS256"  # Алгоритм шифрования токена

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, pg_manager: PostgresManager):
        self.pg_manager = pg_manager
        self.logger = logging.getLogger('app')
        
    # Функция для верификации и декодирования access-токена
    async def verify_access_token_for_admin(self, authorization: str) -> Optional[str]:
        """
        Проверка и верификация access-токена с учётом refresh-токена.
        """
        try:
            # Проверка структуры заголовка
            if not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Authorization header must start with 'Bearer '"
                )

            # Извлечение токена
            access_token = authorization[7:]

            # Декодирование токена
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

            login = payload.get("login")
            if not login == "admin":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token data"
                )

            return True

        except jwt.InvalidTokenError:
            self.logger.error("Ошибка: токен недействителен")
            
        
    async def get_user_data_for_admin(self, user_id: UUID, authorization: str):
        """
        Эндпоинт для получения данных пользователя по user_id.
        Проверяет валидность токена в заголовке Authorization.
        """
        print(authorization, 899383)
        self.logger.info("Получение данных пользователя для user_id: %s", user_id)

        access_token = authorization[7:]
        self.logger.debug("Извлечён токен: %s", access_token)

        try:
            # Проверяем валидность токена
            await self.verify_access_token_for_admin(authorization)
            self.logger.debug("Токен валиден")
            
            user = await self.pg_manager.get_by_id(User, user_id)

            self.logger.info("Успешное получение данных для user_id: %s", user_id)
            return user

        except HTTPException as e:
            self.logger.error(
                "Ошибка HTTP при получении данных пользователя для user_id=%s: %s",
                user_id, str(e.detail)
            )
            raise
        except Exception as e:
            self.logger.error(
                "Неизвестная ошибка при обработке user_id=%s: %s",
                user_id, str(e)
            )
            raise
    
    async def verify_token(self,authorization):
        new_access_token_obj = await self.verify_access_token_for_admin(authorization)
        return new_access_token_obj
 
            

    
@lru_cache
def get_user_service(
    session:AsyncSession=Depends(get_session)
)->UserService:
    pg_manager=PostgresManager(session)
    return UserService(pg_manager)

