"""Schémas Pydantic pour Estimation."""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr

# Types énumérés
TypeProjet = Literal[
    "Landing Page",
    "Site Vitrine",
    "E-commerce",
    "Projet Sur Mesure",
]

DelaiSouhaite = Literal["Rapide", "Normal", "Flexible"]
BudgetType = Literal[
    "Moins de 5 000€",
    "5 000€ - 10 000€",
    "10 000€ - 20 000€",
    "Plus de 20 000€",
]


class ClientInfo(BaseModel):
    """Informations du client pour une estimation."""
    
    email: EmailStr
    prenom: Optional[str] = None
    nom: Optional[str] = None
    telephone: Optional[str] = None


class EstimationData(BaseModel):
    """Données de l'estimation."""
    
    description_projet: str
    type_projet: TypeProjet
    nombre_pages: int = Field(ge=1)
    delai_souhaite: DelaiSouhaite
    budget: BudgetType


class EstimationCreate(BaseModel):
    """Schéma pour créer une estimation avec les infos du client."""
    
    client: ClientInfo
    estimation: EstimationData


class EstimationRead(BaseModel):
    """Schéma pour lire une estimation."""
    
    model_config = ConfigDict(from_attributes=True)
    id: int
    client_id: int
    description_projet: str
    type_projet: str
    nombre_pages: int
    delai_souhaite: str
    budget: str
    created_at: datetime
