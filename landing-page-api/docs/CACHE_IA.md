# 🗄️ Cache PostgreSQL pour les Suggestions IA

## Vue d'ensemble

Le système de cache PostgreSQL permet de :

- ✅ **Éviter les appels répétés** à l'API OpenAI
- ✅ **Réduire les coûts** (~$0.001 économisé par réutilisation)
- ✅ **Accélérer les réponses** (cache instantané vs 2-4s IA)
- ✅ **Tracker l'utilisation** (statistiques et métriques)

## Architecture

```
Description du projet
        ↓
Hash SHA256 (clé de cache)
        ↓
Recherche dans PostgreSQL
        ↓
    Trouvé ?
   /        \
 OUI        NON
  ↓          ↓
Retour    Appel IA
cache      ↓
  ↑     Sauvegarde
  ↑        ↓
  └────────┘
```

## Structure de la table

### `ai_suggestion_cache`

| Colonne              | Type       | Description              |
| -------------------- | ---------- | ------------------------ |
| `id`                 | Integer    | Clé primaire             |
| `description_hash`   | String(64) | Hash SHA256 (clé unique) |
| `description_projet` | Text       | Description originale    |
| `type_projet`        | String(50) | Type suggéré             |
| `nombre_pages`       | Integer    | Nombre de pages          |
| `delai_souhaite`     | String(50) | Délai suggéré            |
| `budget`             | String(50) | Budget suggéré           |
| `explication`        | Text       | Explication détaillée    |
| `created_at`         | DateTime   | Date de création         |
| `used_count`         | Integer    | Nombre d'utilisations    |
| `last_used_at`       | DateTime   | Dernière utilisation     |

**Index :**

- `description_hash` (unique)
- `created_at`
- `last_used_at`

## Fonctionnement

### 1. Hash de la description

```python
import hashlib

def hash_description(description: str) -> str:
    normalized = description.lower().strip()
    return hashlib.sha256(normalized.encode()).hexdigest()
```

Les descriptions similaires (majuscules/minuscules, espaces) produisent le même hash.

### 2. Recherche dans le cache

Avant chaque appel IA :

1. Générer le hash de la description
2. Rechercher dans `ai_suggestion_cache`
3. Si trouvé :
   - Incrémenter `used_count`
   - Mettre à jour `last_used_at`
   - Retourner les suggestions
4. Si non trouvé :
   - Appeler l'IA
   - Sauvegarder dans le cache
   - Retourner les suggestions

### 3. Statistiques

Le système track :

- Nombre d'entrées en cache
- Nombre d'utilisations par entrée
- Économies réalisées
- Taux de réutilisation

## Utilisation

### Via l'API

L'utilisation du cache est automatique et transparente :

```bash
curl -X POST http://localhost:8000/ai/suggest \
  -H "Content-Type: application/json" \
  -d '{"description_projet": "Site web pour mon restaurant"}'
```

**Réponse avec indicateur de cache :**

```json
{
  "success": true,
  "suggestions": {...},
  "explication": "...",
  "from_cache": true  // Indique si provient du cache
}
```

### Script de gestion

```bash
python manage_cache.py
```

**Options disponibles :**

1. **Afficher les statistiques**

   - Nombre d'entrées
   - Utilisations totales
   - Économies estimées
   - Taux de réutilisation

2. **Voir les entrées les plus utilisées**

   - Top 10 des suggestions
   - Détails de chaque entrée

3. **Supprimer les entrées anciennes**

   - Par défaut : 30 jours
   - Personnalisable

4. **Vider complètement le cache**
   - Supprime toutes les entrées

## Exemples

### Première utilisation (miss)

```
🤖 Génération de nouvelles suggestions via IA...
💾 Suggestion sauvegardée dans le cache
```

Temps : **~3 secondes**
Coût : **$0.001**

### Utilisation suivante (hit)

```
✅ Suggestion trouvée dans le cache (utilisée 2 fois)
```

Temps : **<100ms**
Coût : **$0**

### Statistiques

```
📊 STATISTIQUES DU CACHE IA
============================================================
Entrées dans le cache    : 15
Utilisations totales     : 47
Économies estimées       : $0.032
Taux de réutilisation    : 213.3%
============================================================
```

## Configuration

### Variables d'environnement

Le cache utilise la même connexion PostgreSQL que l'application :

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/studio_web
```

### Création automatique

La table est créée automatiquement au démarrage de l'application via SQLAlchemy.

## Performance

### Temps de réponse

| Source      | Temps moyen |
| ----------- | ----------- |
| Cache       | 50-100ms    |
| IA (OpenAI) | 2-4s        |

**Amélioration : 20-80x plus rapide !**

### Économies

Exemple avec 100 requêtes :

- Sans cache : 100 appels IA = $0.10
- Avec cache (50% hit) : 50 appels IA = $0.05
- **Économie : 50%**

## Maintenance

### Nettoyage automatique

Vous pouvez configurer un CRON pour nettoyer régulièrement :

```bash
# Tous les jours à 3h du matin
0 3 * * * cd /path/to/api && python manage_cache.py --clean-old 30
```

### Monitoring

Tables à surveiller :

- Taille de la table `ai_suggestion_cache`
- Taux de hit/miss
- Utilisation par entrée

### Limites

**Taille recommandée :**

- < 10 000 entrées : Excellent
- 10 000 - 50 000 : Bon
- > 50 000 : Considérer un nettoyage

## Sécurité

### Hash SHA256

- ✅ Descriptions normalisées avant hash
- ✅ Impossible de retrouver la description depuis le hash
- ✅ Pas de collision (pratiquement)

### Données sensibles

Les descriptions sont stockées en clair pour :

- Debugging
- Analyse
- Amélioration du service

**⚠️ Ne pas utiliser pour des données ultra-sensibles**

## Amélioration futures

- [ ] Expiration automatique (TTL)
- [ ] Cache distribué (Redis)
- [ ] Compression des descriptions longues
- [ ] Analyse de similarité sémantique
- [ ] Métriques Prometheus

## Tests

### Tester le cache

```python
# Premier appel (miss)
result1 = await ai_service.analyze_and_suggest(description, db)
# from_cache = False

# Deuxième appel (hit)
result2 = await ai_service.analyze_and_suggest(description, db)
# from_cache = True
```

### Vérifier la base de données

```sql
-- Nombre d'entrées
SELECT COUNT(*) FROM ai_suggestion_cache;

-- Entrées les plus utilisées
SELECT description_projet, used_count, created_at
FROM ai_suggestion_cache
ORDER BY used_count DESC
LIMIT 10;

-- Économies estimées
SELECT
  COUNT(*) as entries,
  SUM(used_count) as total_uses,
  (SUM(used_count) - COUNT(*)) * 0.001 as savings
FROM ai_suggestion_cache;
```

## Fichiers

```
src/
├── models/
│   └── ai_cache.py           ← Modèle SQLAlchemy
├── services/
│   ├── ai_service.py         ← Logique de cache
│   └── prompts.py            ← Prompts séparés
└── routes/
    └── ai_suggestions.py     ← Route API

manage_cache.py               ← Script de gestion
docs/
└── CACHE_IA.md              ← Cette documentation
```

## Support

Pour des questions ou problèmes :

1. Consulter les logs de l'application
2. Vérifier les statistiques : `python manage_cache.py`
3. Examiner la table dans PostgreSQL
4. Vider le cache en cas de problème

---

**Le cache améliore significativement les performances et réduit les coûts ! 🚀**
