"""Documentation du Service IA."""

# Service IA - Pré-complétion du Formulaire

## Vue d'ensemble

Le service IA utilise **Langchain** et **OpenAI GPT-4o-mini** pour analyser la description d'un projet client et suggérer automatiquement des paramètres appropriés pour l'estimation.

## Fonctionnalités

### Analyse Intelligente

- Analyse sémantique de la description du projet
- Identification du type de projet adapté
- Estimation du nombre de pages nécessaires
- Suggestion du délai approprié
- Recommandation du budget estimé
- Explication détaillée des suggestions

## Configuration

### Variables d'environnement requises

```bash
OPENAI_API_KEY=votre-clé-api-openai
```

### Installation des dépendances

```bash
pip install langchain langchain-openai python-dotenv
```

## Utilisation

### Route API

**POST** `/ai/suggest`

**Corps de la requête :**

```json
{
  "description_projet": "Je veux créer un site web pour mon restaurant avec un menu en ligne, une galerie de photos et un formulaire de réservation. J'aimerais aussi pouvoir mettre à jour le menu facilement."
}
```

**Réponse en cas de succès :**

```json
{
  "success": true,
  "suggestions": {
    "type_projet": "Site Vitrine",
    "nombre_pages": 5,
    "delai_souhaite": "Normal",
    "budget": "5 000€ - 10 000€"
  },
  "explication": "Pour un site de restaurant avec menu dynamique et réservation, un site vitrine de 5 pages est approprié (Accueil, Menu, Galerie, Réservation, Contact). Le délai normal permet une intégration soignée du système de gestion de menu. Le budget prend en compte le CMS pour la mise à jour autonome du contenu."
}
```

**Réponse en cas d'erreur :**

```json
{
  "success": false,
  "message": "La description du projet doit contenir au moins 20 caractères pour obtenir des suggestions pertinentes."
}
```

## Architecture

### Composants

1. **AIService** (`src/services/ai_service.py`)

   - Classe principale pour les opérations IA
   - Gestion du modèle OpenAI
   - Parsing structuré des réponses

2. **EstimationSuggestion**

   - Modèle Pydantic pour la structure des suggestions
   - Validation des données de sortie

3. **Router IA** (`src/routes/ai_suggestions.py`)
   - Endpoint API pour les suggestions
   - Gestion des erreurs
   - Validation des entrées

### Prompt Engineering

Le système utilise un prompt optimisé qui :

- Définit le contexte d'expertise en développement web
- Fournit des guidelines pour chaque type de projet
- Structure la sortie avec Pydantic
- Assure des réponses cohérentes et pertinentes

### Modèle IA

- **Modèle** : GPT-4o-mini
- **Température** : 0.3 (réponses cohérentes et prévisibles)
- **Format de sortie** : JSON structuré via PydanticOutputParser

## Exemples d'utilisation

### Exemple 1 : Landing Page

**Input :**

```
"Je lance un nouveau produit SaaS et j'ai besoin d'une page pour présenter
les fonctionnalités et collecter des emails pour la beta."
```

**Output suggéré :**

- Type : Landing Page
- Pages : 1
- Délai : Rapide
- Budget : Moins de 5 000€

### Exemple 2 : E-commerce

**Input :**

```
"Je veux vendre mes créations artisanales en ligne. J'ai environ 50 produits
à présenter avec un système de paiement sécurisé et gestion des stocks."
```

**Output suggéré :**

- Type : E-commerce
- Pages : 8-10
- Délai : Normal
- Budget : 10 000€ - 20 000€

### Exemple 3 : Projet Sur Mesure

**Input :**

```
"Besoin d'une plateforme de gestion de projets pour mon équipe avec dashboard,
suivi du temps, chat intégré, et API pour nos autres outils."
```

**Output suggéré :**

- Type : Projet Sur Mesure
- Pages : 15+
- Délai : Flexible
- Budget : Plus de 20 000€

## Gestion des erreurs

### Configuration manquante

```python
# Si OPENAI_API_KEY n'est pas définie
HTTP 503 - Service IA non disponible
```

### Description trop courte

```python
# Si description < 20 caractères
{
  "success": false,
  "message": "Description trop courte..."
}
```

### Erreur du modèle

```python
# Si l'API OpenAI échoue
HTTP 500 - Erreur lors de la génération
```

## Performance

- **Temps de réponse moyen** : 2-4 secondes
- **Coût par requête** : ~$0.001 (avec GPT-4o-mini)
- **Rate limiting** : Géré par OpenAI (3,500 RPM par défaut)

## Améliorations futures

- [ ] Cache des suggestions similaires
- [ ] Fine-tuning sur des données de projets réels
- [ ] Support multilingue
- [ ] Analyse des tendances du marché pour les budgets
- [ ] Intégration de feedback utilisateur pour améliorer les suggestions

## Sécurité

- ✅ Clé API stockée dans variables d'environnement
- ✅ Validation des entrées avec Pydantic
- ✅ Gestion des erreurs sans exposer de détails techniques
- ✅ Limite de taille pour les descriptions (protection contre abus)

## Tests

Pour tester le service localement :

```bash
# Avec curl
curl -X POST http://localhost:8000/ai/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "description_projet": "Je veux créer un blog avec système de commentaires"
  }'

# Ou via Swagger UI
# Ouvrir http://localhost:8000/docs
```
