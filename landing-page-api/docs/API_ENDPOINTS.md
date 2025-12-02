# 📡 Documentation des Endpoints API

Documentation complète de l'API Landing Page avec exemples et tests.

## 📋 Table des Matières

- [Vue d'ensemble](#vue-densemble)
- [Base URL](#base-url)
- [Endpoints](#endpoints)
  - [1. Newsletter](#1-newsletter)
  - [2. Estimations](#2-estimations)
  - [3. Suggestions IA](#3-suggestions-ia)
- [Codes de statut HTTP](#codes-de-statut-http)
- [Exemples d'utilisation](#exemples-dutilisation)

---

## 🌐 Vue d'ensemble

L'API Landing Page fournit 3 endpoints principaux :

| Endpoint       | Méthode | Description                     |
| -------------- | ------- | ------------------------------- |
| `/newsletter`  | POST    | Inscription à la newsletter     |
| `/estimations` | POST    | Création d'estimation de projet |
| `/ai/suggest`  | POST    | Suggestions IA pour formulaire  |

**Format des données** : JSON  
**Authentification** : Aucune (API publique)  
**Rate limiting** : Non implémenté

---

## 🔗 Base URL

```
http://localhost:8000
```

**Documentation interactive** :

- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

---

## 📍 Endpoints

### 1. Newsletter

Permet aux visiteurs de s'abonner à la newsletter en fournissant leur email.

#### 📨 `POST /newsletter`

**Description** : Inscription à la newsletter

**Headers**

```http
Content-Type: application/json
```

**Body Parameters**

| Paramètre | Type           | Requis | Description          |
| --------- | -------------- | ------ | -------------------- |
| `email`   | string (email) | ✅ Oui | Adresse email valide |

**Request Body**

```json
{
  "email": "utilisateur@example.com"
}
```

**Réponses**

**✅ Success (200 OK)**

```json
{
  "message": "Merci pour votre inscription !"
}
```

**⚠️ Remarques importantes** :

- Retourne toujours `200 OK` même si l'email existe déjà (anti-bot)
- Les emails sont stockés avec `newsletter=true`
- Validation email automatique (format)

**Exemples**

**cURL**

```bash
curl -X POST http://localhost:8000/newsletter \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

**JavaScript (Fetch)**

```javascript
fetch("http://localhost:8000/newsletter", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    email: "utilisateur@example.com",
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

**Python**

```python
import requests

response = requests.post(
    'http://localhost:8000/newsletter',
    json={'email': 'utilisateur@example.com'}
)
print(response.json())
```

**Cas d'erreur**

**❌ Email invalide (422 Unprocessable Entity)**

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "input": "email-invalide"
    }
  ]
}
```

---

### 2. Estimations

Création d'une demande d'estimation de projet avec informations client et projet.

#### 📝 `POST /estimations`

**Description** : Créer une estimation de projet

**Headers**

```http
Content-Type: application/json
```

**Body Parameters**

| Paramètre                       | Type           | Requis | Description            |
| ------------------------------- | -------------- | ------ | ---------------------- |
| `client`                        | object         | ✅ Oui | Informations du client |
| `client.email`                  | string (email) | ✅ Oui | Email du client        |
| `estimation`                    | object         | ✅ Oui | Détails du projet      |
| `estimation.description_projet` | string         | ✅ Oui | Description du projet  |
| `estimation.type_projet`        | string         | ✅ Oui | Type de projet         |
| `estimation.nombre_pages`       | integer        | ✅ Oui | Nombre de pages        |
| `estimation.delai_souhaite`     | string         | ✅ Oui | Délai souhaité         |
| `estimation.budget`             | string         | ✅ Oui | Budget estimé          |

**Types de projet disponibles** :

- `"Landing Page"`
- `"Site Vitrine"`
- `"E-commerce"`
- `"Projet Sur Mesure"`

**Délais disponibles** :

- `"Rapide"`
- `"Normal"`
- `"Flexible"`

**Budgets disponibles** :

- `"Moins de 5 000€"`
- `"5 000€ - 10 000€"`
- `"10 000€ - 20 000€"`
- `"Plus de 20 000€"`

**Request Body**

```json
{
  "client": {
    "email": "client@example.com"
  },
  "estimation": {
    "description_projet": "Site e-commerce avec panier et paiement en ligne",
    "type_projet": "E-commerce",
    "nombre_pages": 15,
    "delai_souhaite": "Normal",
    "budget": "5 000€ - 10 000€"
  }
}
```

**Réponses**

**✅ Success (201 Created)**

```json
{
  "id": 1,
  "client_id": 1,
  "description_projet": "Site e-commerce avec panier et paiement en ligne",
  "type_projet": "E-commerce",
  "nombre_pages": 15,
  "delai_souhaite": "Normal",
  "budget": "5 000€ - 10 000€",
  "created_at": "2025-12-01T20:30:00.000Z"
}
```

**Comportement** :

- Si l'email existe : associe l'estimation au client existant
- Si l'email n'existe pas : crée le client puis l'estimation
- Retourne l'estimation créée avec son ID

**Exemples**

**cURL**

```bash
curl -X POST http://localhost:8000/estimations \
  -H "Content-Type: application/json" \
  -d '{
    "client": {
      "email": "client@example.com"
    },
    "estimation": {
      "description_projet": "Site vitrine moderne pour mon restaurant",
      "type_projet": "Site Vitrine",
      "nombre_pages": 5,
      "delai_souhaite": "Normal",
      "budget": "Moins de 5 000€"
    }
  }'
```

**JavaScript (Fetch)**

```javascript
fetch("http://localhost:8000/estimations", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    client: {
      email: "client@example.com",
    },
    estimation: {
      description_projet: "Site vitrine moderne pour mon restaurant",
      type_projet: "Site Vitrine",
      nombre_pages: 5,
      delai_souhaite: "Normal",
      budget: "Moins de 5 000€",
    },
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

**Python**

```python
import requests

response = requests.post(
    'http://localhost:8000/estimations',
    json={
        'client': {
            'email': 'client@example.com'
        },
        'estimation': {
            'description_projet': 'Site vitrine moderne pour mon restaurant',
            'type_projet': 'Site Vitrine',
            'nombre_pages': 5,
            'delai_souhaite': 'Normal',
            'budget': 'Moins de 5 000€'
        }
    }
)
print(response.json())
```

**Cas d'erreur**

**❌ Données manquantes (422 Unprocessable Entity)**

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "estimation", "description_projet"],
      "msg": "Field required",
      "input": {...}
    }
  ]
}
```

---

### 3. Suggestions IA

Génère des suggestions de paramètres de projet basées sur une description textuelle.

#### 🤖 `POST /ai/suggest`

**Description** : Obtenir des suggestions IA pour pré-remplir le formulaire

**Headers**

```http
Content-Type: application/json
```

**Body Parameters**

| Paramètre            | Type   | Requis | Description                     |
| -------------------- | ------ | ------ | ------------------------------- |
| `description_projet` | string | ✅ Oui | Description textuelle du projet |

**Request Body**

```json
{
  "description_projet": "Je veux un site vitrine moderne pour mon restaurant avec menu et réservation en ligne"
}
```

**Réponses**

**✅ Success (200 OK)**

```json
{
  "type_projet": "Site Vitrine",
  "nombre_pages": 8,
  "delai_souhaite": "Normal",
  "budget": "Moins de 5 000€",
  "explication": "Pour un site vitrine de restaurant avec menu et système de réservation, je recommande 8 pages (accueil, menu, réservation, galerie, contact, etc.). Un délai normal est approprié pour intégrer un système de réservation. Le budget de moins de 5 000€ convient pour un site professionnel avec fonctionnalités personnalisées.",
  "from_cache": false,
  "processing_time": 2.34
}
```

**Champs de réponse** :

| Champ             | Type    | Description                     |
| ----------------- | ------- | ------------------------------- |
| `type_projet`     | string  | Type de projet suggéré          |
| `nombre_pages`    | integer | Nombre de pages recommandé      |
| `delai_souhaite`  | string  | Délai suggéré                   |
| `budget`          | string  | Fourchette budgétaire           |
| `explication`     | string  | Justification des suggestions   |
| `from_cache`      | boolean | `true` si résultat mis en cache |
| `processing_time` | float   | Temps de traitement (secondes)  |

**⚡ Performance** :

- **Sans cache** : ~2-4 secondes (appel OpenAI)
- **Avec cache** : <100ms (PostgreSQL)
- Le cache est basé sur un hash SHA256 de la description
- 50%+ de réduction des coûts API avec le cache

**Exemples**

**cURL**

```bash
curl -X POST http://localhost:8000/ai/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "description_projet": "Application web pour gérer mes stocks de boutique"
  }'
```

**JavaScript (Fetch)**

```javascript
fetch("http://localhost:8000/ai/suggest", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    description_projet: "Application web pour gérer mes stocks de boutique",
  }),
})
  .then((response) => response.json())
  .then((data) => {
    console.log("Suggestions:", data);
    console.log("From cache:", data.from_cache);
  });
