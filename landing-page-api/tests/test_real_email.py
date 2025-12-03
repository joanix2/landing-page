#!/usr/bin/env python3
"""Test réel d'envoi d'email de newsletter."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.services import EmailService

def test_real_email_send():
    """Tester l'envoi réel d'un email."""
    print("=" * 60)
    print("📧 TEST ENVOI RÉEL D'EMAIL NEWSLETTER")
    print("=" * 60)
    
    # Initialiser le service
    email_service = EmailService()
    
    print(f"\n📤 Configuration SMTP:")
    print(f"   Server: {email_service.smtp_server}:{email_service.smtp_port}")
    print(f"   From: {email_service.sender_email}")
    print(f"   Password: {'✅ Configuré' if email_service.password else '❌ Manquant'}")
    
    # Email de test
    test_email = "j.dussauld@orange.fr"
    
    print(f"\n📨 Envoi d'email à: {test_email}")
    print("   (cela peut prendre quelques secondes...)")
    
    try:
        success = email_service.send_newsletter_confirmation(test_email)
        
        if success:
            print("\n✅ Email envoyé avec succès !")
            print(f"   Vérifiez votre boîte mail: {test_email}")
            return 0
        else:
            print("\n❌ Échec de l'envoi")
            return 1
            
    except Exception as e:
        print(f"\n❌ Erreur lors de l'envoi: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_real_email_send())
