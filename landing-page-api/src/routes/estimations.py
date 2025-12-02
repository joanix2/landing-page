"""Routes pour la gestion des estimations."""

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_db
from src.models import Client, Estimation
from src.schemas import EstimationCreate

router = APIRouter(prefix="/estimations", tags=["Estimations"])


@router.post("", status_code=status.HTTP_200_OK)
async def create_estimation(
    data: EstimationCreate, db: AsyncSession = Depends(get_db)
):
    """
    Créer une estimation avec les informations du client.
    Crée le client si l'email n'existe pas, ou met à jour ses informations.
    """
    # Rechercher le client par email
    result = await db.execute(
        select(Client).where(Client.email == data.client.email)
    )
    client = result.scalar_one_or_none()
    
    # Si le client n'existe pas, le créer
    if not client:
        client = Client(
            email=data.client.email,
            prenom=data.client.prenom,
            nom=data.client.nom,
            telephone=data.client.telephone,
            newsletter=True  # On considère qu'ils sont intéressés
        )
        db.add(client)
        await db.flush()  # Pour obtenir l'ID du client
    else:
        # Mettre à jour les informations du client si elles sont fournies
        if data.client.prenom is not None:
            client.prenom = data.client.prenom
        if data.client.nom is not None:
            client.nom = data.client.nom
        if data.client.telephone is not None:
            client.telephone = data.client.telephone
    
    # Créer l'estimation
    estimation = Estimation(
        client_id=client.id,
        description_projet=data.estimation.description_projet,
        type_projet=data.estimation.type_projet,
        nombre_pages=data.estimation.nombre_pages,
        delai_souhaite=data.estimation.delai_souhaite,
        budget=data.estimation.budget,
    )
    db.add(estimation)
    await db.commit()
    
    return {"message": "Estimation créée avec succès !"}
