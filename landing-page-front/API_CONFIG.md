# Guide de configuration de l'API URL

## 🔧 Configuration selon l'environnement

### En développement avec Docker (recommandé)

Dans le fichier `.env` à la racine du projet :

```bash
# Utilise une URL relative - le reverse proxy (Nginx Proxy Manager) gère le routage
VITE_API_URL=/api
```

### En développement local (sans Docker)

Dans `landing-page-front/.env` :

```bash
# Accès direct à l'API FastAPI
VITE_API_URL=http://localhost:8000
```

### En production

Dans le fichier `.env` à la racine du projet :

```bash
# Pour production avec domaine et HTTPS
VITE_API_URL=/api

# OU avec URL absolue
VITE_API_URL=https://axynis.cloud/api
```

## 🚀 Après modification

**Important** : Les variables `VITE_*` sont injectées au moment du build/démarrage. Après modification :

```bash
# Redémarrer le conteneur frontend
docker-compose restart frontend

# OU reconstruire si nécessaire
docker-compose up -d --build frontend
```

## 🐛 Debug

Pour vérifier quelle URL est utilisée, ouvrez la console du navigateur. Vous verrez :

```
🔗 API_URL: /api - Environment: development
```

## ✅ Configuration recommandée

**Pour Docker (dev et prod)** : Utilisez `/api`

- ✅ Fonctionne avec le reverse proxy
- ✅ Pas besoin de connaître l'IP/domaine
- ✅ Fonctionne en HTTP et HTTPS

**Nginx Proxy Manager doit router** :

- `http(s)://votre-domaine/` → `frontend:3000`
- `http(s)://votre-domaine/api/` → `api:8000`
