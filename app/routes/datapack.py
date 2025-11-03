from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
import hashlib
import subprocess
import json
import os
from datetime import datetime

router = APIRouter(prefix="/api/datapack", tags=["Datapack"])

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
async def sync_datapack(client_data: dict | None = Body(None)):
    """
    Compare le datapack du client avec celui du serveur.
    - Si aucun JSON n’est envoyé → renvoie le datapack complet.
    - Sinon → renvoie les cartes à mettre à jour et à supprimer.
    """

    # Vérifie que le datapack serveur existe
    if not os.path.exists(SERVER_DATAPACK):
        raise HTTPException(status_code=500, detail="datapack.json not found on server")

    # Charge le datapack serveur
    with open(SERVER_DATAPACK, "r", encoding="utf-8") as f:
        server_data = json.load(f)
        # print(f"{server_data["cards"]}")
        server_cards = {card["image_name"]: card for card in server_data.get("cards", [])}

    # 🟦 Cas 1 : aucun JSON envoyé → renvoyer tout le datapack
    if not client_data:
        return {
            "mode": "full",
            "version": server_data.get("version"),
            "to_update": list(server_cards.keys()),
            "to_delete": [],
            "datapack": server_data
        }

    # 🟧 Cas 2 : JSON client envoyé → comparaison différentielle
    try:
        client_cards = {card["image_name"]: card for card in client_data.get("cards", [])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid client JSON: {e}")

    to_update = []
    to_delete = []

    # Vérifie les cartes présentes côté serveur
    for card_id, srv_card in server_cards.items():
        clt_card = client_cards.get(card_id)
        if not clt_card:
            to_update.append(card_id)
        else:
            # Compare les dates
            srv_date = srv_card.get("last_updated", "1970-01-01T00:00:00Z")
            clt_date = clt_card.get("last_updated", "1970-01-01T00:00:00Z")
            if srv_date > clt_date:
                to_update.append(card_id)

    # Vérifie les cartes supprimées côté serveur
    for card_id in client_cards.keys():
        if card_id not in server_cards:
            to_delete.append(card_id)

    response = {
        "mode": "diff",
        "version": server_data.get("version"),
        "to_update": to_update,
        "to_delete": to_delete,
        "datapack": server_data,
    }

    return JSONResponse(content=response)

# def compute_b2sum(file_path):
#     import subprocess
#     try:
#         result = subprocess.run(["b2sum", file_path], capture_output=True, text=True)
#         return result.stdout.split()[0]
#     except Exception:
#         # fallback in python if b2sum not available
#         import hashlib
#         BUF_SIZE = 65536
#         blake = hashlib.blake2b()
#         with open(file_path, "rb") as f:
#             while chunk := f.read(BUF_SIZE):
#                 blake.update(chunk)
#         return blake.hexdigest()

def compute_b2sum(file_path):
    """
    Calcule le hash BLAKE2b d'un fichier JSON normalisé :
    - Trie les clés (équivalent jq -S .)
    - Supprime l'indentation et les espaces inutiles
    - Utilise b2sum si disponible, sinon hashlib.blake2b()
    """
    try:
        # Lecture et normalisation du JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        normalized_json = json.dumps(data, sort_keys=True, separators=(",", ":"))

        # Essayer d'utiliser b2sum en subprocess
        result = subprocess.run(
            ["b2sum"],
            input=normalized_json,
            text=True,
            capture_output=True
        )

        if result.returncode == 0 and result.stdout:
            return result.stdout.split()[0]

        # fallback Python si b2sum échoue
        raise RuntimeError("b2sum failed")

    except Exception:
        # Fallback Python : calcul direct avec hashlib.blake2b
        blake = hashlib.blake2b()
        blake.update(normalized_json.encode("utf-8"))
        return blake.hexdigest()


@router.post("/hashcheck")
async def hashcheck(data: dict):
    """
    Compare le hash du datapack local (envoyé par le client)
    avec celui du serveur.
    """
    if not os.path.exists(SERVER_DATAPACK):
        raise HTTPException(status_code=500, detail="datapack.json missing")

    server_hash = compute_b2sum(SERVER_DATAPACK)
    client_hash = data.get("hash")

    return JSONResponse({
        "server_hash": server_hash,
        "is_same": (client_hash == server_hash)
    })
