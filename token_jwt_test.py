"""
Script per generare un token JWT di test per l'API Eventi.
Questo script utilizza l'algoritmo HS256 con una chiave segreta semplice.
"""
from datetime import datetime, timedelta
import json
from jose import jwt
import os

# Configurazione
ALGORITHM = "HS256"
SECRET_KEY = "chiave_segreta_per_test_non_usare_in_produzione_12345"

def create_test_token(data, expires_delta=None):
    """
    Crea un token JWT di test.
    
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
    
    # Correggiamo i timestamp per evitare problemi di validità
    if "iat" in to_encode:
        # Impostiamo issued at a 5 minuti fa per evitare problemi di sincronizzazione
        to_encode["iat"] = (datetime.utcnow() - timedelta(minutes=5)).timestamp()
    
    if "nbf" in to_encode:
        # Impostiamo not before a 5 minuti fa per evitare problemi di sincronizzazione
        to_encode["nbf"] = (datetime.utcnow() - timedelta(minutes=5)).timestamp()
    
    # Utilizziamo HS256 con una chiave segreta semplice per i test
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Modifica temporaneamente la sezione __main__ dello script di generazione
if __name__ == "__main__":
    token_data = {"sub": "test"}
    token = create_test_token(token_data, expires_delta=timedelta(minutes=100))
    print("\nToken JWT generato (semplice):")
    print(token)
    print("\nQuesto token scadrà tra 1 ora.")
    print("Puoi utilizzarlo per testare l'API Eventi in ambiente di sviluppo.")
    
    # Salva il token in un file per riferimento futuro
    with open("jwt_token.txt", "w") as f:
        f.write(token)
    print(f"\nIl token è stato salvato nel file: {os.path.abspath('jwt_token.txt')}")    

