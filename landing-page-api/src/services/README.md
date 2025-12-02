# Services

Ce dossier contient les services métier de l'application.

## AIService

Service d'intelligence artificielle pour la pré-complétion du formulaire d'estimation.

### Responsabilités

- Analyser la description d'un projet client
- Générer des suggestions intelligentes pour :
  - Type de projet
  - Nombre de pages
  - Délai souhaité
  - Budget estimé
- Fournir une explication des suggestions

### Technologies

- **Langchain** : Framework pour applications LLM
- **OpenAI GPT-4o-mini** : Modèle de langage
- **Pydantic** : Validation et parsing des données

### Utilisation

```python
from src.services.ai_service import get_ai_service

# Obtenir l'instance du service
ai_service = get_ai_service()

# Analyser un projet
result = await ai_service.analyze_and_suggest(
    "Je veux créer un site web pour mon restaurant"
)

if result['success']:
    suggestions = result['suggestions']
    print(f"Type: {suggestions['type_projet']}")
    print(f"Pages: {suggestions['nombre_pages']}")
    print(f"Budget: {suggestions['budget']}")
```

### Configuration

Variable d'environnement requise :

```bash
OPENAI_API_KEY=sk-your-key-here
```

### Architecture

```
Client Request
     ↓
ai_suggestions.py (Route)
     ↓
AIService.analyze_and_suggest()
     ↓
Langchain Chain (Prompt → LLM → Parser)
     ↓
EstimationSuggestion (Pydantic Model)
     ↓
JSON Response
```

### Modèle de données

**Input :**

```python
{
    "description_projet": str  # min 20 caractères
}
```

**Output :**

```python
{
    "success": bool,
    "suggestions": {
        "type_projet": str,      # Landing Page | Site Vitrine | E-commerce | Projet Sur Mesure
        "nombre_pages": int,     # >= 1
        "delai_souhaite": str,   # Rapide | Normal | Flexible
        "budget": str            # Moins de 5 000€ | 5 000€ - 10 000€ | ...
    },
    "explication": str           # 2-3 phrases
}
```

### Performance

- **Temps de réponse** : 2-4 secondes
- **Coût** : ~$0.001 par requête
- **Rate limit** : 3,500 requêtes/minute (OpenAI)

### Tests

Exécuter le script de test :

```bash
python test_ai_service.py
```

### Gestion d'erreurs

- Configuration manquante → ValueError
- Description trop courte → success: false avec message
- Erreur API OpenAI → success: false avec message générique

### Évolutions futures

- Cache pour descriptions similaires
- Fine-tuning sur données réelles
- Support multilingue
- Métriques et monitoring
- Retry automatique

### Documentation

- [Guide rapide](../AI_SERVICE_GUIDE.md)
- [Documentation complète](../docs/AI_SERVICE.md)
- [Architecture](../docs/ARCHITECTURE_AI.md)
