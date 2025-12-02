"""Modèle Client."""

from typing import List, Optional
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Client(Base):
    """Modèle pour les clients."""
    
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    prenom: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    nom: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    telephone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    newsletter: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relations
    estimations: Mapped[List["Estimation"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )
