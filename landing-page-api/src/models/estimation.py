"""Modèle Estimation."""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Estimation(Base):
    """Modèle pour les estimations de projets."""
    
    __tablename__ = "estimations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))

    description_projet: Mapped[str] = mapped_column(Text, nullable=False)
    type_projet: Mapped[str] = mapped_column(String(50), nullable=False)
    nombre_pages: Mapped[int] = mapped_column(Integer, nullable=False)
    delai_souhaite: Mapped[str] = mapped_column(String(50), nullable=False)
    budget: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relation
    client: Mapped["Client"] = relationship(back_populates="estimations")
