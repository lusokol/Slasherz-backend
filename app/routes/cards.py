from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.card import Card, CardType, CardDimension, CardRarity
from datetime import datetime
import os, shutil, uuid
from app.utils.ip_check import verify_ip_whitelist

router = APIRouter(prefix="/api/cards", tags=["Cards"])

IMAGES_PATH = "app/data/images"

# ✅ 1. Ajouter ou modifier une carte
@router.post("/", dependencies=[Depends(verify_ip_whitelist)])
async def add_or_update_card(
    db: Session = Depends(get_db),
    id: str | None = Form(None),
    code: str = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    type: CardType = Form(...),
    dimension: CardDimension = Form(...),
    level_raw: str | None = Form(None),
    score_raw: str | None = Form(None),
    rarity: CardRarity = Form(...),
    file: UploadFile | None = File(None)
):
    """
    Ajoute une nouvelle carte ou met à jour une carte existante.
    Si une image est fournie, elle remplace l’ancienne.
    Si aucune image n’est envoyée :
      - sur création → erreur
      - sur mise à jour → conserve l’image existante
    """

    def parse_nullable_int(x: str | None):
        if x is None:
            return None
        x = x.strip()
        if x in ("", "-1"):
            return None
        try:
            return int(x)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Valeur invalide pour un entier : '{x}'")

    level = parse_nullable_int(level_raw)
    score = parse_nullable_int(score_raw)

    if not code or not name:
        raise HTTPException(status_code=400, detail="Le code et le nom sont obligatoires")

    # Création ou mise à jour
    # if id:
    #     card = db.query(Card).filter(Card.id == id).first()
    #     if not card:
    #         raise HTTPException(status_code=404, detail="Carte introuvable pour mise à jour")
    # else:
    #     card = Card(id=str(uuid.uuid4()))

    card = db.query(Card).filter(Card.id == id).first()
    if not card:
        card = Card(id=str(uuid.uuid4()))

    # Vérifie si une image est fournie
    new_image_name = None
    if file and file.filename:
        filename = os.path.basename(file.filename)
        if not filename.lower().endswith(".webp"):
            raise HTTPException(status_code=400, detail="L'image doit être au format .webp")
        new_image_name = os.path.splitext(filename)[0]

    # Met à jour les champs de la carte
    card.code = code
    card.name = name
    card.description = description
    card.type = type
    card.dimension = dimension
    card.level = level
    card.score = score
    card.rarity = rarity
    card.last_updated = datetime.utcnow()

    os.makedirs(IMAGES_PATH, exist_ok=True)

    # Gestion de l'image
    if new_image_name:
        # Supprime l'ancienne image si le nom a changé
        old_image_name = getattr(card, "image_name", None)
        if old_image_name and old_image_name != new_image_name:
            old_path = os.path.join(IMAGES_PATH, f"{old_image_name}.webp")
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except Exception:
                    pass  # Ne bloque pas sur suppression échouée

        # Sauvegarde de la nouvelle image
        img_path = os.path.join(IMAGES_PATH, f"{new_image_name}.webp")
        try:
            with open(img_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement de l'image : {e}")

        card.image_name = new_image_name

    else:
        # Pas de nouvelle image : vérifie que la carte en a une
        if not getattr(card, "image_name", None):
            raise HTTPException(status_code=400, detail="Une image .webp est requise pour créer une nouvelle carte")

        # Si c’est une mise à jour sans fichier, on garde l'image existante
        # donc rien à faire ici

    db.merge(card)
    db.commit()

    return {"message": "Carte ajoutée ou mise à jour avec succès", "id": card.id}


# 🗑️ 2. Supprimer une carte
@router.delete("/{card_id}", dependencies=[Depends(verify_ip_whitelist)])
async def delete_card(card_id: str, db: Session = Depends(get_db)):
    """
    Supprime une carte et son image associée.
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carte introuvable")

    # Supprimer l'image
    img_path = os.path.join(IMAGES_PATH, f"{card.image_name}.webp")
    if os.path.exists(img_path):
        os.remove(img_path)

    # Supprimer la carte de la DB
    db.delete(card)
    db.commit()

    return {"message": f"Carte {card_id} supprimée avec succès"}


# 📖 (Optionnel) Récupérer une carte
@router.get("/id/{card_id}", dependencies=[Depends(verify_ip_whitelist)])
async def get_card(card_id: str, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carte introuvable")
    return card


@router.get("/all", response_model=List[dict])
def get_all_cards(db: Session = Depends(get_db)):
    """
    Retourne toutes les cartes de la base.
    """
    cards = db.query(Card).all()
    if not cards:
        raise HTTPException(status_code=404, detail="Aucune carte trouvée dans la base.")
    
    return [
        {
            "id": card.id,
            "code": card.code,
            "name": card.name,
            "description": card.description,
            "type": card.type.value if card.type else None,
            "dimension": card.dimension.value if card.dimension else None,
            "level": card.level,
            "score": card.score,
            "rarity": card.rarity.value if card.rarity else None,
            "image_name": card.image_name,
            "last_updated": card.last_updated
        }
        for card in cards
    ]