```

**Python**

```python
import requests

response = requests.post(
    'http://localhost:8000/ai/suggest',
    json={
        'description_projet': 'Application web pour gérer mes stocks de boutique'
    }
)
suggestions = response.json()
print(f"Type: {suggestions['type_projet']}")
print(f"Pages: {suggestions['nombre_pages']}")
print(f"Cache: {suggestions['from_cache']}")
```

**Cas d'erreur**

**❌ Description vide (422 Unprocessable Entity)**

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "description_projet"],
      "msg": "String should have at least 10 characters",
      "input": "court"
    }
  ]
}
```

**❌ Erreur OpenAI (500 Internal Server Error)**

```json
{
  "detail": "Erreur lors de la génération des suggestions"
}
```

---

## 📊 Codes de statut HTTP

| Code  | Signification         | Utilisation                                        |
| ----- | --------------------- | -------------------------------------------------- |
| `200` | OK                    | Requête réussie (GET, POST newsletter, AI suggest) |
| `201` | Created               | Ressource créée (POST estimations)                 |
| `422` | Unprocessable Entity  | Validation des données échouée                     |
| `500` | Internal Server Error | Erreur serveur (DB, OpenAI, etc.)                  |

---

## 🚀 Exemples d'utilisation

### Scénario complet : Formulaire de contact

