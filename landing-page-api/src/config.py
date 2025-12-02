"""Configuration de la base de données et de l'application."""

import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

# Charger les variables d'environnement
load_dotenv()

# Configuration PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/studio_web")

# Création du moteur et de la session
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dépendance pour obtenir une session de base de données."""
    async with AsyncSessionLocal() as session:
        yield session
