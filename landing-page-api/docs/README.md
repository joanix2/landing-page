# 📚 Documentation - Landing Page API

Bienvenue dans la documentation du projet Landing Page API.

## 📋 Table des matières

### 🚀 Démarrage rapide

1. **[SETUP.md](./SETUP.md)** - Guide d'installation et de configuration
   - Installation avec Docker
   - Installation locale
   - Configuration de l'environnement

### 📡 API

2. **[API_ENDPOINTS.md](./API_ENDPOINTS.md)** - Documentation complète des endpoints
   - `/newsletter` - Inscription newsletter
   - `/estimations` - Création d'estimations
   - `/ai/suggest` - Suggestions IA
   - Exemples curl, JavaScript, Python
   - Codes de statut HTTP

### 🤖 Service IA

3. **[AI_SERVICE.md](./AI_SERVICE.md)** - Documentation complète du service IA

   - Vue d'ensemble
   - Configuration
   - Utilisation
   - Exemples
   - API Reference

4. **[ARCHITECTURE_AI.md](./ARCHITECTURE_AI.md)** - Architecture détaillée du service IA
   - Flux de données
   - Diagrammes
   - Structure des composants
   - Modèle IA utilisé

### 🗄️ Cache PostgreSQL

5. **[CACHE_IA.md](./CACHE_IA.md)** - Système de cache PostgreSQL
   - Fonctionnement du cache
   - Structure de la table
   - Gestion et maintenance
   - Statistiques et performances
   - Script de gestion

### 📁 Structure du projet

6. **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** - Organisation des fichiers
   - Arborescence du projet
   - Description des dossiers
   - Conventions

## 🎯 Par cas d'usage

### Je veux installer le projet

→ [SETUP.md](./SETUP.md)

### Je veux utiliser l'API

→ [API_ENDPOINTS.md](./API_ENDPOINTS.md)

### Je veux comprendre le service IA

→ [AI_SERVICE.md](./AI_SERVICE.md)

### Je veux voir l'architecture

→ [ARCHITECTURE_AI.md](./ARCHITECTURE_AI.md)

### Je veux gérer le cache

→ [CACHE_IA.md](./CACHE_IA.md)

### Je veux voir la structure

→ [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)

## 🔧 Outils et scripts

### Scripts disponibles à la racine

- `install.sh` - Installation automatique des dépendances
- `start.sh` - Démarrage interactif de l'application
- `test_api.sh` - Test complet des endpoints API
- `test_ai_service.py` - Test du service IA
- `test_cache.sh` - Test du système de cache
- `manage_cache.py` - Gestion du cache PostgreSQL

## 📊 Métriques et monitoring

### Service IA

- Temps de réponse : 2-4 secondes (sans cache)
- Coût par requête : ~$0.001
- Modèle : GPT-4o-mini

### Cache PostgreSQL

- Temps de réponse : <100ms (avec cache)
- Économies : 50%+ sur les coûts
- Amélioration : 20-80x plus rapide

## 🆘 Support et dépannage

### Problèmes courants

**Service IA ne fonctionne pas**

- Vérifier `OPENAI_API_KEY` dans `.env`
- Voir [AI_SERVICE.md](./AI_SERVICE.md) section "Gestion des erreurs"

**Cache ne fonctionne pas**

- Vérifier la connexion PostgreSQL
- Voir [CACHE_IA.md](./CACHE_IA.md) section "Dépannage"

**Erreurs de démarrage**

- Voir [SETUP.md](./SETUP.md) section "Dépannage"

## 🔄 Mise à jour de la documentation

Cette documentation est maintenue dans le dossier `docs/`.

Pour contribuer :

1. Modifier les fichiers concernés
2. Mettre à jour ce README si nécessaire
3. Tester les exemples de code

## 📝 Fichiers importants

```
docs/
├── README.md              ← Ce fichier
├── SETUP.md              ← Installation
├── AI_SERVICE.md         ← Service IA
├── ARCHITECTURE_AI.md    ← Architecture
├── CACHE_IA.md          ← Cache PostgreSQL
└── PROJECT_STRUCTURE.md  ← Structure du projet
```

## 🌟 Liens utiles

- **API Swagger** : http://localhost:8000/docs
- **API ReDoc** : http://localhost:8000/redoc
- **OpenAI Platform** : https://platform.openai.com
- **FastAPI Docs** : https://fastapi.tiangolo.com

---

**Dernière mise à jour** : Décembre 2025
