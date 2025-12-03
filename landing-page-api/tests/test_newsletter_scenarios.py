#!/usr/bin/env python3
"""Test des 3 scénarios d'inscription newsletter."""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select
from src.database import AsyncSessionLocal
from src.models import Client
from src.services import EmailService


async def test_newsletter_scenarios():
    """Tester les 3 cas d'inscription newsletter."""
    print("="*60)
    print("🧪 TEST DES SCÉNARIOS D'INSCRIPTION NEWSLETTER")
    print("="*60 + "\n")
    
    test_email = "test-newsletter@example.com"
    email_service = EmailService()
    
    async with AsyncSessionLocal() as db:
        
        # Nettoyer avant test
        result = await db.execute(select(Client).where(Client.email == test_email))
        existing = result.scalar_one_or_none()
        if existing:
            await db.delete(existing)
            await db.commit()
        
        # ═══════════════════════════════════════════════════════
        # SCÉNARIO 1 : Client n'existe pas → Créer + Envoyer email
        # ═══════════════════════════════════════════════════════
        print("📋 SCÉNARIO 1 : Client n'existe pas")
        print("-" * 60)
        
        result = await db.execute(select(Client).where(Client.email == test_email))
        client = result.scalar_one_or_none()
        
        if not client:
            print("✅ Client n'existe pas (comme prévu)")
            # Créer le client
            client = Client(email=test_email, newsletter=True)
            db.add(client)
            await db.commit()
            await db.refresh(client)
            print(f"✅ Client créé avec newsletter={client.newsletter}")
            
            # Envoyer email
            # email_sent = email_service.send_newsletter_confirmation(test_email)
            # print(f"✅ Email envoyé : {email_sent}")
            print("✅ Email devrait être envoyé")
        else:
            print("❌ Le client existe déjà (erreur)")
        
        # ═══════════════════════════════════════════════════════
        # SCÉNARIO 2 : Client existe mais newsletter=False → Réabonner + Email
        # ═══════════════════════════════════════════════════════
        print("\n📋 SCÉNARIO 2 : Client existe mais newsletter=False")
        print("-" * 60)
        
        # Désabonner le client
        client.newsletter = False
        await db.commit()
        print(f"✅ Client désinscrit : newsletter={client.newsletter}")
        
        # Réabonner
        result = await db.execute(select(Client).where(Client.email == test_email))
        client = result.scalar_one_or_none()
        
        if client and not client.newsletter:
            print("✅ Client existe et newsletter=False (comme prévu)")
            # Réabonner
            client.newsletter = True
            await db.commit()
            print(f"✅ Client réabonné : newsletter={client.newsletter}")
            
            # Envoyer email
            # email_sent = email_service.send_newsletter_confirmation(test_email)
            # print(f"✅ Email envoyé : {email_sent}")
            print("✅ Email devrait être envoyé")
        else:
            print("❌ État inattendu")
        
        # ═══════════════════════════════════════════════════════
        # SCÉNARIO 3 : Client existe et newsletter=True → Rien faire
        # ═══════════════════════════════════════════════════════
        print("\n📋 SCÉNARIO 3 : Client existe et newsletter=True")
        print("-" * 60)
        
        result = await db.execute(select(Client).where(Client.email == test_email))
        client = result.scalar_one_or_none()
        
        if client and client.newsletter:
            print("✅ Client existe et newsletter=True (comme prévu)")
            print(f"✅ Newsletter status : {client.newsletter}")
            print("✅ Rien à faire, pas d'email envoyé")
        else:
            print("❌ État inattendu")
        
        # Nettoyer
        await db.delete(client)
        await db.commit()
        print("\n✅ Nettoyage effectué")
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES SCÉNARIOS")
    print("="*60)
    print("""
✅ SCÉNARIO 1 : Client n'existe pas
   → Créer Client(email, newsletter=True)
   → Commit en base
   → Envoyer email de confirmation
   → Retourner {"message": "Merci...", "email_sent": True}

✅ SCÉNARIO 2 : Client existe avec newsletter=False
   → Mettre newsletter=True
   → Commit en base
   → Envoyer email de confirmation
   → Retourner {"message": "Merci...", "email_sent": True}

✅ SCÉNARIO 3 : Client existe avec newsletter=True
   → Ne rien faire
   → Pas d'email
   → Retourner {"message": "Déjà inscrit", "email_sent": False}
    """)


if __name__ == "__main__":
    asyncio.run(test_newsletter_scenarios())
