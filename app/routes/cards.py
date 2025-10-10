from fastapi import APIRouter

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.get("/")
def get_cards():
    return [{"name": "Jason", "type": "Character", "score": 2510}]