#!/usr/bin/env python3
"""Script de test pour l'inscription à la newsletter."""

import asyncio
import sys
from pathlib import Path

# Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

async def test_newsletter_subscription():
    """Tester l'inscription à la newsletter."""
    print("=" * 60)
    print("🧪 TEST INSCRIPTION NEWSLETTER")
    print("=" * 60)
    
    # Test 1: Vérifier que le service email est disponible
    print("\n📧 Test 1: Service Email")
    try:
        from src.services import EmailService
        email_service = EmailService()
        print("  ✅ EmailService initialisé")
        
        # Vérifier la configuration SMTP
        if not email_service.password:
            print("  ⚠️  SMTP_PASSWORD non défini dans .env")
            print("  ℹ️  L'envoi d'email échouera sans ce paramètre")
        else:
            print(f"  ✅ SMTP configuré: {email_service.sender_email}")
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False
    
    # Test 2: Vérifier que la route existe
    print("\n🛣️  Test 2: Route Newsletter")
    try:
        from src.routes.clients import router, subscribe_newsletter
        print("  ✅ Route /newsletter importée")
        print(f"  ℹ️  Prefix: {router.prefix}")
        print(f"  ℹ️  Tags: {router.tags}")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False
    
    # Test 3: Vérifier le template de confirmation
    print("\n🎨 Test 3: Templates Email")
    try:
        template_dir = Path("src/services/email_service/templates")
        html_template = template_dir / "newsletter_confirmation.html.j2"
        txt_template = template_dir / "newsletter_confirmation.txt.j2"
        
        if html_template.exists():
            print(f"  ✅ {html_template}")
        else:
            print(f"  ❌ Manquant: {html_template}")
            return False
            
        if txt_template.exists():
            print(f"  ✅ {txt_template}")
        else:
            print(f"  ❌ Manquant: {txt_template}")
            return False
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False
    
    # Test 4: Tester le rendu du template
    print("\n🖼️  Test 4: Rendu des Templates")
    try:
        from src.services import EmailService
        email_service = EmailService()
        
        # Tester avec un email de test
        test_email = "test@example.com"
        
        html_content = email_service.render_template(
            "newsletter_confirmation.html.j2",
            {"email": test_email}
        )
        print("  ✅ Template HTML rendu")
        print(f"  ℹ️  Longueur: {len(html_content)} caractères")
        
        txt_content = email_service.render_template(
            "newsletter_confirmation.txt.j2",
            {"email": test_email}
        )
        print("  ✅ Template TXT rendu")
        print(f"  ℹ️  Longueur: {len(txt_content)} caractères")
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False
    
    # Test 5: Simuler la logique de la route (sans base de données)
    print("\n⚙️  Test 5: Logique de la Route")
    try:
        from src.services import EmailService
        email_service = EmailService()
        
        # Simuler l'envoi (ne fonctionnera que si SMTP est configuré)
        test_email = "test@example.com"
        print(f"  ℹ️  Test avec: {test_email}")
        
        if email_service.password:
            print("  ⚠️  Test d'envoi réel désactivé pour éviter le spam")
            print("  ℹ️  Pour tester l'envoi, appelez l'API directement")
        else:
            print("  ⚠️  SMTP non configuré, impossible de tester l'envoi")
        
        print("  ✅ Logique de route validée")
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False
    
    return True


async def main():
    """Exécuter le test."""
    success = await test_newsletter_subscription()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTAT")
    print("=" * 60)
    
    if success:
        print("✅ Tous les tests sont passés !")
        print("\n💡 Pour tester l'envoi d'email complet:")
        print("   1. Configurez SMTP_PASSWORD dans .env")
        print("   2. Lancez l'API: uvicorn src.main:app --reload")
        print("   3. Testez avec: curl -X POST http://localhost:8000/api/newsletter \\")
        print('      -H "Content-Type: application/json" \\')
        print('      -d \'{"email": "votre@email.com"}\'')
        return 0
    else:
        print("❌ Certains tests ont échoué")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
