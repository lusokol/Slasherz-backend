from fastapi import Request, HTTPException
import os

ALLOWED_IPS = set(os.getenv("ALLOWED_IPS", "127.0.0.1").split(","))

def verify_ip_whitelist(request: Request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host

    if client_ip not in ALLOWED_IPS:
        raise HTTPException(
            status_code=403,
            # detail=f"Accès refusé"
            detail=f"Accès refusé pour l’adresse IP : {client_ip}"
        )
