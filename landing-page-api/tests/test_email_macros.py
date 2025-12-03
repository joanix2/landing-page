#!/usr/bin/env python3
"""Script de test des macros Jinja2 pour les emails."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from src.services import EmailService


def test_macros():
    """Tester tous les templates avec les macros."""
    print("="*60)
    print("🧪 TEST DES MACROS JINJA2 POUR LES EMAILS")
    print("="*60 + "\n")
    
    email_service = EmailService()
    test_email = "j.dussauld@gmail.com"
    
    # Test 1 : Newsletter confirmation
    print("1️⃣ Test newsletter_confirmation avec macros...")
    try:
        result = email_service.send_newsletter_confirmation(test_email)
        if result:
            print("   ✅ Newsletter confirmation envoyé")
        else:
            print("   ❌ Échec newsletter confirmation")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2 : Estimation confirmation
    print("\n2️⃣ Test estimation_confirmation avec macros...")
    try:
        result = email_service.send_estimation_confirmation(
            client={
                "nom": "Test",
                "prenom": "Utilisateur",
                "email": test_email
            },
            estimation={
                "type_projet": "E-commerce",
                "description_projet": "Boutique en ligne",
                "nombre_pages": "10",
                "delai_souhaite": "3 mois",
                "budget": "5000-10000€"
            }
        )
        if result:
            print("   ✅ Estimation confirmation envoyé")
        else:
            print("   ❌ Échec estimation confirmation")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3 : Admin notification
    print("\n3️⃣ Test admin_notification avec macros...")
    try:
        result = email_service.send_admin_notification({
            "client_nom": "Test Utilisateur",
            "client_email": test_email,
            "type_projet": "E-commerce",
            "description": "Boutique en ligne de test",
            "budget": "5000-10000€",
            "date": "2025-12-03"
        })
        if result:
            print("   ✅ Admin notification envoyé")
        else:
            print("   ❌ Échec admin notification")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DES MACROS")
    print("="*60)
    print("""
✅ Macros créées :
   • email_styles()           - Styles CSS communs
   • email_header(title)       - Header avec gradient
   • email_footer(email, url)  - Footer avec désinscription
   • email_footer_text(...)    - Footer version texte

✅ Templates mis à jour :
   • newsletter_confirmation.html.j2  ✅
   • newsletter_confirmation.txt.j2   ✅
   • estimation_confirmation.html.j2  ✅
   • admin_notification.html.j2       ✅

✅ Avantages :
   • Cohérence visuelle automatique
   • Maintenance centralisée
   • Lien de désinscription automatique
   • Réutilisabilité maximale

📧 Vérifiez votre boîte mail : """ + test_email + """
    """)


if __name__ == "__main__":
    test_macros()
