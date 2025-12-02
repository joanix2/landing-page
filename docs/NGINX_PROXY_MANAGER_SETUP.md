# Nginx Proxy Manager - Configuration Guide

## 🚀 Accès à Nginx Proxy Manager

Après avoir démarré les conteneurs avec `docker-compose up -d`, accédez à l'interface d'administration :

**URL**: http://localhost:81

### Identifiants par défaut (première connexion)

- **Email**: `admin@example.com`
- **Mot de passe**: `changeme`

⚠️ **Vous serez invité à changer ces identifiants lors de la première connexion.**

## 📝 Configuration des Proxy Hosts

### 1. Configuration pour le Frontend React

1. Allez dans **Hosts** > **Proxy Hosts**
2. Cliquez sur **Add Proxy Host**
3. Remplissez les informations :
   - **Domain Names**: `localhost` (ou votre domaine)
   - **Scheme**: `http`
   - **Forward Hostname / IP**: `frontend`
   - **Forward Port**: `5173`
   - ✅ Cochez **Cache Assets**
   - ✅ Cochez **Block Common Exploits**
   - ✅ Cochez **Websockets Support** (pour le HMR de Vite)

### 2. Configuration pour l'API FastAPI

1. Cliquez sur **Add Proxy Host**
2. Remplissez les informations :

   - **Domain Names**: `localhost` (ou votre domaine)
   - **Scheme**: `http`
   - **Forward Hostname / IP**: `api`
   - **Forward Port**: `8000`
   - Dans l'onglet **Advanced**, ajoutez dans **Custom Nginx Configuration** :

   ```nginx
   location /api/ {
       proxy_pass http://api:8000/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }

   location /docs {
       proxy_pass http://api:8000/docs;
       proxy_set_header Host $host;
   }

   location /openapi.json {
       proxy_pass http://api:8000/openapi.json;
       proxy_set_header Host $host;
   }
   ```

### 3. Configuration SSL/HTTPS (optionnel)

Pour activer HTTPS avec Let's Encrypt :

1. Dans l'onglet **SSL** de votre Proxy Host
2. Sélectionnez **Request a new SSL Certificate**
3. ✅ Cochez **Force SSL**
4. ✅ Cochez **HTTP/2 Support**
5. Entrez votre email
6. ✅ Acceptez les conditions

## 🔧 Configuration alternative simple

Si vous voulez une configuration rapide sans passer par l'interface :

### Option 1 : Utiliser Custom Locations

1. Créez un Proxy Host pour `localhost`
2. Forward vers `frontend:5173`
3. Dans l'onglet **Custom Locations**, ajoutez :

   **Location**: `/api/`

   - **Scheme**: `http`
   - **Forward Hostname / IP**: `api`
   - **Forward Port**: `8000`
   - **Advanced** :

   ```nginx
   proxy_pass http://api:8000/;
   ```

## 🌐 Accès aux services après configuration

- **Application Frontend**: http://localhost
- **API Backend**: http://localhost/api
- **Documentation API**: http://localhost/docs
- **pgAdmin**: http://localhost:5050
- **Nginx Proxy Manager**: http://localhost:81

## 📊 Avantages de Nginx Proxy Manager

✅ Interface graphique intuitive  
✅ Gestion des certificats SSL Let's Encrypt automatique  
✅ Configuration des proxy hosts sans fichiers de config  
✅ Logs et statistiques en temps réel  
✅ Support WebSocket (important pour Vite HMR)  
✅ Gestion des redirections  
✅ Protection contre les exploits courants

## 🔐 Sécurité

Après la première connexion, pensez à :

1. Changer le mot de passe par défaut
2. Créer des utilisateurs supplémentaires si nécessaire
3. Configurer les Access Lists pour restreindre l'accès
4. Activer SSL pour tous les hosts en production

## 🐛 Dépannage

### Le port 80 est déjà utilisé

Si vous avez une erreur de port déjà utilisé, modifiez dans `docker-compose.yaml` :

```yaml
ports:
  - "8080:80" # Au lieu de "80:80"
  - "8443:443" # Au lieu de "443:443"
  - "81:81" # Interface admin (inchangé)
```

### Les services ne sont pas accessibles

Vérifiez que tous les conteneurs sont sur le même réseau `app-network` :

```bash
docker network inspect marketing-bot_app-network
```

### Réinitialiser la configuration

Pour repartir de zéro :

```bash
docker-compose down -v
docker-compose up -d
```
