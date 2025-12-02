# Marketing Bot - Landing Page

Application complète avec Frontend React, API FastAPI, PostgreSQL et Nginx Proxy Manager.

## 🏗️ Architecture

- **Frontend**: React + Vite + TailwindCSS
- **Backend**: FastAPI + SQLAlchemy + Langchain
- **Base de données**: PostgreSQL 16
- **Visualisation DB**: pgAdmin 4
- **Reverse Proxy**: Nginx Proxy Manager (avec interface graphique)
- **Containerisation**: Docker + Docker Compose

## 📋 Prérequis

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- Clé API OpenAI

## 🚀 Démarrage rapide

### 1. Configuration de l'environnement

Copiez le fichier d'exemple et configurez vos variables :

```bash
cp .env.example .env
```

Éditez `.env` et ajoutez votre clé API OpenAI :

```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 2. Lancement de l'application

Démarrez tous les services :

```bash
docker-compose up -d
```

Ou pour voir les logs en temps réel :

```bash
docker-compose up
```

### 3. Build initial (si nécessaire)

Si c'est la première fois ou après des modifications :

```bash
docker-compose up --build
```

## 🌐 Accès aux services

Une fois les conteneurs démarrés :

- **Nginx Proxy Manager (Interface Admin)**: http://localhost:81
  - Première connexion : `admin@example.com` / `changeme`
  - ⚠️ Changez ces identifiants lors de la première connexion !
- **Application Frontend**: http://localhost (après config NPM)
- **API Backend**: http://localhost/api (après config NPM)
- **Documentation API (Swagger)**: http://localhost/docs (après config NPM)
- **pgAdmin (Visualisation DB)**: http://localhost:5050
  - Email: `admin@admin.com`
  - Mot de passe: `admin123`

📖 **Consultez [NGINX_PROXY_MANAGER_SETUP.md](./NGINX_PROXY_MANAGER_SETUP.md) pour configurer les proxies via l'interface graphique.**

### Configuration de pgAdmin

1. Accédez à http://localhost:5050
2. Connectez-vous avec les identifiants ci-dessus
3. Ajoutez un nouveau serveur :
   - **Host**: `postgres`
   - **Port**: `5432`
   - **Database**: `marketing_bot`
   - **Username**: `admin`
   - **Password**: `admin123`

## 🛠️ Commandes utiles

### Gestion des conteneurs

```bash
# Démarrer les services
docker-compose up -d

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f api
docker-compose logs -f frontend
docker-compose logs -f nginx

# Reconstruire les images
docker-compose build

# Redémarrer un service
docker-compose restart api
```

### Gestion de la base de données

```bash
# Accéder au conteneur PostgreSQL
docker-compose exec postgres psql -U admin -d marketing_bot

# Sauvegarder la base de données
docker-compose exec postgres pg_dump -U admin marketing_bot > backup.sql

# Restaurer la base de données
docker-compose exec -T postgres psql -U admin marketing_bot < backup.sql
```

### Développement

```bash
# Accéder au shell du conteneur API
docker-compose exec api bash

# Accéder au shell du conteneur Frontend
docker-compose exec frontend sh

# Installer des dépendances Python
docker-compose exec api pip install nouvelle-dependance
docker-compose exec api pip freeze > requirements.txt

# Installer des dépendances npm
docker-compose exec frontend npm install nouvelle-dependance
```

## 📁 Structure du projet

```
.
├── docker-compose.yml           # Configuration des services
├── .env                         # Variables d'environnement (à créer)
├── .env.example                 # Exemple de configuration
├── landing-page-api/           # Backend FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
├── landing-page-front/         # Frontend React
│   ├── Dockerfile
│   ├── Dockerfile.prod         # Build de production
│   ├── package.json
│   └── src/
└── nginx/                      # Configuration Nginx
    ├── Dockerfile
    ├── nginx.conf
    └── conf.d/
        └── default.conf
```

## 🔧 Configuration avancée

### Variables d'environnement

Principales variables configurables dans `.env` :

- `OPENAI_API_KEY`: Votre clé API OpenAI
- `DATABASE_URL`: URL de connexion PostgreSQL
- `VITE_API_URL`: URL de l'API pour le frontend

### Ports

Les ports par défaut peuvent être modifiés dans `docker-compose.yml` :

- `80`: Nginx (HTTP)
- `443`: Nginx (HTTPS - à configurer)
- `5432`: PostgreSQL
- `5050`: pgAdmin
- `8000`: API (accès direct, optionnel)

## 🐛 Dépannage

### Les conteneurs ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs

# Vérifier l'état des conteneurs
docker-compose ps

# Nettoyer et redémarrer
docker-compose down -v
docker-compose up --build
```

### Erreurs de connexion à la base de données

```bash
# Vérifier que PostgreSQL est prêt
docker-compose exec postgres pg_isready -U admin

# Recréer la base de données
docker-compose down -v
docker-compose up postgres -d
```

### Problèmes de cache ou de build

```bash
# Reconstruire sans cache
docker-compose build --no-cache

# Nettoyer les images Docker
docker system prune -a
```

## 📝 Notes de développement

- Le mode développement active le hot-reload pour React (Vite) et FastAPI
- Les volumes sont montés pour permettre les modifications en temps réel
- Les migrations de base de données doivent être exécutées manuellement si nécessaire

## 🚀 Production

Pour un déploiement en production, utilisez le Dockerfile de production du frontend :

```bash
# Modifier docker-compose.yml pour utiliser Dockerfile.prod
# Puis construire et démarrer
docker-compose -f docker-compose.prod.yml up -d
```

## 📄 Licence

[Votre licence ici]
