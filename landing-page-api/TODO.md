✅ Service IA avec Langchain pour la pré complétion du formulaire

- Service créé dans src/services/ai_service.py
- Route API : POST /ai/suggest
- Documentation : docs/AI_SERVICE.md et AI_SERVICE_GUIDE.md
- Script de test : test_ai_service.py
- Utilise GPT-4o-mini via Langchain + OpenAI
- ✅ Prompts dans fichier séparé (src/services/prompts.py)
- ✅ Cache PostgreSQL intégré (src/models/ai_cache.py)
- ✅ Script de gestion du cache (manage_cache.py)
- Documentation cache : docs/CACHE_IA.md

⏳ Envoie d'estimation par mail
⏳ Validation de l'abonnement à la news letter par mail
