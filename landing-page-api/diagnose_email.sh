#!/bin/bash
# Script de diagnostic pour l'envoi d'email sur le serveur

echo "════════════════════════════════════════════════════════════"
echo "🔍 DIAGNOSTIC EMAIL - SERVEUR AXYNIS.CLOUD"
echo "════════════════════════════════════════════════════════════"
echo ""

# 1. Vérifier le .env sur le serveur
echo "1️⃣ Vérification du .env sur le serveur..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ssh root@148.230.113.134 << 'EOF'
cd ~/landing-page
if [ -f .env ]; then
    echo "✅ Fichier .env existe"
    echo ""
    echo "Variables SMTP trouvées :"
    grep "SMTP" .env || echo "❌ Aucune variable SMTP trouvée"
    echo ""
else
    echo "❌ Fichier .env n'existe pas !"
fi
EOF

echo ""
echo "2️⃣ Vérification des variables dans le conteneur..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ssh root@148.230.113.134 << 'EOF'
echo "Variables SMTP dans le conteneur :"
docker exec marketing-bot-api env | grep SMTP || echo "❌ Aucune variable SMTP"
echo ""
echo "Variable ADMIN_EMAIL :"
docker exec marketing-bot-api env | grep ADMIN_EMAIL || echo "❌ ADMIN_EMAIL non défini"
EOF

echo ""
echo "3️⃣ Vérification du docker-compose.yml..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ssh root@148.230.113.134 << 'EOF'
cd ~/landing-page
echo "Service API dans docker-compose.yml :"
grep -A 20 "api:" docker-compose.yml | grep -E "env_file|environment" || echo "❌ Pas de configuration env trouvée"
EOF

echo ""
echo "4️⃣ Test d'envoi d'email depuis le conteneur..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ssh root@148.230.113.134 << 'EOF'
docker exec marketing-bot-api python -c "
import os
print('SMTP_SERVER:', os.getenv('SMTP_SERVER', 'NON DÉFINI'))
print('SMTP_PORT:', os.getenv('SMTP_PORT', 'NON DÉFINI'))
print('SMTP_EMAIL:', os.getenv('SMTP_EMAIL', 'NON DÉFINI'))
print('SMTP_PASSWORD:', '***' if os.getenv('SMTP_PASSWORD') else 'NON DÉFINI')
print('ADMIN_EMAIL:', os.getenv('ADMIN_EMAIL', 'NON DÉFINI'))
" 2>&1
EOF

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📋 SOLUTIONS POSSIBLES"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Si les variables SMTP ne sont pas dans le conteneur :"
echo ""
echo "Solution 1 : Copier le .env sur le serveur"
echo "  scp .env root@148.230.113.134:~/landing-page/.env"
echo ""
echo "Solution 2 : Vérifier docker-compose.yml"
echo "  Le service 'api' doit avoir : env_file: - .env"
echo ""
echo "Solution 3 : Redémarrer les conteneurs"
echo "  ssh root@148.230.113.134 'cd ~/landing-page && docker-compose down && docker-compose up -d'"
echo ""
echo "Solution 4 : Ajouter manuellement dans docker-compose.yml"
echo "  environment:"
echo "    - SMTP_SERVER=smtp.hostinger.com"
echo "    - SMTP_PORT=587"
echo "    - SMTP_EMAIL=contact@axynis.cloud"
echo "    - SMTP_PASSWORD=!m0GoSq[:;iv"
echo "    - ADMIN_EMAIL=j.dussauld@gmail.com"
echo ""
