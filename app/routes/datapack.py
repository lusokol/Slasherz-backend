from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime

router = APIRouter(prefix="/datapack", tags=["Datapack"])

# === Chemins vers les fichiers serveurs ===
DATA_PATH = "app/data"
SERVER_DATAPACK = os.path.join(DATA_PATH, "datapack.json")
VERSION_FILE = os.path.join(DATA_PATH, "version.json")


# === Route 1 : obtenir la version actuelle du datapack ===
@router.get("/version")
def get_version():
    """Retourne la version actuelle du datapack (et éventuellement son hash)."""
    if not os.path.exists(VERSION_FILE):
        raise HTTPException(status_code=404, detail="version.json not found")

    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        version_data = json.load(f)

    return version_data


# === Route 2 : synchroniser le datapack ===
@router.post("/sync")
async def sync_datapack(file: UploadFile | None = File(None)):
    """
    Compare le datapack du client avec celui du serveur.
    - Si aucun fichier n’est envoyé → renvoie le datapack complet.
    - Sinon → renvoie les cartes à mettre à jour et à supprimer.
    """

    # Vérifie l’existence du datapack serveur
    if not os.path.exists(SERVER_DATAPACK):
        raise HTTPException(status_code=500, detail="datapack.json not found on server")

    # Charge le datapack du serveur
    with open(SERVER_DATAPACK, "r", encoding="utf-8") as f:
        server_data = json.load(f)
        server_cards = {card["id"]: card for card in server_data.get("cards", [])}

    # Cas 1 : aucun fichier envoyé → on renvoie tout
    if file is None:
        return {
            "mode": "full",
            "version": server_data.get("version"),
            "to_update": list(server_cards.keys()),
            "to_delete": [],
            "datapack": server_data
        }

    # Cas 2 : fichier JSON client envoyé → comparaison différentielle
    try:
        content = await file.read()
        client_data = json.loads(content.decode("utf-8"))
        client_cards = {card["id"]: card for card in client_data.get("cards", [])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {e}")

    to_update = []
    to_delete = []

    # Vérifie les cartes présentes côté serveur
    for card_id, srv_card in server_cards.items():
        clt_card = client_cards.get(card_id)
        if not clt_card:
            to_update.append(card_id)
        else:
            # Compare les dates de mise à jour
            srv_date = srv_card.get("last_updated", "1970-01-01")
            clt_date = clt_card.get("last_updated", "1970-01-01")
            if srv_date > clt_date:
                to_update.append(card_id)

    # Vérifie les cartes supprimées côté client
    for card_id in client_cards.keys():
        if card_id not in server_cards:
            to_delete.append(card_id)

    response = {
        "mode": "diff",
        "version": server_data.get("version"),
        "to_update": to_update,
        "to_delete": to_delete,
        "datapack": server_data
    }

    return JSONResponse(content=response)
