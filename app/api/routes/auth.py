from fastapi import APIRouter, Depends
from app.core.security import verify_token

router = APIRouter()

@router.get("/auth-test", tags=["auth"])
async def auth_test(payload: dict = Depends(verify_token)):
    """
    Endpoint di test per l'autenticazione JWT.
    Questo endpoint è protetto e richiede un token JWT valido.
    
    Returns:
        Un messaggio di successo con i dettagli del payload del token
    """
    return {
        "message": "Autenticazione riuscita",
        "payload": payload
    }
