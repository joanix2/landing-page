# Service AI

Service d'intelligence artificielle pour générer des suggestions d'estimation de projet web basées sur une description utilisateur.

## Structure

```
ai_service/
├── __init__.py           # Export du service
├── ai_service.py         # Classe principale AIService
└── templates/            # Templates Jinja2 pour les prompts IA
    ├── system_prompt.txt.j2
    └── user_prompt.txt.j2
```

## Utilisation

```python
from src.services import AIService

# Initialiser le service
ai_service = AIService()

# Obtenir des suggestions
suggestion = await ai_service.suggest_estimation_params(
    description="Je veux un site e-commerce pour vendre mes produits artisanaux",
    db=db_session
)

# Résultat
print(suggestion.type_projet)    # "E-commerce"
print(suggestion.liste_pages)    # ["Accueil", "Boutique", "Panier", ...]
print(suggestion.explication)    # "Un site e-commerce adapté..."
```

## Configuration requise

### Variables d'environnement

- `OPENAI_API_KEY` : Clé API OpenAI (obligatoire)

### Dépendances

- `langchain-openai>=0.0.2`
- `langchain>=0.1.0`
- `jinja2>=3.1.2`
- `pydantic>=2.0.0`

## Templates

Les templates Jinja2 définissent les prompts envoyés à l'IA :

- **system_prompt.txt.j2** : Instructions système pour l'IA
- **user_prompt.txt.j2** : Template du prompt utilisateur avec la description du projet

Variables disponibles dans les templates :

- `{{ description }}` : Description du projet fournie par l'utilisateur
- `{{ format_instructions }}` : Instructions de formatage pour la réponse structurée

## Cache

Le service utilise un système de cache (table `ai_cache`) pour éviter de faire des appels API redondants :

- Durée de validité : 30 jours
- Clé de cache : Hash MD5 de la description
