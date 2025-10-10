from fastapi import FastAPI, Depends
from app.routes import cards, datapack
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

app = FastAPI(title="Slasherz Backend")

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
