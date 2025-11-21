# 🩸 Documentation API Slasherz Backend

## 📋 Vue d'ensemble

**Slasherz** est un jeu de cartes à collectionner (TCG) avec un thème horrifique/slasher. Le backend est une API REST développée avec **FastAPI** et **PostgreSQL**.

### Architecture des domaines

- **Frontend** : `slasherz.fr` → Interface utilisateur (HTML/CSS/JS)
- **Backend API** : `slasherz.fr/api` → Serveur de données (FastAPI)
- **Images** : `slasherz.fr/api/images/{nom}.webp` → Assets des cartes

---

## 🎮 Contexte du jeu

Slasherz est un TCG où deux joueurs s'affrontent :
- Chaque joueur a **1 Survivant** (identité, 50 PV)
- **4 Victimes** à protéger (10 PV chacune)
- Un deck de **40-60 cartes** (personnages, objets, lieux, événements)
- **5 dimensions** : Désert 🏜️, Nature 🌲, Urbain 🏙️, Enfer 🔥, Espace 🌌
- **4 raretés** : Commune, Rare, Super Rare, Mythique

### Types de cartes (9 types)

| Type | Code | Description |
|------|------|-------------|
| **Survivant** | `survivant` | Identité du joueur (50 PV, capacité unique) |
| **Victime** | `victime` | Cibles à protéger (10 PV, effet au retournement) |
| **Level 1** | `lvl1` | Personnages de base (posables directement) |
| **Level 2** | `lvl2` | Évolutions (nécessite sacrifier 1 LVL1) |
| **Level 3** | `lvl3` | Finishers (nécessite sacrifier 2 LVL1 ou 1 LVL2) |
| **Objet** | `objet` | Équipements (2 max par personnage) |
| **Lieu** | `lieu` | Terrains (2 max sur le terrain, effet continu) |
| **Événement** | `evenement` | Sort instantané (activable à tout moment) |
| **Jeton** | `jeton` | Créé par effets (ne peut pas attaquer/être équipé) |

### Dimensions

| Dimension | Code | Style de jeu |
|-----------|------|--------------|
| 🏜️ Désert | `desert` | Gagner des PV pour épuiser l'adversaire |
| 🌲 Nature | `nature` | Accumuler des Personnages LVL1 |
| 🏙️ Urbain | `urbain` | Infliger des dégâts via effets |
| 🔥 Enfer | `enfer` | Sacrifier ses ressources pour l'avantage rapide |
| 🌌 Espace | `espace` | Utiliser les cartes retirées du jeu |

### Raretés

