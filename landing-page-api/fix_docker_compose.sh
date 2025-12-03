#!/bin/bash
# Script pour ajouter les variables SMTP au docker-compose.yaml et redémarrer

echo "════════════════════════════════════════════════════════════"
echo "🔧 CORRECTION DOCKER-COMPOSE.YAML"
echo "════════════════════════════════════════════════════════════"
echo ""

ssh root@148.230.113.134 << 'ENDSSH'
cd ~/landing-page

echo "1️⃣ Sauvegarde du docker-compose.yaml..."
cp docker-compose.yaml docker-compose.yaml.backup.$(date +%Y%m%d_%H%M%S)
echo "✅ Sauvegarde créée"
echo ""

echo "2️⃣ Modification du service API pour ajouter les variables SMTP..."

# Création du nouveau docker-compose.yaml avec les variables SMTP
cat > docker-compose.yaml << 'EOF'
version: "3.9"

services:
  # Base de données PostgreSQL
  postgres:
    image: postgres:16-alpine
    container_name: marketing-bot-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # pgAdmin pour visualiser la base de données
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: marketing-bot-pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
      PGADMIN_CONFIG_SERVER_MODE: "False"
    ports:
      - "5050:80"
    networks:
      - app-network
    depends_on:
      - postgres
    volumes:
      - pgadmin_data:/var/lib/pgadmin

  # API FastAPI
  api:
    build:
      context: ./landing-page-api
      dockerfile: Dockerfile
    container_name: marketing-bot-api
    restart: unless-stopped
    env_file:
      - .env
    environment:
      DATABASE_URL: ${DATABASE_URL}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      API_HOST: ${API_HOST}
      API_PORT: ${API_PORT}
      SMTP_SERVER: ${SMTP_SERVER}
      SMTP_PORT: ${SMTP_PORT}
      SMTP_EMAIL: ${SMTP_EMAIL}
      SMTP_PASSWORD: ${SMTP_PASSWORD}
      ADMIN_EMAIL: ${ADMIN_EMAIL}
    volumes:
      - ./landing-page-api:/app
    ports:
      - "${API_PORT}:${API_PORT}"
    networks:
      - app-network
    depends_on:
      postgres:
        condition: service_healthy
    command: uvicorn src.main:app --host ${API_HOST} --port ${API_PORT} --reload

  # Frontend React
  frontend:
    build:
      context: ./landing-page-front
      dockerfile: Dockerfile
    container_name: marketing-bot-frontend
    restart: unless-stopped
    environment:
      # Variable d'environnement pour Vite (mode dev)
      - VITE_API_URL=${VITE_API_URL}
    ports:
      - "3000:3000"
    volumes:
      - ./landing-page-front:/app
      - /app/node_modules
    networks:
      - app-network
    depends_on:
      - api

  # Nginx Proxy Manager
  nginx-proxy-manager:
    image: jc21/nginx-proxy-manager:latest
    container_name: marketing-bot-npm
    restart: unless-stopped
    ports:
      - "80:80" # HTTP
      - "443:443" # HTTPS
      - "81:81" # Interface d'administration
    environment:
      DB_SQLITE_FILE: "/data/database.sqlite"
      DISABLE_IPV6: "true"
    volumes:
      - npm_data:/data
      - npm_letsencrypt:/etc/letsencrypt
    networks:
      - app-network
    depends_on:
      - api
      - frontend

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
  pgadmin_data:
  npm_data:
  npm_letsencrypt:
EOF

echo "✅ docker-compose.yaml modifié"
echo ""

echo "3️⃣ Vérification du .env..."
if grep -q "ADMIN_EMAIL" .env; then
    echo "✅ ADMIN_EMAIL existe dans .env"
else
    echo "⚠️  Ajout de ADMIN_EMAIL au .env..."
    echo "" >> .env
    echo "# Admin Email for system notifications" >> .env
    echo "ADMIN_EMAIL=j.dussauld@gmail.com" >> .env
fi
echo ""

echo "4️⃣ Redémarrage des conteneurs..."
docker-compose down
echo ""
docker-compose up -d
echo ""

echo "5️⃣ Attente du démarrage de l'API (30 secondes)..."
sleep 30
echo ""

echo "6️⃣ Vérification des variables SMTP dans le conteneur..."
docker exec marketing-bot-api env | grep -E "SMTP|ADMIN_EMAIL" | sort
echo ""

echo "════════════════════════════════════════════════════════════"
echo "✅ CORRECTION TERMINÉE"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Test de l'envoi d'email depuis Python :"
docker exec marketing-bot-api python -c "
import os
print('Configuration SMTP:')
print(f'  SMTP_SERVER: {os.getenv(\"SMTP_SERVER\", \"NON DÉFINI\")}')
print(f'  SMTP_PORT: {os.getenv(\"SMTP_PORT\", \"NON DÉFINI\")}')
print(f'  SMTP_EMAIL: {os.getenv(\"SMTP_EMAIL\", \"NON DÉFINI\")}')
print(f'  SMTP_PASSWORD: {\"***\" if os.getenv(\"SMTP_PASSWORD\") else \"NON DÉFINI\"}')
print(f'  ADMIN_EMAIL: {os.getenv(\"ADMIN_EMAIL\", \"NON DÉFINI\")}')
"

ENDSSH

echo ""
echo "════════════════════════════════════════════════════════════"
echo "🧪 TEST D'ENVOI D'EMAIL"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Pour tester l'envoi d'email maintenant :"
echo ""
echo "curl -X POST https://axynis.cloud/api/newsletter \\
  -H 'Content-Type: application/json' \\
  -d '{\"email\":\"test@example.com\"}'"
echo ""
