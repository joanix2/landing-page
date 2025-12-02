# Services API - Documentation d'intégration

## ✅ Modifications effectuées

### 1. Création du service API (`src/services/api.js`)

Trois fonctions principales ont été créées :

- **`subscribeNewsletter(email)`** - Abonnement à la newsletter
- **`createEstimation(data)`** - Création d'une estimation/devis
- **`getAISuggestions(description)`** - Obtenir des suggestions IA

### 2. Configuration de l'environnement

- ✅ Fichier `.env` créé avec `VITE_API_URL=http://localhost:8000`
- ✅ Fichier `.env.example` pour la documentation
- ✅ README.md mis à jour avec la documentation complète

### 3. Intégration dans les composants

#### Hero.jsx

- ✅ Utilise `subscribeNewsletter()` pour le formulaire de newsletter
- ✅ Gestion des états de chargement (`isSubmitting`)
- ✅ Affichage des erreurs
- ✅ Feedback visuel pendant l'envoi

#### Home.jsx (3 endroits)

1. **Footer** - Newsletter fixe en bas de page
2. **Section CTA** - Popup de newsletter
3. Les deux utilisent `subscribeNewsletter()`

- ✅ États de chargement indépendants
- ✅ Gestion d'erreurs avec alert
- ✅ Boutons désactivés pendant l'envoi

#### Services.jsx (QuoteWizard)

- ✅ `getAISuggestions()` pour l'analyse IA de la description
- ✅ `createEstimation()` pour envoyer le devis complet
- ✅ Mapping des données vers le format API
- ✅ Gestion d'erreurs avec fallback (continuer en manuel)
- ✅ Messages d'erreur explicites

### 4. Mapping des données

#### Pour les suggestions IA

```javascript
API Response → Frontend
type_projet → project_type
nombre_pages → number_of_pages
fonctionnalites → features
niveau_design → design_level
delai_souhaite → timeline
budget → budget_range
contenu_disponible → has_content
maintenance_requise → needs_maintenance
```

#### Pour l'estimation

```javascript
Frontend → API
{
  client: { email, nom, telephone, entreprise },
  estimation: {
    description_projet,
    type_projet,
    nombre_pages,
    delai_souhaite,
    budget
  }
}
```

## 🧪 Comment tester

### 1. Démarrer l'API backend

```bash
# Assurez-vous que l'API tourne sur http://localhost:8000
```

### 2. Démarrer le frontend

```bash
cd landing-page-front
npm run dev
```

### 3. Tester les fonctionnalités

#### Newsletter

- Cliquer sur "S'abonner à la newsletter" dans le Hero
- Remplir l'email et soumettre
- Vérifier la console réseau (Network tab)
- Vérifier que l'API reçoit bien la requête POST /newsletter

#### Estimation

- Cliquer sur "Obtenir un devis"
- Remplir la description du projet
- Cliquer sur "Analyser avec l'IA" ou "Suivant"
- Remplir le formulaire complet
- Soumettre
- Vérifier POST /ai/suggest et POST /estimations

## 🔧 Prochaines étapes

1. ✅ Services API créés et intégrés
2. ✅ Gestion des erreurs implémentée
3. ✅ États de chargement ajoutés
4. ⏳ Tests avec l'API backend réelle
5. ⏳ Améliorer les messages d'erreur si nécessaire
6. ⏳ Ajouter des validations côté client supplémentaires

## 📝 Notes importantes

- **CORS** : Assurez-vous que l'API backend autorise les requêtes depuis `http://localhost:5173`
- **Variables d'env** : Le fichier `.env` n'est PAS commité (utilisez `.env.example`)
- **Production** : Changez `VITE_API_URL` pour pointer vers votre API en production
- **Ancienne dépendance** : L'ancien `base44Client.js` n'est plus utilisé et peut être supprimé

## 🐛 Debugging

Si les appels API ne fonctionnent pas :

1. Vérifier la console navigateur (F12)
2. Vérifier l'onglet Network pour voir les requêtes
3. Vérifier que `VITE_API_URL` est correctement défini
4. Vérifier que l'API backend est démarrée
5. Vérifier les logs du backend pour les erreurs CORS
