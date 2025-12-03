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
        # 1. Vérifier si le client existe déjà dans la base
        result = await db.execute(
            select(Client).where(Client.email == client_in.email)
        )
        existing_client = result.scalar_one_or_none()
        
        # Variable pour savoir si on doit envoyer l'email
        should_send_email = False
        
        if not existing_client:
            # CAS 1: Client n'existe pas → Créer nouveau client avec newsletter=True
            client = Client(email=client_in.email, newsletter=True)
            db.add(client)
            await db.commit()
            await db.refresh(client)
            should_send_email = True
            
        elif not existing_client.newsletter:
            # CAS 2: Client existe mais n'était pas abonné → Réabonner (newsletter=True)
            existing_client.newsletter = True
            await db.commit()
            should_send_email = True
            
        else:
            # CAS 3: Client existe et est déjà abonné → Rien à faire
            pass
        
        # 2. Envoyer l'email de confirmation uniquement si nécessaire
        if should_send_email:
            email_service = EmailService()
            email_sent = email_service.send_newsletter_confirmation(client_in.email)
            
            if not email_sent:
                # Rollback de l'inscription si l'email n'a pas pu être envoyé
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Impossible d'envoyer l'email de confirmation. Veuillez réessayer plus tard."
                )
        
        # 3. Retourner la réponse
        return {
            "message": "Merci pour votre inscription !" if should_send_email else "Vous êtes déjà inscrit à notre newsletter.",
            "email_sent": should_send_email
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
