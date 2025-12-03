# Newsletter avec Email de Confirmation

## 📧 Fonctionnalité

Lors de l'inscription à la newsletter via l'endpoint `/api/newsletter`, le système :

1. ✅ Vérifie si l'email existe déjà en base de données
2. ✅ Crée un nouveau client ou met à jour l'abonnement existant
3. ✅ Envoie un email de confirmation automatique
4. ❌ Retourne une erreur si l'envoi d'email échoue

## 🔧 Configuration requise

### Variables d'environnement (.env)

```bash
# Configuration SMTP (obligatoire)
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=587
SMTP_EMAIL=contact@axynis.cloud
SMTP_PASSWORD=votre_mot_de_passe_smtp
```

⚠️ **Important** : Sans `SMTP_PASSWORD`, l'inscription échouera avec une erreur 503.

## 🛣️ Endpoint API

### POST `/api/newsletter`

Inscrit un email à la newsletter et envoie un email de confirmation.

**Request Body:**

```json
{
  "email": "utilisateur@example.com"
}
```

**Success Response (200 OK):**

```json
{
  "message": "Merci pour votre inscription !",
  "email_sent": true
}
```

**Error Responses:**

- **503 Service Unavailable** : Email de confirmation non envoyé

  ```json
  {
    "detail": "Impossible d'envoyer l'email de confirmation. Veuillez réessayer plus tard."
  }
  ```

- **500 Internal Server Error** : Erreur système
  ```json
  {
    "detail": "Erreur lors de l'inscription : [détails]"
  }
  ```

## 📝 Templates Email

L'email de confirmation utilise deux templates Jinja2 :

- **HTML** : `src/services/email_service/templates/newsletter_confirmation.html.j2`
- **Texte** : `src/services/email_service/templates/newsletter_confirmation.txt.j2`

### Variables disponibles

- `{{ email }}` : Email du destinataire

### Exemple de contenu

**Objet:** Bienvenue dans notre newsletter !

**Corps (texte):**

```
Bonjour,

Merci de vous être inscrit(e) à notre newsletter !

Vous recevrez désormais nos dernières actualités, conseils et offres exclusives
directement dans votre boîte mail.

À bientôt,
L'équipe Axynis
```

## 🧪 Tests

### Test automatique

```bash
python test_newsletter.py
```

### Test avec curl (API en cours d'exécution)

```bash
# Démarrer l'API
uvicorn src.main:app --reload

# Tester l'inscription
curl -X POST http://localhost:8000/api/newsletter \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

### Test avec Docker

```bash
# Avec docker-compose
docker-compose up -d

# Tester l'inscription
curl -X POST http://localhost:8000/api/newsletter \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

## 🔐 Sécurité

### Gestion des doublons

- Si l'email existe déjà ET est déjà abonné : pas d'email envoyé, retour 200 OK
- Si l'email existe mais n'était pas abonné : mise à jour + email envoyé
- Si l'email est nouveau : création + email envoyé

### Protection contre le spam

- L'inscription est transactionnelle : si l'email échoue, l'inscription est annulée (rollback)
- Gestion d'erreurs appropriée pour éviter les fuites d'information

### Validation

- L'email est validé par Pydantic avec le type `EmailStr`
- Format d'email vérifié automatiquement

## 📊 Logs

Le service email génère des logs :

```python
✅ Email envoyé à utilisateur@example.com
❌ Erreur lors de l'envoi de l'email à utilisateur@example.com: [détail]
```

## 🐛 Dépannage

### "SMTP_PASSWORD non défini dans .env"

**Solution** : Ajouter `SMTP_PASSWORD` dans le fichier `.env`

```bash
SMTP_PASSWORD=votre_mot_de_passe
```

### "Authentication failed"

**Causes possibles** :

- Mot de passe SMTP incorrect
- Compte email bloqué
- Authentification 2FA activée

**Solution** : Vérifier les credentials SMTP auprès de votre hébergeur

### "Connection refused"

**Causes possibles** :

- SMTP_SERVER ou SMTP_PORT incorrect
- Firewall bloquant le port 587

**Solution** : Vérifier la configuration SMTP

### Email non reçu mais statut 200

**Causes possibles** :

- Email marqué comme spam
- Quota d'envoi dépassé
- Délai de livraison

**Solution** : Vérifier les dossiers spam, attendre quelques minutes

## 🚀 Prochaines améliorations possibles

- [ ] File d'attente d'emails avec Celery/Redis
- [ ] Retry automatique en cas d'échec temporaire
- [ ] Confirmation de désabonnement (unsubscribe link)
- [ ] Analytics d'ouverture d'emails
- [ ] Rate limiting sur l'endpoint
- [ ] CAPTCHA pour éviter les bots

## 📚 Voir aussi

- [Service Email Documentation](src/services/email_service/README.md)
- [Configuration des Services](SERVICES_CONFIGURATION.md)
- [API Endpoints](docs/API_ENDPOINTS.md)