| Rareté | Code | Couleur |
|--------|------|---------|
| Commune | `commune` | Gris (#666) |
| Rare / Violent | `rare` | Bronze (#cd7f32) |
| Super Rare / Gore | `super_rare` | Argent (#c0c0c0) |
| Mythique / Slasher | `mythique` | Or (#d4af37) |

---

## 🔌 Endpoints de l'API

### Base URL
```
https://slasherz.fr/api
```

---

### 📖 **Endpoints publics** (pas d'authentification)

#### 1. GET `/`
**Route racine - Informations de bienvenue**

**Réponse :**
```json
{
  "message": "Bienvenue sur l'API de Slasherz !"
}
```

---

#### 2. GET `/api/cards/all`
**Récupérer toutes les cartes de la collection**

**Réponse :** `200 OK`
```json
[
  {
    "id": "bc7fba34-2341-47d3-9565-c2519fb9a0e5",
    "code": "M1-001-D",
    "name": "Andy - Jeune garçon - Brillante",
    "description": "Cette capacité ne peut être activée que pendant votre tour...",
    "type": "survivant",
    "dimension": "desert",
    "level": null,
    "score": null,
    "rarity": "commune",
    "image_name": "andy_jeune_garcon_brillante",
    "last_updated": "2025-10-21T18:23:06Z"
  },
  {
    "id": "uuid-carte-2",
    "code": "M1-015",
    "name": "Tueur masqué",
    "description": "Détruit un personnage adverse LVL1.",
    "type": "lvl2",
    "dimension": "enfer",
    "level": 2,
    "score": 1500,
    "rarity": "rare",
    "image_name": "tueur_masque",
    "last_updated": "2025-10-22T10:15:30Z"
  }
]
```

**Statistiques de la collection actuelle :**
- **700 cartes totales**
- 30 Survivants
- 68 Victimes
- 148 LVL1
- 60 LVL2
- 30 LVL3
- 128 Objets
- 100 Lieux
- 130 Événements
- 6 Jetons

**Champs importants :**

| Champ | Type | Description |
|-------|------|-------------|
| `id` | UUID | Identifiant unique de la carte |
| `code` | string | Code collecteur (ex: M1-001, M1-015-D) |
| `name` | string | Nom complet de la carte |
| `description` | string\|null | Texte de l'effet (peut être long) |
| `type` | enum | Type de carte (voir tableau ci-dessus) |
| `dimension` | enum | Dimension (desert, nature, urbain, enfer, espace) |
| `level` | int\|null | Niveau du personnage (1-3) ou `null`/`-1` si N/A |
| `score` | int\|null | Points de combat (0-3000) ou `null`/`-1` si N/A |
| `rarity` | enum | Rareté (commune, rare, super_rare, mythique) |
| `image_name` | string | Nom du fichier image (sans extension) |
| `last_updated` | ISO 8601 | Date de dernière modification |

**Notes :**
- Les valeurs `-1` ou `null` pour `level` et `score` signifient "Non applicable"
- Les Survivants/Victimes n'ont pas de `level` ni `score`
- Les Objets/Lieux/Événements peuvent ne pas avoir de `score`

---

#### 3. GET `/api/images/{image_name}.webp`
**Récupérer l'image d'une carte**

**Exemple :**
```
GET /api/images/andy_jeune_garcon_brillante.webp
```

**Réponse :** Fichier image `.webp`

**Usage :**
```html
<img src="https://slasherz.fr/api/images/andy_jeune_garcon_brillante.webp" alt="Andy">
```

**Notes :**
- Toutes les images sont au format `.webp` (obligatoire)
- L'accès est public (pas d'authentification)
- Utiliser le champ `image_name` de la carte + `.webp`

---

#### 4. GET `/api/datapack/version`
**Obtenir la version actuelle du datapack**

**Réponse :** `200 OK`
```json
{
  "version": "0.0.12",
  "last_update": "2025-10-16 12:22:02"
}
```

**Usage :** Pour vérifier si des mises à jour sont disponibles

---

#### 5. POST `/api/datapack/sync`
**Synchroniser le datapack (mode full ou différentiel)**

**Body (optionnel) :**
```json
{
  "cards": [
    {
      "image_name": "andy_jeune_garcon",
      "last_updated": "2025-10-21T18:23:06Z"
    }
  ]
}
```

**Réponse - Mode FULL** (si aucun body envoyé) :
```json
{
  "mode": "full",
  "version": "0.0.12",
  "to_update": ["andy_jeune_garcon", "chris_victime", "..."],
  "to_delete": [],
  "datapack": {
    "cards": [/* toutes les cartes */]
  }
}
```

**Réponse - Mode DIFF** (si body envoyé) :
```json
{
  "mode": "diff",
  "version": "0.0.12",
  "to_update": ["nouvelle_carte", "carte_modifiee"],
  "to_delete": ["carte_supprimee"],
  "datapack": {
    "cards": [/* toutes les cartes */]
  }
}
```

**Logique :**
- Compare les dates `last_updated` de chaque carte
- Retourne les cartes à mettre à jour (nouvelles ou modifiées)
- Retourne les cartes à supprimer (présentes chez le client mais absentes du serveur)

---

#### 6. POST `/api/datapack/hashcheck`
**Vérifier l'intégrité du datapack avec hash BLAKE2b**

**Body :**
```json
{
  "hash": "blake2b_hash_du_client"
}
```

**Réponse :**
```json
{
  "server_hash": "abc123...",
  "is_same": false
}
```

**Usage :** Détecter rapidement si le datapack local est à jour

---

#### 7. GET `/db-test`
**Tester la connexion à la base de données PostgreSQL**

**Réponse :**
```json
{
  "postgres_version": "PostgreSQL 14.5 on x86_64-pc-linux-gnu..."
}
```

---

### 🔐 **Endpoints protégés** (whitelist IP uniquement)

Les routes suivantes nécessitent que l'IP soit dans la liste `ALLOWED_IPS` (variable d'environnement).

**Erreur si IP non autorisée :**
```json
{
  "detail": "Accès refusé pour l'adresse IP : 192.168.1.100"
}
```
**Status :** `403 Forbidden`

---

#### 8. GET `/api/admin`
**Page d'administration HTML**

**Réponse :** Page HTML avec interface CRUD pour gérer les cartes

**Fonctionnalités :**
- Liste toutes les cartes avec recherche
- Formulaire d'ajout/modification
- Upload d'images .webp
- Suppression de cartes

---

#### 9. POST `/api/cards/`
**Ajouter ou modifier une carte**

**Headers :** `Content-Type: multipart/form-data`

**Body (FormData) :**
```
id: "uuid" ou null (généré si null)
code: "M1-025"
name: "Nouvelle carte"
description: "Effet de la carte..."
type: "lvl1"
dimension: "enfer"
level_raw: "1" ou "" ou "-1"
score_raw: "1200" ou "" ou "-1"
rarity: "rare"
file: [fichier .webp] (optionnel si mise à jour)
```

**Réponse :** `200 OK`
```json
{
  "message": "Carte ajoutée ou mise à jour avec succès",
  "id": "uuid-de-la-carte"
}
```

**Règles :**
- Image obligatoire pour création (`.webp` uniquement)
- Image optionnelle pour mise à jour (conserve l'ancienne si non fournie)
- Si `level_raw` ou `score_raw` = `""` ou `"-1"` → stocké comme `null`

---

#### 10. DELETE `/api/cards/{card_id}`
**Supprimer une carte**

**Exemple :**
```
DELETE /api/cards/bc7fba34-2341-47d3-9565-c2519fb9a0e5
```

**Réponse :** `200 OK`
```json
{
  "message": "Carte bc7fba34-2341-47d3-9565-c2519fb9a0e5 supprimée avec succès"
}
```

**Actions :**
- Supprime la carte de la base de données
- Supprime le fichier image `.webp` associé

---

#### 11. GET `/api/cards/id/{card_id}`
**Récupérer une carte spécifique par ID**

**Exemple :**
```
GET /api/cards/id/bc7fba34-2341-47d3-9565-c2519fb9a0e5
```

**Réponse :** Objet carte (même format que `/api/cards/all`)

---

## 🎨 Recommandations pour le Frontend

### 1. Affichage des cartes

**Grille responsive :**
```css
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}
```

**Ratio des cartes :**
- Aspect ratio : **5:7** (format carte standard)
- Taille recommandée : 200x280px minimum

**Badges visuels :**
- **Rareté** : Badge coloré en haut à droite
  - Commune : gris (#666)
  - Rare : bronze (#cd7f32)
  - Super Rare : argent (#c0c0c0)
  - Mythique : or (#d4af37) avec animation pulsante

- **Dimension** : Badge circulaire en haut à gauche avec emoji
  - 🏜️ Désert : #f4a460
  - 🌲 Nature : #228b22
  - 🏙️ Urbain : #808080
  - 🔥 Enfer : #ff4500
  - 🌌 Espace : #191970

### 2. Filtres recommandés

```javascript
// Filtres à implémenter
const filters = {
  search: '', // Recherche dans nom + description
  type: '',   // Type de carte
  dimension: '', // Dimension
  rarity: ''  // Rareté
};
```

### 3. Statistiques en temps réel

Calculer et afficher :
- Nombre total de cartes
- Nombre par type (Survivants, Personnages, etc.)
- Nombre par rareté
- Nombre par dimension

### 4. Modal de détail

Au clic sur une carte, afficher :
- Grande image (300x420px recommandé)
- Nom complet
- Code collecteur
- Type et dimension
- Level et Score (si applicable)
- Description complète
- Rareté

### 5. Thème visuel

**Palette horrifique :**
```css
:root {
  --blood-red: #8B0000;
  --dark-red: #450000;
  --black: #0a0a0a;
  --gray: #1a1a1a;
  --text: #e0e0e0;
}
```

**Typographies recommandées :**
- Titres : `Nosifer`, `Creepster`, `Metal Mania` (Google Fonts)
- Corps : Arial, sans-serif

**Animations :**
- Hover sur cartes : `translateY(-10px) scale(1.05)`
- Ombres rouges : `box-shadow: 0 15px 40px rgba(139, 0, 0, 0.8)`
- Transitions : `transition: all 0.3s ease`

### 6. Gestion des images manquantes

```javascript
<img
  src="/api/images/${card.image_name}.webp"
  onerror="this.src='placeholder.svg'"
  alt="${card.name}"
>
```

### 7. Performance

**Optimisations :**
- Charger toutes les cartes une seule fois au démarrage
- Filtrer côté client (JS)
- Lazy loading des images si > 100 cartes affichées
- Virtualisation si > 500 cartes

### 8. Responsive design

**Breakpoints recommandés :**
```css
/* Mobile */
@media (max-width: 768px) {
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
}

/* Desktop */
@media (min-width: 1400px) {
  max-width: 1400px;
  margin: 0 auto;
}
```

---

## 🔧 Configuration Backend

### Variables d'environnement

Le backend nécessite ces variables :
```bash
# Base de données PostgreSQL
DB_USER=slasherz_user
DB_PASSWORD=MotDePasseFort!
DB_HOST=localhost
DB_NAME=slasherz

# Sécurité (whitelist IP pour admin)
ALLOWED_IPS=127.0.0.1,192.168.1.100
```

### Technologie backend

- **Framework** : FastAPI 0.119.0
- **Base de données** : PostgreSQL 14+
- **ORM** : SQLAlchemy 2.0.44
- **Serveur** : Uvicorn 0.37.0
- **Images** : Format .webp obligatoire

---

## 📊 Exemples de requêtes

### Fetch avec JavaScript

```javascript
// Récupérer toutes les cartes
async function loadCards() {
  const response = await fetch('https://slasherz.fr/api/cards/all');
  const cards = await response.json();
  return cards;
}

// Afficher une image
function getCardImageUrl(imageName) {
  return `https://slasherz.fr/api/images/${imageName}.webp`;
}

// Filtrer les Survivants
const survivors = cards.filter(c => c.type === 'survivant');

// Filtrer par dimension
const hellCards = cards.filter(c => c.dimension === 'enfer');

// Filtrer les Mythiques
const mythics = cards.filter(c => c.rarity === 'mythique');

// Recherche
function searchCards(query) {
  return cards.filter(c =>
    c.name.toLowerCase().includes(query.toLowerCase()) ||
    (c.description && c.description.toLowerCase().includes(query.toLowerCase()))
  );
}
```

---

## 🚨 Erreurs courantes

| Status | Erreur | Cause |
|--------|--------|-------|
| `404` | `Aucune carte trouvée` | La base est vide (peu probable) |
| `403` | `Accès refusé pour l'adresse IP` | IP non dans la whitelist (routes admin) |
| `400` | `L'image doit être au format .webp` | Mauvais format d'image |
| `404` | `Carte introuvable` | ID invalide |
| `500` | `datapack.json not found on server` | Erreur serveur critique |

---

## 📝 Notes importantes

### Versions brillantes
- Les cartes brillantes sont des **cartes séparées** avec un ID unique
- Exemple : "Andy - Jeune garçon" et "Andy - Jeune garçon - Brillante"
- Les effets sont différents (effet supplémentaire pour les brillantes)

### Valeurs NULL vs -1
- Dans la base : `null`
- Dans l'API : peut être `null` ou `-1` selon le contexte
- **Toujours vérifier les deux** : `if (card.level === null || card.level === -1)`

### Images
- **Format obligatoire** : `.webp`
- **Stockage** : `/app/data/images/` (backend)
- **Accès** : `https://slasherz.fr/api/images/{nom}.webp`
- Taille typique : ~50-200 Ko par image

### Système de mise à jour
- Le datapack est régénéré depuis la base PostgreSQL
- Version actuelle : `0.0.12`
- Format de versionnage : `majeur.mineur.patch`
- Le champ `last_updated` permet de détecter les modifications

---

## 🎯 Cas d'usage Frontend

### Page de galerie
- Liste toutes les 700 cartes en grille
- Filtres par type/dimension/rareté
- Barre de recherche
- Modal de détail au clic

### Deck builder (futur)
- Sélection de 1 Survivant
- Sélection de 4 Victimes différentes
- Ajout de 35-55 autres cartes
- Validation : max 3 exemplaires par carte
- Export/Import de deck

### Page de carte individuelle
- Affichage grande taille
- Toutes les informations
- Cartes similaires (même type/dimension)

### Recherche avancée
- Recherche par texte d'effet
- Filtres combinés
- Tri par rareté, score, nom

---

## 🔮 Fonctionnalités futures (non implémentées)

Ces fonctionnalités ne sont **PAS** disponibles dans l'API actuelle :

- ❌ Système de comptes utilisateurs
- ❌ Collection personnelle / progression
- ❌ Moteur de jeu en temps réel
- ❌ Validation de deck
- ❌ Matchmaking
- ❌ Historique de parties
- ❌ Classement / leaderboard

Le backend actuel est un **gestionnaire de contenu** pour distribuer les données des cartes. La logique de jeu doit être implémentée côté client ou dans un serveur de jeu séparé.

---

## ✅ Checklist pour créer le Frontend

1. ✅ Fetch `/api/cards/all` au chargement
2. ✅ Afficher les cartes en grille responsive
3. ✅ Charger les images depuis `/api/images/{nom}.webp`
4. ✅ Gérer les images manquantes avec placeholder
5. ✅ Implémenter les filtres (type, dimension, rareté)
6. ✅ Ajouter une barre de recherche
7. ✅ Créer une modal de détail
8. ✅ Afficher des statistiques (compteurs)
9. ✅ Appliquer le thème horrifique (couleurs, fonts)
10. ✅ Rendre responsive (mobile/tablette/desktop)
11. ✅ Gérer les valeurs NULL/-1 pour level/score
12. ✅ Tester avec les 700 cartes

---

## 🎓 Résumé pour Claude

**En une phrase :**
Crée un site web de galerie de cartes Slasherz en fetchant `https://slasherz.fr/api/cards/all`, en affichant les 700 cartes en grille avec filtres, et en chargeant les images depuis `https://slasherz.fr/api/images/{image_name}.webp` avec un thème horrifique rouge sang et noir.

**URL de base :** `https://slasherz.fr/api`

**Endpoint principal :** `GET /api/cards/all` → 700 cartes

**Images :** `/api/images/{image_name}.webp`

**Thème :** Slasher/Horreur (rouge sang #8B0000, noir profond, fonts effrayantes)

**Bon développement ! 🩸🔪**
