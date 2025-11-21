# 🩸 Prompt pour créer le Frontend Slasherz

Copie-colle ce texte à un autre Claude pour qu'il crée le frontend.

---

## Mission

Créer un site web de galerie pour **Slasherz**, un jeu de cartes à collectionner horrifique avec 700 cartes.

## Architecture

- **Frontend** : `slasherz.fr` (repo : https://github.com/lusokol/Slasherz-Frontend)
- **Backend API** : `slasherz.fr/api`

## API Backend

### Endpoint principal
```
GET https://slasherz.fr/api/cards/all
```

Retourne un tableau de 700 cartes :
```json
[
  {
    "id": "uuid",
    "code": "M1-001",
    "name": "Andy - Jeune garçon",
    "description": "Texte de l'effet...",
    "type": "survivant",
    "dimension": "desert",
    "level": null,
    "score": null,
    "rarity": "commune",
    "image_name": "andy_jeune_garcon",
    "last_updated": "2025-10-21T18:23:06Z"
  }
]
```

### Images des cartes
```
https://slasherz.fr/api/images/{image_name}.webp
```

Exemple : `https://slasherz.fr/api/images/andy_jeune_garcon.webp`

## Données importantes

### Types de cartes (9)
- `survivant` : Identité joueur (30 cartes)
- `victime` : Cibles à protéger (68 cartes)
- `lvl1` : Personnages de base (148 cartes)
- `lvl2` : Évolutions (60 cartes)
- `lvl3` : Finishers (30 cartes)
- `objet` : Équipements (128 cartes)
- `lieu` : Terrains (100 cartes)
- `evenement` : Sorts instantanés (130 cartes)
- `jeton` : Créés par effets (6 cartes)

### Dimensions (5)
- `desert` 🏜️ : Gagner des PV
- `nature` 🌲 : Accumuler des personnages
- `urbain` 🏙️ : Dégâts par effets
- `enfer` 🔥 : Sacrifices pour avantage
- `espace` 🌌 : Utiliser cartes retirées

### Raretés (4)
- `commune` : Gris (#666)
- `rare` : Bronze (#cd7f32)
- `super_rare` : Argent (#c0c0c0)
- `mythique` : Or (#d4af37) ← avec animation pulsante

## Design requis

### Palette de couleurs
```css
--blood-red: #8B0000;
--dark-red: #450000;
--black: #0a0a0a;
--gray: #1a1a1a;
--text: #e0e0e0;
```

### Thème
- **Style** : Horrifique/Slasher (pensez à des films d'horreur années 80-90)
- **Ambiance** : Sombre, rouge sang, effets de sang qui goutte
- **Fonts** : `Nosifer`, `Creepster`, `Metal Mania` (Google Fonts)
- **Animations** : Effets hover dramatiques, ombres rouges brillantes

### Layout suggéré

```
┌─────────────────────────────────────────────┐
│  🔪 SLASHERZ 🩸 - Collection des Horreurs  │
├─────────────────────────────────────────────┤
│  📊 Stats : 700 cartes | 30 Survivants...  │
├─────────────────────────────────────────────┤
│  🔍 [Recherche] [Type▼] [Dimension▼] [...]│
├─────────────────────────────────────────────┤
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐  │
│  │🃏│ │🃏│ │🃏│ │🃏│ │🃏│ │🃏│ │🃏│ │🃏│  │
│  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘  │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐  │
│  │🃏│ │🃏│ │🃏│ │🃏│ │🃏│ │🃏│ │🃏│ │🃏│  │
│  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘  │
│  ... (grille de 700 cartes)                │
└─────────────────────────────────────────────┘
```

## Fonctionnalités requises

### 1. Affichage des cartes
- Grille responsive : `grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))`
- Ratio des cartes : **5:7** (format carte standard)
- Hover : zoom + ombre rouge brillante

### 2. Badges visuels
- **Badge rareté** : Coin supérieur droit (avec couleurs ci-dessus)
- **Badge dimension** : Coin supérieur gauche (emoji + couleur de fond)
  - 🏜️ Desert: #f4a460
  - 🌲 Nature: #228b22
  - 🏙️ Urbain: #808080
  - 🔥 Enfer: #ff4500
  - 🌌 Espace: #191970

### 3. Filtres
- Barre de recherche (nom + description)
- Select Type (9 options)
- Select Dimension (5 options)
- Select Rareté (4 options)
- Tout filtrer côté client (pas d'appels API supplémentaires)

### 4. Modal de détail
- Au clic sur une carte → modal avec :
  - Grande image (300x420px)
  - Nom complet
  - Code (M1-001, etc.)
  - Type, Dimension, Rareté
  - Level et Score (si applicable, sinon cacher)
  - Description complète
- Fermeture : X, clic extérieur, touche Escape

### 5. Statistiques
Afficher en haut de page :
- Total cartes : 700
- Survivants : 30
- Personnages (LVL1+2+3) : 238
- Mythiques : (calculer)

### 6. Responsive
- Mobile : 2 colonnes
- Tablette : 3-4 colonnes
- Desktop : 5-7 colonnes

## Code de démarrage

### Fetch des cartes
```javascript
async function loadCards() {
  const response = await fetch('https://slasherz.fr/api/cards/all');
  const cards = await response.json();
  return cards;
}

function getCardImageUrl(imageName) {
  return `https://slasherz.fr/api/images/${imageName}.webp`;
}
```

### Gestion des valeurs NULL
```javascript
// level et score peuvent être null ou -1
const displayLevel = card.level && card.level !== -1 ? card.level : 'N/A';
const displayScore = card.score && card.score !== -1 ? card.score : 'N/A';
```

### Filtres
```javascript
function filterCards(cards, filters) {
  return cards.filter(card => {
    const matchSearch = !filters.search ||
      card.name.toLowerCase().includes(filters.search.toLowerCase()) ||
      (card.description && card.description.toLowerCase().includes(filters.search.toLowerCase()));

    const matchType = !filters.type || card.type === filters.type;
    const matchDimension = !filters.dimension || card.dimension === filters.dimension;
    const matchRarity = !filters.rarity || card.rarity === filters.rarity;

    return matchSearch && matchType && matchDimension && matchRarity;
  });
}
```

### Placeholder pour images manquantes
```html
<img
  src="https://slasherz.fr/api/images/${card.image_name}.webp"
  onerror="this.src='data:image/svg+xml,%3Csvg...placeholder...'"
  alt="${card.name}"
>
```

## Notes importantes

1. **Toutes les images** sont en `.webp` (obligatoire)
2. **Charger une seule fois** : Fetch `/api/cards/all` au chargement, puis filtrer côté client
3. **Valeurs NULL** : `level` et `score` peuvent être `null` ou `-1` pour "Non applicable"
4. **700 cartes** : Optimiser l'affichage (lazy loading si nécessaire)
5. **Cartes brillantes** : Ce sont des cartes séparées (pas un flag), elles ont "-Brillante" dans le nom
6. **Pas d'authentification** : L'endpoint `/api/cards/all` est public

## Exemples de cartes

### Survivant
```json
{
  "name": "Andy - Jeune garçon",
  "type": "survivant",
  "dimension": "desert",
  "level": null,
  "score": null,
  "rarity": "commune",
  "image_name": "andy_jeune_garcon"
}
```

### Personnage LVL2
```json
{
  "name": "Tueur masqué",
  "type": "lvl2",
  "dimension": "enfer",
  "level": 2,
  "score": 1500,
  "rarity": "rare",
  "image_name": "tueur_masque"
}
```

### Objet
```json
{
  "name": "Tronçonneuse",
  "type": "objet",
  "dimension": "enfer",
  "level": null,
  "score": null,
  "rarity": "super_rare",
  "image_name": "tronconneuse"
}
```

## Checklist

- [ ] Fetch et afficher les 700 cartes
- [ ] Grille responsive 5:7 ratio
- [ ] Images depuis `/api/images/{nom}.webp`
- [ ] Badges rareté + dimension
- [ ] Filtres (recherche, type, dimension, rareté)
- [ ] Modal de détail au clic
- [ ] Statistiques en haut
- [ ] Thème horrifique (rouge sang, noir, fonts effrayantes)
- [ ] Animations hover
- [ ] Gestion des NULL/-1
- [ ] Placeholder images manquantes
- [ ] Responsive mobile/desktop

## Inspiration visuelle

Pense à :
- Films : Friday the 13th, Nightmare on Elm Street, Scream
- Couleurs : Sang qui coule, nuit noire, néons rouges
- Ambiance : VHS années 80, grindhouse, slasher
- Effets : Glitch, dripping blood, scratches

**Objectif** : Une galerie immersive qui donne l'impression d'explorer une collection de films d'horreur cultes sous forme de cartes ! 🩸🔪

Bon développement ! 💀
