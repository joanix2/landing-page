#!/bin/bash

# Script de démarrage pour tester le cache IA
echo "🧪 Test du système de cache IA"
echo "================================"
echo ""

# Activer l'environnement virtuel si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "📊 Étape 1 : Vérifier les statistiques du cache"
echo ""
python manage_cache.py << EOF
1
5
EOF

echo ""
echo "🤖 Étape 2 : Tester les suggestions IA (avec cache)"
echo ""
python test_ai_service.py

echo ""
echo "📊 Étape 3 : Vérifier les nouvelles statistiques"
echo ""
python manage_cache.py << EOF
1
5
EOF

echo ""
echo "✅ Test terminé !"
echo ""
echo "💡 Pour gérer le cache : python manage_cache.py"
