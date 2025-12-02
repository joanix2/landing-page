# Dockerfile pour le Frontend React
FROM node:20-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 3000

# Variable d'environnement pour Vite
ENV HOST=0.0.0.0

# Commande pour démarrer le serveur de développement
CMD ["npm", "run", "dev"]
