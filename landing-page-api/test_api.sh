#!/bin/bash

# Script de test des endpoints de l'API

API_URL="http://localhost:8000"

echo "🧪 Test de l'API Landing Page"
echo "================================"
echo ""

# Test 1: Newsletter
echo "📧 Test 1: Abonnement Newsletter"
echo "--------------------------------"
curl -X POST "$API_URL/newsletter" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}' \
  -w "\nStatus: %{http_code}\n\n"

sleep 1

# Test 2: Estimation
echo "📝 Test 2: Création d'Estimation"
echo "--------------------------------"
curl -X POST "$API_URL/estimations" \
  -H "Content-Type: application/json" \
  -d '{
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
  }' \
  -w "\nStatus: %{http_code}\n\n"

sleep 1

# Test 3: Suggestions IA
echo "🤖 Test 3: Suggestions IA"
echo "--------------------------------"
curl -X POST "$API_URL/ai/suggest" \
  -H "Content-Type: application/json" \
  -d '{"description_projet": "Je veux un site vitrine moderne pour mon restaurant avec menu et réservation en ligne"}' \
  -w "\nStatus: %{http_code}\n\n"

echo ""
echo "✅ Tests terminés!"
