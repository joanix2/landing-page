# Structure du Projet

```
landing-page-api/
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── main.py                   # Application FastAPI principale
│   ├── config.py                 # Configuration DB et dépendances
│   ├── database.py               # Base SQLAlchemy
│   │
│   ├── models/                   # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── client.py             # Modèle Client
│   │   ├── rendez_vous.py        # Modèle RendezVous
│   │   └── estimation.py         # Modèle Estimation
│   │
│   ├── schemas/                  # Schémas Pydantic
│   │   ├── __init__.py
│   │   ├── client.py             # Schémas Client
│   │   ├── rendez_vous.py        # Schémas RendezVous
│   │   └── estimation.py         # Schémas Estimation + types
│   │
│   └── routes/                   # Routes de l'API
│       ├── __init__.py
│       ├── clients.py            # Routes /clients
│       ├── rendez_vous.py        # Routes /rendez_vous
│       └── estimations.py        # Routes /estimations
│
├── main.py                       # Point d'entrée (importe src.main)
├── requirements.txt              # Dépendances Python
├── .env.example                  # Template de configuration
├── .gitignore                    # Fichiers à ignorer
└── README.md                     # Documentation
```

## Organisation du Code

### 📁 `src/`

Dossier principal contenant tout le code source.

### 📄 `src/main.py`

Application FastAPI principale avec :

- Configuration CORS
- Inclusion des routers
- Événement de démarrage
- Route racine `/`

### ⚙️ `src/config.py`

- Configuration de la base de données
- Création du moteur SQLAlchemy
- Fonction `get_db()` pour l'injection de dépendances

### 🗄️ `src/database.py`

- Classe de base `Base` pour tous les modèles SQLAlchemy

### 📦 `src/models/`

Modèles SQLAlchemy (tables de la base de données) :

- **client.py** : Table `clients`
- **rendez_vous.py** : Table `rendez_vous`
- **estimation.py** : Table `estimations`

### 📋 `src/schemas/`

Schémas Pydantic pour la validation des données :

- **client.py** : `ClientBase`, `ClientCreate`, `ClientRead`
- **rendez_vous.py** : `RendezVousBase`, `RendezVousCreate`, `RendezVousRead`
- **estimation.py** : `EstimationBase`, `EstimationCreate`, `EstimationRead` + types Literal

### 🛣️ `src/routes/`

Routes de l'API (endpoints) :

- **clients.py** : CRUD complet pour les clients
- **rendez_vous.py** : Création et listing des rendez-vous
- **estimations.py** : CRUD pour les estimations

### 📌 `main.py` (racine)

Point d'entrée qui importe l'application depuis `src.main`.
Permet de lancer l'application avec : `uvicorn main:app --reload`

## Avantages de cette Structure

✅ **Séparation des responsabilités** : Chaque fichier a un rôle précis
✅ **Maintenabilité** : Facile de trouver et modifier du code
✅ **Scalabilité** : Simple d'ajouter de nouveaux modèles/routes
✅ **Testabilité** : Chaque module peut être testé indépendamment
✅ **Lisibilité** : Structure claire et organisée
