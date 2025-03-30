from functools import lru_cache
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status, Depends
from src.db.postgres import get_session
from .db_managers import PostgresManager
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from src.models.entity import User
from passlib.context import CryptContext
from src.core.logging_config import setup_logging

SECRET_KEY = "your_secret_key"  # Секретный ключ для подписи токенов
ALGORITHM = "HS256"  # Алгоритм шифрования токена

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, pg_manager: PostgresManager):
        self.pg_manager = pg_manager
        self.logger = setup_logging()

    async def verify_access_token_for_admin(self, authorization: str) -> Optional[str]:
        """
        Проверка и верификация access-токена.
        """
        try:
            if not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Authorization header must start with 'Bearer '"
                )

            access_token = authorization[7:]
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            login = payload.get("login")
            print(login, 999)
            if login != "admin":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token data"
                )

            self.logger.debug("Токен успешно верифицирован для admin")
            return True

        except jwt.JWTError:
            self.logger.error("Ошибка: токен недействителен")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    async def get_user_data_for_admin(self, user_id: UUID, authorization: str):
        """
        Получение данных пользователя по user_id.
        """
        self.logger.info("Запрос данных для user_id: %s", user_id)
        access_token = authorization[7:]
        self.logger.debug("Извлечён токен: %s", access_token)

        try:
            await self.verify_access_token_for_admin(authorization)
            self.logger.debug("Токен валиден")

            user = await self.pg_manager.get_by_id(User, user_id)
            self.logger.info("Данные получены для user_id: %s", user_id)

            return user

        except HTTPException as e:
            self.logger.error("Ошибка HTTP при user_id=%s: %s", user_id, str(e.detail))
            raise
        except Exception as e:
            self.logger.error("Неизвестная ошибка для user_id=%s: %s", user_id, str(e))
            raise

    async def verify_token(self, authorization: str):
        return await self.verify_access_token_for_admin(authorization)


@lru_cache
def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    pg_manager = PostgresManager(session)
    return UserService(pg_manager)
