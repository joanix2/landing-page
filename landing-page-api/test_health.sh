#!/bin/bash

# Script de test du health check

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="${1:-http://localhost:8000}"

echo "🏥 Health Check de l'API"
echo "========================"
echo "URL: $API_URL/health"
echo ""

# Faire la requête
response=$(curl -s -w "\n%{http_code}" "$API_URL/health")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | head -n -1)

# Afficher le code HTTP
if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ Status HTTP: $http_code${NC}"
else
    echo -e "${RED}✗ Status HTTP: $http_code${NC}"
fi

echo ""
echo "Réponse:"
echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
echo ""

# Analyser la réponse
if echo "$body" | grep -q '"status": "healthy"'; then
    echo -e "${GREEN}✓ API Status: HEALTHY${NC}"
    
    if echo "$body" | grep -q '"connected": true'; then
        echo -e "${GREEN}✓ Database: CONNECTED${NC}"
    else
        echo -e "${RED}✗ Database: DISCONNECTED${NC}"
    fi
else
    echo -e "${RED}✗ API Status: UNHEALTHY${NC}"
fi

echo ""
echo "========================"
