# Fonctionnalité de Désinscription Newsletter

## 📋 Vue d'ensemble

Cette fonctionnalité permet aux utilisateurs de se désinscrire de la newsletter en un clic depuis l'email reçu.

## ✅ Composants implémentés

### 1. Routes API (`src/routes/clients.py`)

#### POST `/api/newsletter`

Inscription à la newsletter avec envoi d'email de confirmation.

**Body:**

```json
{
  "email": "user@example.com"
}
```

**Réponse:**

```json
{
  "message": "Merci pour votre inscription !",
  "email_sent": true
}
```

**Erreurs:**

- `503` : Impossible d'envoyer l'email
- `500` : Erreur serveur

#### GET `/api/newsletter/client/{email}`

Récupère les informations d'un client par email.

**Réponse:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "prenom": "Jean",
  "nom": "Dupont",
  "newsletter": true
}
```

**Erreurs:**

- `404` : Email non trouvé
- `500` : Erreur serveur

#### POST `/api/newsletter/unsubscribe/{email}`

Désinscrit un utilisateur de la newsletter (met `newsletter` à `false`).

**Réponse:**

```json
{
  "message": "Vous avez été désinscrit avec succès de notre newsletter",
  "email": "user@example.com",
  "newsletter": false
}
```

**Erreurs:**

- `404` : Email non trouvé
- `500` : Erreur serveur

### 2. Templates Email

#### `newsletter_confirmation.html.j2`

Template HTML enrichi avec :

- Header gradient violet/bleu
- Liste des bénéfices
- Bouton CTA "Découvrir nos services"
- **Lien de désinscription en footer**

#### `newsletter_confirmation.txt.j2`

Version texte brut avec lien de désinscription.

**Variables disponibles:**

- `{{ email }}` : Email du destinataire
- `{{ year }}` : Année actuelle
- `{{ unsubscribe_url }}` : URL de désinscription complète

### 3. Service Email (`src/services/email_service/email_service.py`)

#### `send_newsletter_confirmation(email, base_url="https://axynis.cloud")`

Envoie l'email de confirmation avec génération automatique du lien de désinscription.

**Paramètres:**

- `email`: Email du destinataire
- `base_url`: URL de base du site (défaut: https://axynis.cloud)

**URL générée:**

```
https://axynis.cloud/unsubscribe?email={email_encodé}
```

### 4. Page React de Désinscription (`src/pages/Unsubscribe.jsx`)

#### Fonctionnalités

1. **Récupération de l'email depuis l'URL**

   - Parse le paramètre `?email=xxx`
   - Vérifie la présence de l'email

2. **Vérification du statut**

   - Appel API pour vérifier si l'email existe
   - Détecte si déjà désinscrit

3. **Formulaire de désinscription**

   - Affiche l'email concerné
   - Liste les avantages perdus
   - Boutons "Annuler" et "Me désinscrire"

4. **États possibles**
   - Loading : Vérification en cours
   - Email manquant : Erreur, pas d'email dans l'URL
   - Email non trouvé : 404, email inconnu
   - Déjà désinscrit : Déjà fait
   - Confirmation : Formulaire de désinscription
   - Succès : Désinscription effectuée

#### Design

- Gradient violet/bleu en arrière-plan
- Card centrée avec Material Design
- Icônes Lucide React
- Composants shadcn/ui

## 🔧 Configuration

### Variables d'environnement (`.env`)

```bash
# Email SMTP
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=587
SMTP_EMAIL=contact@axynis.cloud
SMTP_PASSWORD=!m0GoSq[:;iv
ADMIN_EMAIL=j.dussauld@gmail.com

# URL de base pour les liens
VITE_API_URL=/api
```

### Base de données

Le champ `newsletter` existe déjà dans le modèle `Client` :

```python
newsletter: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
```

## 🧪 Tests

### Test manuel complet

1. **Inscription**

   ```bash
   curl -X POST https://axynis.cloud/api/newsletter \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com"}'
   ```

2. **Vérifier l'email reçu**

   - Ouvrir la boîte mail
   - Vérifier le lien de désinscription

3. **Cliquer sur le lien**

   - Ouvre `https://axynis.cloud/unsubscribe?email=test@example.com`
   - Page de confirmation s'affiche

4. **Se désinscrire**

   - Cliquer sur "Me désinscrire"
   - Message de succès

5. **Vérifier en base**
   ```sql
   SELECT email, newsletter FROM clients WHERE email='test@example.com';
   -- newsletter devrait être FALSE
   ```

### Script de test automatique

```bash
cd landing-page-api
python test_unsubscribe.py
```

## 📱 Expérience utilisateur

### Parcours complet

1. **Utilisateur s'inscrit** sur le site
   → Email de confirmation envoyé

2. **Utilisateur reçoit l'email**
   → Contient le lien de désinscription en bas

3. **Utilisateur clique sur "Se désinscrire"**
   → Redirigé vers `/unsubscribe?email=xxx`

4. **Page affiche le formulaire**
   → Email préchargé
   → Liste des avantages perdus
   → Bouton de confirmation

5. **Utilisateur confirme**
   → Appel API POST `/api/newsletter/unsubscribe/{email}`
   → Message de succès

6. **Base de données mise à jour**
   → `newsletter = False`
   → Ne recevra plus d'emails

### Messages utilisateur

| Situation              | Message                                                    |
| ---------------------- | ---------------------------------------------------------- |
| Désinscription réussie | "Vous avez été désinscrit avec succès de notre newsletter" |
| Déjà désinscrit        | "Vous êtes déjà désinscrit de notre newsletter"            |
| Email non trouvé       | "Email non trouvé dans notre base de données"              |
| Erreur serveur         | "Erreur lors de la désinscription"                         |

## 🚀 Déploiement

### Frontend

```bash
cd landing-page-front
npm run build
docker-compose up -d --build frontend
```

### Backend

```bash
cd landing-page-api
docker-compose up -d --build api
```

### Test en production

```bash
# Tester l'API
curl https://axynis.cloud/api/newsletter/client/test@example.com

# Tester la page
open https://axynis.cloud/unsubscribe?email=test@example.com
```

## 📊 Monitoring

### Logs à surveiller

```bash
# Logs API
docker-compose logs -f api | grep unsubscribe

# Logs emails
docker-compose logs -f api | grep "Email envoyé"
```

### Métriques importantes

- Taux de désinscription
- Emails envoyés vs emails délivrés
- Erreurs SMTP
- Temps de réponse API

## 🔒 Sécurité

### Mesures implémentées

1. **Encodage de l'email** dans l'URL

   - `urllib.parse.quote(email)`
   - Évite les injections

2. **Validation des entrées**

   - Email validé par Pydantic `EmailStr`
   - Paramètres SQL paramétrés

3. **Gestion d'erreurs**

   - Pas de détails d'implémentation exposés
   - Messages utilisateur génériques

4. **Pas d'authentification requise**
   - Désinscription simple (lien email)
   - Pas de token nécessaire

### Considérations

⚠️ **Note**: La désinscription ne nécessite pas d'authentification. C'est volontaire pour simplifier le processus, mais un token signé pourrait être ajouté pour plus de sécurité.

## 📚 Références

- [RFC 8058 - Signaling of One-Click Unsubscribe](https://www.rfc-editor.org/rfc/rfc8058.html)
- [CAN-SPAM Act Compliance](https://www.ftc.gov/tips-advice/business-center/guidance/can-spam-act-compliance-guide-business)
- [RGPD - Droit d'opposition](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre3#Article21)

## ✅ Checklist de validation

- [x] Routes API créées et testées
- [x] Templates email avec lien de désinscription
- [x] Page React de désinscription
- [x] Service email mis à jour
- [x] Composants UI (Alert) créés
- [x] Route ajoutée au routeur React
- [x] Gestion d'erreurs complète
- [x] Tests manuels effectués
- [x] Email de test envoyé avec succès
- [ ] Tests en production
- [ ] Monitoring mis en place

## 🎯 Prochaines améliorations possibles

1. **Analytics**

   - Tracker les désinscriptions
   - Raison de désinscription (formulaire optionnel)

2. **Sécurité renforcée**

   - Token signé dans le lien
   - Expiration du lien (24h)

3. **UX améliorée**

   - Animation de désinscription
   - Feedback utilisateur plus détaillé
   - Option de réabonnement facile

4. **Conformité**
   - Header "List-Unsubscribe" (RFC 8058)
   - Export des données utilisateur
