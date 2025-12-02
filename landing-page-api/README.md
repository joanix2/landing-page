# 🚀 Landing Page API

API FastAPI moderne pour la gestion d'inscriptions newsletter et estimations de projets web avec suggestions IA intelligentes.

## ✨ Fonctionnalités

- 📧 **Newsletter** : Inscription simple et sécurisée par email
- 📝 **Estimations** : Création d'estimations avec informations clients
- 🤖 **IA Suggestions** : Pré-complétion intelligente via Langchain + OpenAI GPT-4o-mini
- 🗄️ **Cache PostgreSQL** : Économies 50%+ et performances 20-80x plus rapides
- 🔒 **Validation** : Validation robuste avec Pydantic
- 🌐 **CORS** : Support complet pour applications frontend

## 📚 Documentation

Documentation complète disponible dans [`docs/`](./docs/README.md) :

| Document                                      | Description                           |
| --------------------------------------------- | ------------------------------------- |
| [**Installation**](./docs/SETUP.md)           | Guide d'installation et configuration |
| [**Service IA**](./docs/AI_SERVICE.md)        | Documentation du service IA           |
| [**Architecture**](./docs/ARCHITECTURE_AI.md) | Architecture détaillée                |
| [**Cache**](./docs/CACHE_IA.md)               | Système de cache PostgreSQL           |
| [**Structure**](./docs/PROJECT_STRUCTURE.md)  | Organisation du projet                |

## ⚡ Démarrage rapide

### Option 1 : Installation automatique (recommandé)

```bash
# Installation des dépendances
./install.sh

# Configuration (ajouter OPENAI_API_KEY)
nano .env

# Démarrage interactif
./start.sh
```

### Option 2 : Installation manuelle

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer l'environnement
cp .env.example .env
nano .env  # Ajouter OPENAI_API_KEY

# 3. Démarrer PostgreSQL
docker-compose up -d

# 4. Lancer l'API
uvicorn src.main:app --reload
```

### 🌐 Accès à l'API

- **API** : http://localhost:8000
- **Documentation Swagger** : http://localhost:8000/docs
- **Documentation ReDoc** : http://localhost:8000/redoc

## 📋 Prérequis

- Python 3.11+
- PostgreSQL 14+ (ou Docker)
- Clé API OpenAI ([obtenir ici](https://platform.openai.com/api-keys))

## 🌐 Endpoints API

| Méthode | Endpoint       | Description               |
| ------- | -------------- | ------------------------- |
| `POST`  | `/newsletter`  | Inscription newsletter    |
| `POST`  | `/estimations` | Créer estimation + client |
| `POST`  | `/ai/suggest`  | Suggestions IA            |

### 💡 Exemples d'utilisation

**Inscription newsletter**

```bash
curl -X POST http://localhost:8000/newsletter \
  -H "Content-Type: application/json" \
  -d '{"email": "client@example.com"}'
```

**Suggestions IA**

```bash
curl -X POST http://localhost:8000/ai/suggest \
  -H "Content-Type: application/json" \
  -d '{"description_projet": "Site web pour mon restaurant"}'
```

**Création d'estimation**

```bash
curl -X POST http://localhost:8000/estimations \
  -H "Content-Type: application/json" \
  -d '{
    "client": {
      "email": "client@example.com",
      "prenom": "Jean",
      "nom": "Dupont"
    },
    "estimation": {
      "description_projet": "Site vitrine restaurant",
      "type_projet": "Site Vitrine",
      "nombre_pages": 5,
      "delai_souhaite": "Normal",
      "budget": "5 000€ - 10 000€"
    }
  }'
```

## 🛠️ Scripts disponibles

| Script               | Description                              |
| -------------------- | ---------------------------------------- |
| `install.sh`         | Installation automatique des dépendances |
| `start.sh`           | Démarrage interactif de l'application    |
| `test_ai_service.py` | Test du service IA avec exemples         |
| `test_cache.sh`      | Test du système de cache                 |
| `manage_cache.py`    | Gestion et statistiques du cache         |

### Exemples d'utilisation

```bash
# Tester le service IA
python test_ai_service.py

# Voir les statistiques du cache
python manage_cache.py

# Tester le cache
./test_cache.sh
```

## 📊 Performance

| Métrique         | Sans cache | Avec cache | Gain          |
| ---------------- | ---------- | ---------- | ------------- |
| Temps de réponse | 2-4s       | <100ms     | **20-80x** ⚡ |
| Coût par requête | $0.001     | $0         | **100%** 💰   |
| API calls OpenAI | 100%       | 50%        | **50%** 📉    |

## 🏗️ Architecture

```
Frontend
    ↓
FastAPI
    ├─ /newsletter → PostgreSQL
    ├─ /estimations → Client + Estimation → PostgreSQL
    └─ /ai/suggest → Cache ? ✅ : OpenAI GPT-4o-mini → Cache
```

## 🔧 Technologies

| Catégorie            | Technologies                    |
| -------------------- | ------------------------------- |
| **Backend**          | FastAPI, Python 3.11+           |
| **Base de données**  | PostgreSQL + SQLAlchemy (async) |
| **IA**               | Langchain + OpenAI GPT-4o-mini  |
| **Validation**       | Pydantic                        |
| **Cache**            | PostgreSQL                      |
| **Containerisation** | Docker + Docker Compose         |

## 📁 Structure du projet

```
landing-page-api/
├── src/
│   ├── models/          # Modèles SQLAlchemy
│   ├── routes/          # Routes API
│   ├── schemas/         # Schémas Pydantic
│   └── services/        # Services (IA, cache)
├── docs/               # Documentation complète
├── tests/              # Tests
├── install.sh          # Installation auto
├── start.sh            # Démarrage interactif
├── manage_cache.py     # Gestion du cache
└── README.md          # Ce fichier
```

## 🧪 Tests

```bash
# Tester le service IA
python test_ai_service.py

# Tester via l'API
curl http://localhost:8000/docs
```

## 🔐 Sécurité

- ✅ Clé API OpenAI dans `.env` (non versionné)
- ✅ Validation Pydantic des entrées
- ✅ Hash SHA256 pour le cache
- ✅ CORS configuré
- ✅ Pas d'erreurs détaillées exposées

## 📈 Métriques du cache

Avec `manage_cache.py` :

- Nombre d'entrées en cache
- Utilisations totales
- Économies réalisées
- Taux de réutilisation
- Top 10 des suggestions

## 🐛 Dépannage

### Service IA ne fonctionne pas

```bash
# Vérifier la clé API
cat .env | grep OPENAI_API_KEY

# Voir la doc
cat docs/AI_SERVICE.md
```

### Cache ne fonctionne pas

```bash
# Vérifier PostgreSQL
docker ps

# Voir les logs
python manage_cache.py
```

### Erreurs au démarrage

Consultez [docs/SETUP.md](./docs/SETUP.md) section dépannage.

## 📖 En savoir plus

- **Documentation complète** : [docs/](./docs/README.md)
- **Guide d'installation** : [docs/SETUP.md](./docs/SETUP.md)
- **Service IA** : [docs/AI_SERVICE.md](./docs/AI_SERVICE.md)
- **Cache PostgreSQL** : [docs/CACHE_IA.md](./docs/CACHE_IA.md)

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez consulter la documentation avant de contribuer.

## 📝 Licence

MIT

---

**Développé avec ❤️ | Décembre 2025**
