# Guide d'Installation et de Démarrage

## Option 1 : Avec Docker (Recommandé)

### 1. Installer Docker
Si Docker n'est pas installé :
```bash
# Sur Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER  # Puis se déconnecter/reconnecter
```

### 2. Démarrer PostgreSQL avec Docker
```bash
docker-compose up -d
```

Vérifier que PostgreSQL fonctionne :
```bash
docker ps
```

### 3. Installer les dépendances Python
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Lancer l'application
```bash
uvicorn main:app --reload
```

### 5. Arrêter PostgreSQL
```bash
docker-compose down
```

Pour supprimer les données :
```bash
docker-compose down -v
```

---

## Option 2 : PostgreSQL installé localement

### 1. Installer PostgreSQL
```bash
# Sur Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### 2. Configurer la base de données
```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Dans psql :
CREATE USER user WITH PASSWORD 'password';
CREATE DATABASE studio_web OWNER user;
GRANT ALL PRIVILEGES ON DATABASE studio_web TO user;
\q
```

### 3. Installer les dépendances Python
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Lancer l'application
```bash
uvicorn main:app --reload
```

---

## Option 3 : Mode développement sans base de données

Si vous voulez juste tester l'API sans PostgreSQL :

```bash
# L'application démarrera avec un avertissement mais fonctionnera
source venv/bin/activate
uvicorn main:app --reload
```

⚠️ **Note** : Les routes qui accèdent à la base de données retourneront des erreurs.

---

## Accéder à l'API

Une fois l'application lancée :

- **API** : http://localhost:8000
- **Documentation Swagger** : http://localhost:8000/docs
- **Documentation ReDoc** : http://localhost:8000/redoc

---

## Configuration personnalisée

Pour modifier la configuration de la base de données, éditez `src/config.py` :

```python
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/studio_web"
```

Ou créez un fichier `.env` :
```env
DATABASE_URL=postgresql+asyncpg://votre_user:votre_password@localhost:5432/votre_db
```

---

## Commandes utiles

### Activer l'environnement virtuel
```bash
source venv/bin/activate
```

### Désactiver l'environnement virtuel
```bash
deactivate
```

### Installer une nouvelle dépendance
```bash
pip install nom_du_package
pip freeze > requirements.txt
```

### Voir les logs Docker
```bash
docker-compose logs -f
```

### Redémarrer l'application
```bash
# Ctrl+C pour arrêter uvicorn
uvicorn main:app --reload
```
