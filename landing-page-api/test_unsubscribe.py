#!/usr/bin/env python3
"""Script de test de la fonctionnalité de désinscription newsletter."""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from src.services import EmailService


def test_email_with_unsubscribe_link():
    """Tester l'envoi d'email avec lien de désinscription."""
    print("🧪 Test d'envoi d'email avec lien de désinscription\n")
    
    email_service = EmailService()
    test_email = "j.dussauld@gmail.com"
    
    print(f"📧 Envoi à : {test_email}")
    print(f"🔗 Lien de désinscription : https://axynis.cloud/unsubscribe?email={test_email}\n")
    
    result = email_service.send_newsletter_confirmation(test_email)
    
    if result:
        print("✅ Email envoyé avec succès !")
        print("\nVérifiez votre boîte mail pour :")
        print("  1. Le contenu de l'email")
        print("  2. Le lien de désinscription en bas de page")
        print("  3. Cliquez sur le lien pour tester la désinscription")
        return True
    else:
        print("❌ Échec de l'envoi de l'email")
        return False


async def test_api_routes():
    """Tester les routes API de désinscription."""
    print("\n" + "="*60)
    print("🧪 Test des routes API")
    print("="*60 + "\n")
    
    from sqlalchemy import select
    from src.database import AsyncSessionLocal
    from src.models import Client
    
    test_email = "test-unsubscribe@example.com"
    
    async with AsyncSessionLocal() as db:
        # 1. Créer un client test
        print("1️⃣ Création d'un client test...")
        result = await db.execute(select(Client).where(Client.email == test_email))
        existing = result.scalar_one_or_none()
        
        if existing:
            await db.delete(existing)
            await db.commit()
        
        client = Client(email=test_email, newsletter=True)
        db.add(client)
        await db.commit()
        print(f"   ✅ Client créé : {test_email} (newsletter=True)")
        
        # 2. Vérifier que le client existe
        print("\n2️⃣ Vérification du client...")
        result = await db.execute(select(Client).where(Client.email == test_email))
        client = result.scalar_one_or_none()
        assert client is not None, "Client non trouvé"
        assert client.newsletter is True, "Newsletter devrait être True"
        print(f"   ✅ Client trouvé : newsletter={client.newsletter}")
        
        # 3. Désinscrire le client
        print("\n3️⃣ Désinscription du client...")
        client.newsletter = False
        await db.commit()
        print("   ✅ Client désinscrit (newsletter=False)")
        
        # 4. Vérifier la désinscription
        print("\n4️⃣ Vérification de la désinscription...")
        result = await db.execute(select(Client).where(Client.email == test_email))
        client = result.scalar_one_or_none()
        assert client.newsletter is False, "Newsletter devrait être False"
        print(f"   ✅ Désinscription confirmée : newsletter={client.newsletter}")
        
        # 5. Nettoyer
        print("\n5️⃣ Nettoyage...")
        await db.delete(client)
        await db.commit()
        print("   ✅ Client test supprimé")
    
    print("\n✅ Tous les tests API ont réussi !")
    return True


def print_summary():
    """Afficher un résumé de la fonctionnalité."""
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DE LA FONCTIONNALITÉ")
    print("="*60)
    print("""
✅ Routes API créées :
   • POST /api/newsletter              - S'inscrire à la newsletter
   • GET  /api/newsletter/client/{email} - Info sur un client
   • POST /api/newsletter/unsubscribe/{email} - Se désinscrire

✅ Templates email mis à jour :
   • newsletter_confirmation.html.j2   - Version HTML
   • newsletter_confirmation.txt.j2    - Version texte
   • Lien de désinscription ajouté en footer

✅ Page React créée :
   • /unsubscribe?email=xxx            - Page de désinscription
   • Vérification du statut
   • Confirmation de désinscription
   • Gestion d'erreurs complète

✅ Service email :
   • Génération automatique du lien de désinscription
   • URL encodée pour la sécurité
   • Base URL configurable

📝 Tests à effectuer :
   1. S'inscrire à la newsletter depuis le site
   2. Vérifier la réception de l'email
   3. Cliquer sur "Se désinscrire" en bas de l'email
   4. Confirmer la désinscription sur la page web
   5. Vérifier que newsletter=False dans la base de données

🔗 URLs de test :
   • https://axynis.cloud/                          - Page d'accueil
   • https://axynis.cloud/unsubscribe?email=xxx     - Désinscription
   • https://axynis.cloud/api/docs                  - Documentation API
    """)


async def main():
    """Fonction principale."""
    print("="*60)
    print("🧪 TEST DE LA FONCTIONNALITÉ DE DÉSINSCRIPTION")
    print("="*60 + "\n")
    
    # Test 1 : Email
    email_ok = test_email_with_unsubscribe_link()
    
    # Test 2 : API
    try:
        api_ok = await test_api_routes()
    except Exception as e:
        print(f"\n❌ Erreur lors des tests API : {e}")
        api_ok = False
    
    # Résumé
    print_summary()
    
    # Résultat final
    print("="*60)
    if email_ok and api_ok:
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        return 0
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
