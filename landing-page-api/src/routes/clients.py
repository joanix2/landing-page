"""Routes pour la gestion des clients."""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_db
from src.models import Client
from src.schemas import ClientCreate, ClientRead
from src.services import EmailService

router = APIRouter(prefix="/newsletter", tags=["Newsletter"])


@router.post("", status_code=status.HTTP_200_OK)
async def subscribe_newsletter(client_in: ClientCreate, db: AsyncSession = Depends(get_db)):
    """
    Inscrire un email à la newsletter.
    Envoie un email de confirmation.
    Retourne une erreur si l'envoi d'email échoue.
    """
    try:
        # Vérifier si l'email existe déjà
        result = await db.execute(
            select(Client).where(Client.email == client_in.email)
        )
        existing_client = result.scalar_one_or_none()
        
        # Variable pour savoir si c'est une nouvelle inscription
        is_new_subscription = False
        
        # Si l'email n'existe pas, créer un nouveau client
        if not existing_client:
            client = Client(email=client_in.email, newsletter=True)
            db.add(client)
            await db.commit()
            is_new_subscription = True
        elif not existing_client.newsletter:
            # Si le client existe mais n'était pas abonné
            existing_client.newsletter = True
            await db.commit()
            is_new_subscription = True
        
        # Envoyer l'email de confirmation uniquement pour les nouvelles inscriptions
        if is_new_subscription:
            email_service = EmailService()
            email_sent = email_service.send_newsletter_confirmation(client_in.email)
            
            if not email_sent:
                # Rollback de l'inscription si l'email n'a pas pu être envoyé
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Impossible d'envoyer l'email de confirmation. Veuillez réessayer plus tard."
                )
        
        # Toujours retourner 200 OK pour les inscriptions réussies
        return {
            "message": "Merci pour votre inscription !",
            "email_sent": is_new_subscription
        }
        
    except HTTPException:
        # Propager les HTTPException
        raise
    except Exception as e:
        # Gérer les autres erreurs
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'inscription : {str(e)}"
        )


@router.get("/client/{email}", status_code=status.HTTP_200_OK)
async def get_client_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    Récupérer les informations d'un client par son email.
    Utilisé pour la page de désinscription.
    """
    try:
        result = await db.execute(
            select(Client).where(Client.email == email)
        )
        client = result.scalar_one_or_none()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email non trouvé"
            )
        
        return {
            "id": client.id,
            "email": client.email,
            "prenom": client.prenom,
            "nom": client.nom,
            "newsletter": client.newsletter
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du client : {str(e)}"
        )


@router.post("/unsubscribe/{email}", status_code=status.HTTP_200_OK)
async def unsubscribe_newsletter(email: str, db: AsyncSession = Depends(get_db)):
    """
    Désinscrire un email de la newsletter.
    Met le champ newsletter à False.
    """
    try:
        result = await db.execute(
            select(Client).where(Client.email == email)
        )
        client = result.scalar_one_or_none()
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email non trouvé dans notre base de données"
            )
        
        if not client.newsletter:
            return {
                "message": "Vous êtes déjà désinscrit de notre newsletter",
                "email": email,
                "newsletter": False
            }
        
        # Désinscrire le client
        client.newsletter = False
        await db.commit()
        
        return {
            "message": "Vous avez été désinscrit avec succès de notre newsletter",
            "email": email,
            "newsletter": False
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la désinscription : {str(e)}"
        )
