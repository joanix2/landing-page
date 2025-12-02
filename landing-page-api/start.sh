#!/bin/bash

# Script de démarrage rapide pour tester le service IA
# Landing Page API

echo "🚀 Démarrage du service IA - Landing Page API"
echo "=============================================="
echo ""

# Vérifier si .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé"
    echo "📝 Création à partir de .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT : Éditer .env et ajouter votre OPENAI_API_KEY"
    echo "   Obtenir une clé sur : https://platform.openai.com/api-keys"
    echo ""
    read -p "Appuyez sur Entrée une fois la clé ajoutée..."
fi

# Vérifier si le venv existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer le venv
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt --quiet

echo ""
echo "✅ Configuration terminée !"
echo ""

# Menu de choix
echo "Que voulez-vous faire ?"
echo "1) Tester le service IA (sans lancer l'API)"
echo "2) Lancer l'API complète"
echo "3) Voir la documentation"
echo ""
read -p "Votre choix (1-3) : " choice

case $choice in
    1)
        echo ""
        echo "🧪 Lancement du test du service IA..."
        echo ""
        python test_ai_service.py
        ;;
    2)
        echo ""
        echo "🌐 Lancement de l'API FastAPI..."
        echo ""
        echo "📍 API disponible sur : http://localhost:8000"
        echo "📚 Documentation : http://localhost:8000/docs"
        echo ""
        uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
        ;;
    3)
        echo ""
        echo "📖 Documentation disponible :"
        echo "   - AI_SERVICE_GUIDE.md   → Guide rapide"
        echo "   - docs/AI_SERVICE.md    → Documentation complète"
        echo "   - docs/ARCHITECTURE_AI.md → Architecture détaillée"
        echo ""
        ;;
    *)
        echo "❌ Choix invalide"
        ;;
esac
