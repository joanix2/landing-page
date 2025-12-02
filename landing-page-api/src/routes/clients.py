"""Routes pour la gestion des clients."""

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_db
from src.models import Client
from src.schemas import ClientCreate

router = APIRouter(prefix="/newsletter", tags=["Newsletter"])


@router.post("", status_code=status.HTTP_200_OK)
async def subscribe_newsletter(client_in: ClientCreate, db: AsyncSession = Depends(get_db)):
    """
    Inscrire un email à la newsletter.
    Retourne toujours 200 OK même si l'email existe déjà (anti-bot).
    """
    # Vérifier si l'email existe déjà
    result = await db.execute(
        select(Client).where(Client.email == client_in.email)
    )
    existing_client = result.scalar_one_or_none()
    
    # Si l'email n'existe pas, créer un nouveau client
    if not existing_client:
        client = Client(email=client_in.email, newsletter=True)
        db.add(client)
        await db.commit()
    
    # Toujours retourner 200 OK sans détails (anti-bot)
    return {"message": "Merci pour votre inscription !"}
