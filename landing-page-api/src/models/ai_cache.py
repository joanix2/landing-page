"""Modèle pour le cache des suggestions IA."""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, Index, func, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class AISuggestionCache(Base):
    """Cache des suggestions IA pour éviter les appels répétés."""
    
    __tablename__ = "ai_suggestion_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Description du projet (utilisée comme clé de cache)
    description_hash: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    description_projet: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Suggestions générées
    type_projet: Mapped[str] = mapped_column(String(50), nullable=False)
    liste_pages: Mapped[list] = mapped_column(JSON, nullable=False)
    explication: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Métadonnées
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    used_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    last_used_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    
    # Index pour améliorer les performances
    __table_args__ = (
        Index('ix_ai_cache_created', 'created_at'),
        Index('ix_ai_cache_used', 'last_used_at'),
    )
