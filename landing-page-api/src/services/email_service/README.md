# Service Email

Service d'envoi d'emails via SMTP avec templates Jinja2 pour les différents types de notifications.

## Structure

```
email_service/
├── __init__.py              # Export du service
├── email_service.py         # Classe principale EmailService
└── templates/               # Templates Jinja2 pour les emails
    ├── newsletter_confirmation.html.j2
    ├── newsletter_confirmation.txt.j2
    ├── estimation_confirmation.html.j2
    ├── estimation_confirmation.txt.j2
    ├── admin_notification.html.j2
    └── admin_notification.txt.j2
```

## Utilisation

```python
from src.services import EmailService

# Initialiser le service
email_service = EmailService()

# Envoyer une confirmation de newsletter
email_service.send_newsletter_confirmation(
    email="client@example.com"
)

# Envoyer une confirmation d'estimation
email_service.send_estimation_confirmation(
    client={
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@example.com"
    },
    estimation={
        "type_projet": "E-commerce",
        "budget": "5000-10000€",
        "delai": "3 mois"
    }
)

# Notifier l'admin d'une nouvelle estimation
email_service.send_admin_notification(
    estimation_data={...}
)
```

## Configuration requise

### Variables d'environnement

- `SMTP_SERVER` : Serveur SMTP (défaut: smtp.hostinger.com)
- `SMTP_PORT` : Port SMTP (défaut: 587)
- `SMTP_EMAIL` : Email expéditeur (ex: contact@axynis.cloud)
- `SMTP_PASSWORD` : Mot de passe SMTP (obligatoire)
- `ADMIN_EMAIL` : Email de l'administrateur pour les notifications

### Dépendances

- `jinja2>=3.1.2`
- Librairie standard Python : `smtplib`, `email`, `ssl`

## Templates

Chaque type d'email a deux versions :

- **`.html.j2`** : Version HTML enrichie
- **`.txt.j2`** : Version texte brut (fallback)

### Variables disponibles

#### newsletter_confirmation

- `{{ email }}` : Email du destinataire

#### estimation_confirmation

- `{{ client.nom }}` : Nom du client
- `{{ client.prenom }}` : Prénom du client
- `{{ client.email }}` : Email du client
- `{{ estimation.type_projet }}` : Type de projet
- `{{ estimation.budget }}` : Budget estimé
- `{{ estimation.delai }}` : Délai estimé
- `{{ estimation.liste_pages }}` : Liste des pages (si applicable)

#### admin_notification

- `{{ client_nom }}` : Nom complet du client
- `{{ client_email }}` : Email du client
- `{{ type_projet }}` : Type de projet
- `{{ description }}` : Description du projet
- `{{ budget }}` : Budget
- `{{ date }}` : Date de soumission

## Sécurité

- Utilise TLS/STARTTLS pour la connexion SMTP
- Les mots de passe ne sont jamais loggés
- Gestion des erreurs avec logs appropriés
