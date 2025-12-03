Mail

- https://app.abusix.com/lookup
- https://check.spamhaus.org/
  Logo
  Style
  Informations
  Page de vente MDE
  Tracking
  ✅ Je veux que l'utilisateur puisse se désinscrire (TERMINÉ)
  - ✅ ajouter la route à l'api pour passer un booleen à false sur l'envoie des email pour un client
    • GET /api/newsletter/client/{email}
    • POST /api/newsletter/unsubscribe/{email}
  - ✅ créer la page créer une page web qui permet la description d'un client
    • /unsubscribe?email=xxx
    • Vérification du statut
    • Formulaire de confirmation
    • Gestion d'erreurs
  - ✅ ajouter le lien au template (ajouter l'url de la page précédante dans le mail)
    • Lien ajouté en footer des templates HTML et TXT
    • URL encodée pour sécurité
    • Doc complète: docs/UNSUBSCRIBE_FEATURE.md
