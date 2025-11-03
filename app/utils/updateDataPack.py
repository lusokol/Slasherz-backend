import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.card import Card

DJSON = "/home/slasherz/Slasherz-backend/app/data/datapack.json"

def update_version():
    db: Session = SessionLocal()

    try:
        cards = db.query(Card).all()
        if not cards:
            print("❌ Aucune carte trouvée dans la base.")
            return

        # Génération du datapack
        data = {
            "cards": [
                {
                    "id": card.id,
                    "code": card.code,
                    "name": card.name,
                    "description": card.description,
                    "type": card.type.value if card.type else None,
                    "dimension": card.dimension.value if card.dimension else None,
                    "level": card.level if card.level else -1,
                    "score": card.score if card.score else -1,
                    "rarity": card.rarity.value if card.rarity else None,
                    "image_name": card.image_name,
                    "last_updated": card.last_updated.strftime("%Y-%m-%dT%H:%M:%SZ") if card.last_updated else None,
                }
                for card in cards
            ],
        }

        with open(DJSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Datapack mis à jour ({len(cards)} cartes).")

    finally:
        db.close()


update_version()