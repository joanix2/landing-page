"""
Architecture du Service IA - Landing Page API
=============================================

┌─────────────────────────────────────────────────────────────────┐
│ CLIENT (Frontend) │
└────────────────────────┬────────────────────────────────────────┘
│
│ 1. User entre description
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ POST /ai/suggest │
│ (src/routes/ai_suggestions.py) │
└────────────────────────┬────────────────────────────────────────┘
│
│ 2. Validation (min 20 chars)
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ AIService.analyze_and_suggest() │
│ (src/services/ai_service.py) │
└────────────────────────┬────────────────────────────────────────┘
│
│ 3. Création du prompt
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ Langchain Chain │
│ Prompt Template → LLM (GPT-4o-mini) → Pydantic Parser │
└────────────────────────┬────────────────────────────────────────┘
│
│ 4. Réponse structurée
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ EstimationSuggestion │
│ { │
│ type_projet: "Site Vitrine", │
│ nombre_pages: 5, │
│ delai_souhaite: "Normal", │
│ budget: "5 000€ - 10 000€", │
│ explication: "..." │
│ } │
└────────────────────────┬────────────────────────────────────────┘
│
│ 5. Retour JSON formaté
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ CLIENT (Frontend) │
│ • Pré-remplit le formulaire │
│ • Affiche l'explication │
│ • User valide/modifie │
└────────────────────────┬────────────────────────────────────────┘
│
│ 6. Soumission finale
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ POST /estimations │
│ • Crée/met à jour le client │
│ • Crée l'estimation │
│ • Sauvegarde en DB │
└─────────────────────────────────────────────────────────────────┘

# Flux de données détaillé

1. INPUT (Frontend → API)
   {
   "description_projet": "Site web pour mon restaurant avec menu"
   }

2. PROCESSING (AIService)

   - Validation longueur
   - Construction du prompt avec contexte expert
   - Appel OpenAI API
   - Parsing de la réponse en structure Pydantic

3. AI RESPONSE (OpenAI → Langchain)
   {
   "type_projet": "Site Vitrine",
   "nombre_pages": 5,
   "delai_souhaite": "Normal",
   "budget": "5 000€ - 10 000€",
   "explication": "Pour un site de restaurant..."
   }

4. OUTPUT (API → Frontend)
   {
   "success": true,
   "suggestions": {...},
   "explication": "..."
   }

5. FORM PRE-FILL (Frontend)
   - Les champs sont automatiquement remplis
   - L'utilisateur peut modifier
   - Soumission vers POST /estimations

# Structure des fichiers

landing-page-api/
├── src/
│ ├── services/
│ │ ├── **init**.py
│ │ └── ai_service.py ← 🤖 Service IA principal
│ ├── routes/
│ │ ├── **init**.py
│ │ ├── clients.py ← Newsletter
│ │ ├── estimations.py ← Estimations
│ │ └── ai_suggestions.py ← 🆕 Route IA
│ ├── models/
│ │ ├── client.py
│ │ └── estimation.py
│ └── schemas/
│ ├── client.py
│ └── estimation.py
├── docs/
│ ├── AI_SERVICE.md ← 📚 Doc complète
│ └── SETUP.md
├── test_ai_service.py ← 🧪 Tests
├── AI_SERVICE_GUIDE.md ← 📖 Guide rapide
├── requirements.txt ← Dépendances (avec langchain)
├── .env ← 🔑 Clé API OpenAI
├── .env.example
└── README.md

# Configuration requise

Variables d'environnement (.env):
DATABASE_URL=postgresql+asyncpg://...
OPENAI_API_KEY=sk-...

Dépendances Python:

- fastapi
- langchain
- langchain-openai
- python-dotenv
- pydantic
- sqlalchemy
- asyncpg

# Endpoints disponibles

POST /newsletter
→ Inscription email

POST /estimations
→ Créer estimation + client

POST /ai/suggest 🆕
→ Obtenir suggestions IA

# Modèle IA

Fournisseur : OpenAI
Modèle : gpt-4o-mini
Température : 0.3 (cohérence)
Coût : ~$0.001/requête
Latence : 2-4 secondes

# Sécurité

✅ Clé API dans .env (non versionné)
✅ Validation Pydantic des entrées
✅ Gestion d'erreurs sans exposition technique
✅ Limite de caractères sur la description

# Performance

Cache : Non implémenté (TODO)
Rate Limit : Géré par OpenAI
Retry : Non implémenté (TODO)
Timeout : Défaut OpenAI (60s)

# Métriques à surveiller

- Temps de réponse IA
- Taux d'erreur API OpenAI
- Coût mensuel OpenAI
- Taux d'utilisation des suggestions
- Taux de modification des suggestions

# Améliorations futures

1. Cache Redis pour descriptions similaires
2. Retry automatique en cas d'erreur
3. Fine-tuning sur projets réels
4. Analyse de sentiment
5. Support multilingue
6. Métriques Prometheus
7. AB Testing des prompts
8. Feedback loop utilisateur
   """
