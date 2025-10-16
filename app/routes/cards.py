from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.card import Card

router = APIRouter(prefix="/cards", tags=["Cards"])

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