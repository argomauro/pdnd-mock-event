from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Configurazione per la sicurezza JWT
# In un ambiente di produzione, queste informazioni dovrebbero essere in un file di configurazione
# o variabili d'ambiente

# Supporto per entrambi gli algoritmi
ALGORITHM_RS256 = "RS256"
ALGORITHM_HS256 = "HS256"

# Chiave pubblica per RS256 (originale)
JWT_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnzyis1ZjfNB0bBgKFMSv
vkTtwlvBsaJq7S5wA+kzeVOVpVWwkWdVha4s38XM/pa/yr47av7+z3VTmvDRyAHc
aT92whREFpLv9cj5lTeJSibyr/Mrm/YtjCZVWgaOYIhwrXwKLqPr/11inWsAkfIy
tvHWTxZYEcXLgAXFuUuaS3uF9gEiNQwzGTU1v0FqkqTBr4B8nW3HCN47XUu0t8Y0
e+lf4s4OxQawWD79J9/5d3Ry0vbV3Am1FtGJiJvOwRsIfVChDpYStTcHTCMqtvWb
V6L11BWkpzGXSW4Hv43qa+GSYOD2QU68Mb59oSk2OB+BtOLpJofmbGEGgvmwyCI9
MwIDAQAB
-----END PUBLIC KEY-----
"""

# Chiave segreta per HS256 (nuova)
JWT_SECRET_KEY = "chiave_segreta_per_test_non_usare_in_produzione_12345"

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifica il token JWT.
    
    Supporta sia token firmati con RS256 (originale) che HS256 (per test).
    
    Args:
        credentials: Credenziali di autorizzazione HTTP
        
    Returns:
        Il payload del token se valido
        
    Raises:
        HTTPException: Se il token non è valido o è scaduto
    """
    try:
        token = credentials.credentials
        
        # Prima prova a decodificare con HS256 (per i token di test)
        try:
            payload = jwt.decode(
                token, 
                JWT_SECRET_KEY, 
                algorithms=[ALGORITHM_HS256],
                options={"verify_signature": True}
            )
        except JWTError:
            # Se fallisce, prova con RS256 (per i token di produzione)
            payload = jwt.decode(
                token, 
                JWT_PUBLIC_KEY, 
                algorithms=[ALGORITHM_RS256],
                options={"verify_signature": True}
            )
        
        # Verifica scadenza token
        if "exp" in payload and datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token scaduto",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token JWT non valido",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Funzione per generare un token di test con HS256 (per scopi di sviluppo)
def create_test_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT di test usando HS256.
    Nota: Questa funzione è solo per scopi di test e non dovrebbe essere usata in produzione.
    In produzione, i token verrebbero generati da PDND.
    
    Args:
        data: Dati da includere nel token
        expires_delta: Tempo di scadenza del token
        
    Returns:
        Token JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    
    # Utilizziamo HS256 con una chiave segreta semplice per i test
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM_HS256)
    return encoded_jwt

# La funzione originale per generare token RS256 è mantenuta per compatibilità
def create_rs256_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT usando RS256.
    Nota: Questa funzione è mantenuta per compatibilità con il codice esistente.
    
    Args:
        data: Dati da includere nel token
        expires_delta: Tempo di scadenza del token
        
    Returns:
        Token JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    
    # Chiave privata per RS256 (originale)
    test_private_key = """
    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCfPKKzVmN80HRs
    GAoUxK++RO3CW8GxomrtLnAD6TN5U5WlVbCRZ1WFrizfxcz+lr/Kvjtq/v7PdVOa
    8NHIAdxpP3bCFEQWku/1yPmVN4lKJvKv8yub9i2MJlVaBo5giHCtfAouo+v/XWKd
    awCR8jK28dZPFlgRxcuABcW5S5pLe4X2ASI1DDMZNTW/QWqSpMGvgHydbccI3jtd
    S7S3xjR76V/izg7FBrBYPv0n3/l3dHLS9tXcCbUW0YmIm87BGwh9UKEOlhK1NwdM
    Iyq29ZtXovXUFaSnMZdJbge/jepr4ZJg4PZBTrwxvn2hKTY4H4G04ukmh+ZsYQaC
    +bDIIj0zAgMBAAECggEAKIBGrbNxFR5XKS8Lcj2aMhQmS7wDrPt5ZyEyFDo7g1Rd
    5TP07wVONUO9UTVRzUmHo7JJ4JxHzjQ0WjdcJKLZWh6iUY+OXxXM/zCVrYYJvnYT
    JmQ9c/XOiNWwNpEpHLJc3suAn7dDezopGwDN2QKpFnCAdEJJOqohbqFoyGWtqxYa
    YTTBsABnpfQFwZNfDqKrYtJ8bpKdUaF5ggIrAZ9rcRn3i0jf3+0oKJJWrSPoEjQ8
    F7wui+S7oBmP8WZuYNu0PYXv5prH4Xj5CwAJWzRIUJE+KHmj5/L6Orx6GAwyDYFx
    LDpFmLYBaD1q/VsMvivT4pDLLnbGZzMpCxfkBM+RoQKBgQDPcUUj20nNXKqELkm5
    9+1RSKNHlnIvkybfAXBKK3D2FzFUpyIHVGJHzXtNYZGKGv6OlUgTUJ/ZB8VB7uZP
    TWLYHZm7vsFOzVjU/hEFTGRtLhYCjf4S6MBUxLXQ3yUGmZhfKHNhOzagYBAikFQh
    IKmKYGbfeRY19B5Y9A5Z7e97YQKBgQDEQwTxUiujNMEhhh+JU/QwVSs08Vdgqjav
    Af9oi1rICx8KvNhcC3+Dr5d8jOr6fFGXA9lELsYQVLX8tOUn6aOUMbYVDZzHqGdY
    zJLxicHxqGnxW+/6YYGvV0HnmHxQRKP25PSRwRqY5+FLDWsuTYjrWEALsKSQENp9
    OZuEJsYwEwKBgQCUWdJU4ZzDQlSqIvnFQ2KEjpCFEQRXE9MvOYy0tVhLrjYEAbfM
    /HwY/l1+3Pev4JXtXFDM+GXZe8TVrsA7kZ1XLGZPwXHogMvUENVYVYITf+8m6DJY
    j4aL9SB4Tsg4+aBPXYXhn7dGqVUbeoKfVWvz/0wNhGnkQnwUlcOWyGdSAQKBgD+F
    rtLYQQyfFbUNEomzxbBfVnwTjJbwJ0wCx6xkGQzPWFXGTr2IZBCzQgm3HQqUVsqA
    h/d6Q7aTQNLYQ8X6K5PBxHHwCrSzBuasCo2wMvGqYsC1ZtlMHMPfk8KWnXJB0c8F
    +wqXFLQWHzCIz8XHRqDvfDLzpx4CkBFOtPEYih5LAoGAZmRqyd0+pYN9iezfBZkj
    PkKAPzA5wCerNESsS4Vt+P1uwGxziKF5DvOW8KZwZpEr3HTMH2NZMmEwuQeAGGLq
    +aGXAhi4A7hGHZkCnf8AEHsXuT9+HQQnVzsJqXXeYbGxYLcXXJRxDIwGzQo2N7Qb
    BYFdlps792OQC8xJXXYMvK0=
    -----END PRIVATE KEY-----
    """
    
    encoded_jwt = jwt.encode(to_encode, test_private_key, algorithm=ALGORITHM_RS256)
    return encoded_jwt