```javascript
// 1. Utilisateur tape sa description
const description = document.getElementById("description").value;

// 2. Obtenir des suggestions IA
const suggestions = await fetch("http://localhost:8000/ai/suggest", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ description_projet: description }),
}).then((r) => r.json());

// 3. Pré-remplir le formulaire
document.getElementById("type_projet").value = suggestions.type_projet;
document.getElementById("nombre_pages").value = suggestions.nombre_pages;
document.getElementById("delai").value = suggestions.delai_souhaite;
document.getElementById("budget").value = suggestions.budget;

// 4. Utilisateur soumet le formulaire
const email = document.getElementById("email").value;
const estimation = await fetch("http://localhost:8000/estimations", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    client: { email },
    estimation: {
      description_projet: description,
      type_projet: suggestions.type_projet,
      nombre_pages: suggestions.nombre_pages,
      delai_souhaite: suggestions.delai_souhaite,
      budget: suggestions.budget,
    },
  }),
}).then((r) => r.json());

console.log("Estimation créée:", estimation);
```

### Script de test complet

Un script bash `test_api.sh` est disponible à la racine du projet :

```bash
#!/bin/bash
./test_api.sh
```

Ce script teste automatiquement les 3 endpoints avec des données d'exemple.

---

## 🔧 Gestion et Maintenance

### Cache IA

Pour gérer le cache PostgreSQL :

```bash
# Afficher les statistiques
python manage_cache.py

# Voir toutes les entrées
python manage_cache.py

# Supprimer les entrées anciennes (>30 jours)
python manage_cache.py

# Vider tout le cache
python manage_cache.py
```

### Logs

Les logs SQL sont activés par défaut (voir console uvicorn).

Pour désactiver :

```python
# src/config.py
engine = create_async_engine(DATABASE_URL, echo=False)  # Mettre False
```

---

## 📝 Notes importantes

### Sécurité

- ✅ Validation des emails (format)
- ✅ Protection anti-bot (toujours retour 200 pour newsletter)
- ⚠️ Pas d'authentification (API publique)
- ⚠️ Pas de rate limiting
- ⚠️ Pas de CAPTCHA

### Performance

- Cache IA : ~50% de réduction des coûts OpenAI
- Base de données : PostgreSQL avec indexes optimisés
- Async/await : Gestion asynchrone complète

### Limites

- Descriptions IA : minimum 10 caractères
- Emails : format standard (validation Pydantic)
- Pas de limite de taux pour l'instant

---

## 🔗 Liens utiles

- [Documentation complète](../README.md)
- [Configuration et Installation](./SETUP.md)
- [Service IA](./AI_SERVICE.md)
- [Architecture IA](./ARCHITECTURE_AI.md)
- [Cache PostgreSQL](./CACHE_IA.md)

---

**Version** : 1.0.0  
**Dernière mise à jour** : 1 décembre 2025  
**API Framework** : FastAPI 0.109.0
