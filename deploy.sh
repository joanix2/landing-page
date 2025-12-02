#!/bin/bash

# Script de déploiement en production

echo "🚀 Déploiement en production..."

# 1. Vérifier que le fichier .env existe
if [ ! -f .env ]; then
    echo "❌ Fichier .env manquant. Copiez .env.example et configurez-le."
    exit 1
fi

# 2. Vérifier que VITE_API_URL est configuré pour la production
if grep -q "VITE_API_URL=http://localhost" .env; then
    echo "⚠️  VITE_API_URL pointe vers localhost!"
    echo "📝 Mettez à jour VITE_API_URL dans .env avec votre domaine de production"
    echo "   Exemple: VITE_API_URL=https://axynis.cloud/api"
    read -p "Voulez-vous continuer quand même? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 3. Arrêter les conteneurs
echo "🛑 Arrêt des conteneurs..."
docker-compose down

# 4. Reconstruire les images
echo "🔨 Reconstruction des images..."
docker-compose build --no-cache

# 5. Démarrer les services
echo "▶️  Démarrage des services..."
docker-compose up -d

# 6. Afficher les logs
echo "📋 Logs des services (Ctrl+C pour quitter)..."
docker-compose logs -f
