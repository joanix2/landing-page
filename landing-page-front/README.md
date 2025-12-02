# Landing Page Axynis - Frontend

Landing page pour Axynis avec fonctionnalités de devis et newsletter.

## 🚀 Démarrage rapide

### Prérequis

- Node.js 18+
- npm ou yarn

### Installation

```bash
# Installer les dépendances
npm install

# Copier le fichier d'environnement
cp .env.example .env

# Modifier l'URL de l'API si nécessaire
# VITE_API_URL=http://localhost:8000
```

### Développement

```bash
# Démarrer le serveur de développement
npm run dev
```

Le site sera accessible sur `http://localhost:5173/`

### Build

```bash
# Créer une version de production
npm run build

# Prévisualiser la version de production
npm run preview
```

## 📡 Services API

Le frontend communique avec l'API backend via les services définis dans `src/services/api.js`.

### Endpoints utilisés

#### Newsletter

```javascript
POST / newsletter;
Body: {
  email: string;
}
```

#### Estimation

```javascript
POST /estimations
Body: {
  client: {
    email: string,
    nom?: string,
    telephone?: string,
    entreprise?: string
  },
  estimation: {
    description_projet: string,
    type_projet: string,
    nombre_pages: number,
    delai_souhaite: string,
    budget: string
  }
}
```

#### Suggestions IA

```javascript
POST / ai / suggest;
Body: {
  description_projet: string;
}
```

### Configuration de l'API

L'URL de l'API est configurée via la variable d'environnement `VITE_API_URL` dans le fichier `.env`.

Par défaut: `http://localhost:8000`

## 🏗️ Structure du projet

```
src/
├── api/              # Anciens clients API (à supprimer)
├── assets/           # Images et ressources statiques
├── components/       # Composants React
│   ├── landing/     # Composants de la landing page
│   └── ui/          # Composants UI réutilisables
├── entities/         # Schémas d'entités
├── lib/             # Utilitaires
├── pages/           # Pages principales
├── services/        # Services API
│   └── api.js       # Client API principal
└── App.jsx          # Composant racine
```

## 🎨 Technologies utilisées

- **React 18** - Framework UI
- **Vite** - Build tool et dev server
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Lucide React** - Icônes
- **Radix UI** - Composants UI accessibles

## 📝 Fonctionnalités

- ✅ Page d'accueil avec Hero animé
- ✅ Section services
- ✅ Formulaire de devis avec 3 étapes
- ✅ Analyse IA de la description du projet
- ✅ Abonnement à la newsletter (3 emplacements)
- ✅ Design responsive
- ✅ Animations fluides

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet:

```env
VITE_API_URL=http://localhost:8000
```

Pour la production, adaptez cette URL à votre API déployée.

## 🚀 Déploiement

Le projet peut être déployé sur n'importe quelle plateforme supportant les sites statiques:

- Vercel
- Netlify
- GitHub Pages
- etc.

N'oubliez pas de configurer la variable `VITE_API_URL` avec l'URL de votre API en production.
