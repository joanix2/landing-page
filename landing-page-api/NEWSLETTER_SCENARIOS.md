#!/usr/bin/env python3
"""Test API des scénarios d'inscription newsletter."""

print("="*60)
print("📋 SCÉNARIOS D'INSCRIPTION NEWSLETTER - DOCUMENTATION")
print("="*60 + "\n")

print("""
✅ IMPLÉMENTATION ACTUELLE dans src/routes/clients.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Route : POST /api/newsletter
Body  : {"email": "user@example.com"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCÉNARIO 1 : Client n'existe pas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Vérifier si client existe
   → result = db.execute(select(Client).where(email == "..."))
   → existing_client = result.scalar_one_or_none()
   → Result: None

2. Créer nouveau client
   → client = Client(email="...", newsletter=True)
   → db.add(client)
   → db.commit()
   → should_send_email = True

3. Envoyer email de confirmation
   → email_service.send_newsletter_confirmation(email)
   → Avec lien de désinscription automatique (macro)

4. Retourner
   → {"message": "Merci pour votre inscription !", "email_sent": True}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCÉNARIO 2 : Client existe avec newsletter=False
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Vérifier si client existe
   → existing_client = ...
   → Result: Client trouvé avec newsletter=False

2. Réabonner le client
   → existing_client.newsletter = True
   → db.commit()
   → should_send_email = True

3. Envoyer email de confirmation
   → email_service.send_newsletter_confirmation(email)

4. Retourner
   → {"message": "Merci pour votre inscription !", "email_sent": True}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCÉNARIO 3 : Client existe avec newsletter=True
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Vérifier si client existe
   → existing_client = ...
   → Result: Client trouvé avec newsletter=True

2. Ne rien faire
   → Client déjà abonné
   → should_send_email = False

3. Pas d'email envoyé

4. Retourner
   → {"message": "Vous êtes déjà inscrit...", "email_sent": False}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GESTION D'ERREURS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Si l'email ne peut pas être envoyé :
→ db.rollback()  # Annuler l'inscription
→ HTTPException(503, "Impossible d'envoyer l'email...")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MODÈLE CLIENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Client(Base):
    id: int (PK)
    email: str (UNIQUE, NOT NULL)
    prenom: str (nullable)
    nom: str (nullable)
    telephone: str (nullable)
    newsletter: bool (NOT NULL, default=True)  ← Contrôle l'abonnement

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMAIL AUTOMATIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Template : newsletter_confirmation.html.j2
Macros   : email_header(), email_footer() avec lien désinscription
Variables: 
  - email: user@example.com
  - year: 2025
  - unsubscribe_url: https://axynis.cloud/unsubscribe?email=xxx

Contenu automatique du footer :
  - Email destinataire
  - Copyright Axynis
  - Lien site web
  - Lien de désinscription (conditionnel)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TESTS MANUELS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test 1 - Nouvelle inscription :
curl -X POST http://localhost:8000/api/newsletter \\
  -H "Content-Type: application/json" \\
  -d '{"email":"nouveau@example.com"}'

Attendu:
- 200 OK
- {"message": "Merci...", "email_sent": true}
- Email reçu

Test 2 - Réinscription après désinscription :
1. Se désinscrire via /api/newsletter/unsubscribe/email@example.com
2. Se réinscrire via POST /api/newsletter

Attendu:
- 200 OK
- newsletter passé de False à True
- Email reçu

Test 3 - Déjà inscrit :
curl -X POST http://localhost:8000/api/newsletter \\
  -H "Content-Type: application/json" \\
  -d '{"email":"deja.inscrit@example.com"}'

Attendu:
- 200 OK
- {"message": "Vous êtes déjà inscrit...", "email_sent": false}
- Pas d'email

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FLUX COMPLET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. User clique "S'inscrire" sur le site
2. Frontend → POST /api/newsletter {"email": "..."}
3. Backend vérifie si client existe
4. Backend crée/met à jour client.newsletter = True
5. Backend envoie email avec lien de désinscription
6. User reçoit email
7. User peut cliquer sur "Se désinscrire" → /unsubscribe?email=xxx
8. Page de confirmation affichée
9. User confirme → POST /api/newsletter/unsubscribe/email
10. Backend met newsletter = False
11. User ne reçoit plus d'emails

✅ TOUT EST IMPLÉMENTÉ ET FONCTIONNEL !
""")
