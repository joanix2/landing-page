# Services

Ce dossier contient tous les services métier de l'application.

## Structure

```
services/
├── __init__.py           # Exports centralisés des services
├── ai_service/           # Service d'intelligence artificielle
│   ├── __init__.py
│   ├── ai_service.py
│   ├── README.md
│   └── templates/
│       ├── system_prompt.txt.j2
│       └── user_prompt.txt.j2
└── email_service/        # Service d'envoi d'emails
    ├── __init__.py
    ├── email_service.py
    ├── README.md
    └── templates/
        ├── newsletter_confirmation.html.j2
        ├── newsletter_confirmation.txt.j2
        ├── estimation_confirmation.html.j2
        ├── estimation_confirmation.txt.j2
        ├── admin_notification.html.j2
        └── admin_notification.txt.j2
```

## Services disponibles

### 🤖 AIService

Service d'intelligence artificielle pour générer des suggestions d'estimation de projet.

**Fonctionnalités :**

- Analyse de descriptions de projet en langage naturel
- Suggestion de type de projet (Landing Page, Site Vitrine, E-commerce, Sur Mesure)
- Génération automatique de liste de pages
- Cache des résultats pour optimiser les performances

**Documentation :** [ai_service/README.md](./ai_service/README.md)

### 📧 EmailService

Service d'envoi d'emails transactionnels avec templates Jinja2.

**Fonctionnalités :**

- Confirmation d'inscription à la newsletter
- Confirmation de demande d'estimation (client)
- Notification admin de nouvelle estimation
- Support HTML + texte brut
- Templates personnalisables

**Documentation :** [email_service/README.md](./email_service/README.md)

## Utilisation

### Import centralisé

```python
from src.services import AIService, EmailService

# Initialiser les services
ai_service = AIService()
email_service = EmailService()
```

### Import spécifique

```python
from src.services.ai_service import AIService, EstimationSuggestion
from src.services.email_service import EmailService
```

## Configuration

Chaque service a ses propres variables d'environnement. Consultez le README de chaque service pour les détails.

### Variables requises globalement

```bash
# AI Service
OPENAI_API_KEY=sk-...

# Email Service
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=587
SMTP_EMAIL=contact@axynis.cloud
SMTP_PASSWORD=...
ADMIN_EMAIL=admin@axynis.cloud
```

## Dépendances

### AI Service

```
langchain-openai>=0.0.2
langchain>=0.1.0
jinja2>=3.1.2
pydantic>=2.0.0
```

### Email Service

```
jinja2>=3.1.2
```

## Architecture

Chaque service suit une structure cohérente :

1. **Module principal** (`service_name.py`) : Contient la classe du service
2. **`__init__.py`** : Exporte les classes et fonctions publiques
3. **`templates/`** : Templates Jinja2 spécifiques au service
4. **`README.md`** : Documentation détaillée du service

### Principes

- ✅ **Isolation** : Chaque service a ses propres dépendances et templates
- ✅ **Réutilisabilité** : Services utilisables indépendamment
- ✅ **Testabilité** : Chaque service peut être testé en isolation
- ✅ **Documentation** : README dédié par service
- ✅ **Configuration** : Variables d'environnement clairement définies

## Tests

```bash
# Tester le service AI
python -m pytest tests/test_ai_service.py

# Tester le service Email
python -m pytest tests/test_email_service.py
```

## Ajout d'un nouveau service

1. Créer un nouveau dossier `nouveau_service/`
2. Créer `__init__.py`, `nouveau_service.py`, `README.md`
3. Ajouter les templates dans `nouveau_service/templates/`
4. Exporter dans `services/__init__.py`
5. Ajouter les dépendances dans `requirements.txt`
6. Documenter dans ce README

## Support

Pour toute question sur un service spécifique, consultez son README dédié.
