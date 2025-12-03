# Macros Jinja2 pour les Templates Email

Ce fichier contient les macros réutilisables pour tous les templates d'emails.

## 📦 Fichiers de macros

- **`_macros.html.j2`** : Macros pour templates HTML
- **`_macros.txt.j2`** : Macros pour templates texte

## 🎨 Macros HTML disponibles

### `email_styles()`

Retourne tous les styles CSS communs pour les emails.

**Usage:**

```jinja
{% from "_macros.html.j2" import email_styles %}
<!DOCTYPE html>
<html>
<head>
    {{ email_styles() }}
</head>
```

**Styles inclus:**

- Structure body et container
- Header avec gradient violet/bleu
- Content avec padding
- Boutons CTA
- Footer
- Classes utilitaires

### `email_header(title)`

Génère le header d'email avec le gradient et le titre.

**Paramètres:**

- `title` (string) : Titre affiché dans le header (défaut: "Axynis")

**Usage:**

```jinja
{% from "_macros.html.j2" import email_header %}
{{ email_header("🎉 Bienvenue chez Axynis !") }}
```

**Rendu:**

```html
<div class="header">
  <h1>🎉 Bienvenue chez Axynis !</h1>
</div>
```

### `email_footer(email, unsubscribe_url=None)`

Génère le footer d'email avec informations de contact et lien de désinscription optionnel.

**Paramètres:**

- `email` (string, requis) : Email du destinataire
- `unsubscribe_url` (string, optionnel) : URL de désinscription

**Usage:**

```jinja
{% from "_macros.html.j2" import email_footer %}
{{ email_footer(email, unsubscribe_url) }}
```

**Rendu:**

```html
<div class="footer">
  <p>Cet email a été envoyé à <strong>user@example.com</strong></p>
  <p>© 2025 Axynis. Tous droits réservés.</p>
  <p>🌐 <a href="https://axynis.cloud">axynis.cloud</a></p>
  <p style="margin-top: 15px;">
    <a href="...">Se désinscrire de la newsletter</a>
  </p>
</div>
```

## 📝 Macros TEXT disponibles

### `email_footer_text(email, unsubscribe_url=None)`

Génère le footer texte pour les emails en format texte brut.

**Paramètres:**

- `email` (string, requis) : Email du destinataire
- `unsubscribe_url` (string, optionnel) : URL de désinscription

**Usage:**

```jinja
{% from "_macros.txt.j2" import email_footer_text %}
{{ email_footer_text(email, unsubscribe_url) }}
```

**Rendu:**

```
---
Cet email a été envoyé à user@example.com
© 2025 Axynis. Tous droits réservés.
🌐 https://axynis.cloud

Se désinscrire : https://axynis.cloud/unsubscribe?email=xxx
```

## 🔧 Utilisation dans un template

### Template HTML complet

```jinja
{% from "_macros.html.j2" import email_header, email_footer, email_styles %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ email_styles() }}
</head>
<body>
    <div class="email-container">
        {{ email_header("Mon Titre Personnalisé") }}

        <div class="content">
            <p>Bonjour {{ nom }},</p>
            <p>Votre contenu ici...</p>
        </div>

        {{ email_footer(email, unsubscribe_url) }}
    </div>
</body>
</html>
```

### Template TEXT complet

```jinja
Bonjour {{ nom }},

Votre contenu en texte brut...

Cordialement,
L'équipe Axynis

{% from "_macros.txt.j2" import email_footer_text %}
{{ email_footer_text(email, unsubscribe_url) }}
```

## ✨ Avantages

1. **Cohérence** : Tous les emails ont le même style
2. **Maintenabilité** : Modifier le footer = modifier un seul fichier
3. **DRY** : Don't Repeat Yourself
4. **Flexibilité** : Lien de désinscription optionnel
5. **Réutilisabilité** : Import dans n'importe quel template

## 📋 Variables globales requises

Ces variables doivent être passées au contexte Jinja2 :

- `email` : Email du destinataire
- `year` : Année actuelle (généré automatiquement)
- `unsubscribe_url` : URL de désinscription (optionnel)

## 🎯 Templates utilisant les macros

- ✅ `newsletter_confirmation.html.j2`
- ✅ `newsletter_confirmation.txt.j2`
- ✅ `estimation_confirmation.html.j2`
- ✅ `estimation_confirmation.txt.j2`
- ✅ `admin_notification.html.j2`
- ✅ `admin_notification.txt.j2`

## 🔄 Personnalisation

Pour modifier le style de tous les emails :

1. **Éditer `_macros.html.j2`**

   - Modifier les couleurs du gradient
   - Ajuster les paddings
   - Changer la police

2. **Les changements s'appliquent automatiquement** à tous les templates

Exemple : Changer le gradient violet → vert

```jinja
.header {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}
```

## 📚 Références Jinja2

- [Jinja2 Macros Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/#macros)
- [Jinja2 Import Statement](https://jinja.palletsprojects.com/en/3.1.x/templates/#import)
