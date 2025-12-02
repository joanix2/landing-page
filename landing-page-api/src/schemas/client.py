"""Schémas Pydantic pour Client."""

from pydantic import BaseModel, EmailStr, ConfigDict


class ClientBase(BaseModel):
    """Schéma de base pour un client."""
    
    email: EmailStr


class ClientCreate(ClientBase):
    """Schéma pour créer un client (inscription newsletter)."""
    pass


class ClientRead(ClientBase):
    """Schéma pour lire un client."""
    
    model_config = ConfigDict(from_attributes=True)
    id: int
    newsletter: bool
