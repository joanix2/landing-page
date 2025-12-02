"""Route pour les suggestions IA."""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from src.config import get_db
from src.services.ai_service import get_ai_service

router = APIRouter(prefix="/ai", tags=["IA"])


class DescriptionInput(BaseModel):
    """Schéma pour la description du projet."""
    
    description_projet: str = Field(
        ...,
        min_length=20,
        description="Description du projet (minimum 20 caractères)"
    )


@router.post("/suggest", status_code=status.HTTP_200_OK)
async def suggest_estimation_params(
    data: DescriptionInput,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtenir des suggestions IA pour les paramètres d'estimation.
    
    Utilise un cache PostgreSQL pour éviter les appels répétés à l'API OpenAI.
    
    Analyse la description du projet et suggère :
    - Type de projet
    - Nombre de pages
    - Délai souhaité
    - Budget estimé
    """
    try:
        ai_service = get_ai_service()
        result = await ai_service.analyze_and_suggest(data.description_projet, db)
        return result
        
    except ValueError as e:
        # Erreur de configuration (ex: clé API manquante)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service IA non disponible : {str(e)}"
        )
    except Exception as e:
        # Autres erreurs
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la génération des suggestions"
        )
