from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import AsyncSessionLocal

session: AsyncSession | None = None

def get_session():
    return session