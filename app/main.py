from fastapi import FastAPI, Depends, HTTPException
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from app.routes import cards, datapack
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.utils.ip_check import verify_ip_whitelist
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

app = FastAPI(
    title="Slasherz Backend",
    version="0.1"
)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

app.mount("/api/images", StaticFiles(directory="app/data/images"), name="images")

app.include_router(cards.router)
app.include_router(datapack.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de Slasherz !"}

@app.get("/db-test")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT version();"))
    version = result.fetchone()
    return {"postgres_version": version[0]}

# === ROUTE DE L’ADMIN PAGE === #
@app.get("/api/admin", response_class=HTMLResponse, dependencies=[Depends(verify_ip_whitelist)])
async def serve_admin_page():
    """
    Sert la page d’administration si l’IP est autorisée.
    """
    admin_page = os.path.join("app", "static", "admin", "index.html")
    if not os.path.exists(admin_page):
        raise HTTPException(status_code=404, detail="Fichier admin introuvable")
    return FileResponse(admin_page, media_type="text/html")
