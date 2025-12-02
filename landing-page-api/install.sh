#!/bin/bash

# Installation rapide des dépendances du service IA
echo "📦 Installation des dépendances pour le Service IA..."
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Créer venv si nécessaire
if [ ! -d "venv" ]; then
    echo "🔧 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer venv
source venv/bin/activate

# Mettre à jour pip
echo "⬆️  Mise à jour de pip..."
pip install --upgrade pip --quiet

# Installer les dépendances
echo "📥 Installation des packages Python..."
pip install -r requirements.txt

echo ""
echo "✅ Installation terminée !"
echo ""
echo "📝 Prochaines étapes :"
echo "   1. Configurer votre clé OpenAI dans .env"
echo "   2. Tester avec : python test_ai_service.py"
echo "   3. Lancer l'API avec : uvicorn src.main:app --reload"
echo ""
echo "📚 Documentation : AI_SERVICE_GUIDE.md"
