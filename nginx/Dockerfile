# Dockerfile pour Nginx
FROM nginx:alpine

# Supprimer la configuration par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Copier les configurations personnalisées
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d /etc/nginx/conf.d

# Exposer les ports
EXPOSE 80 443

# Commande de démarrage
CMD ["nginx", "-g", "daemon off;"]
