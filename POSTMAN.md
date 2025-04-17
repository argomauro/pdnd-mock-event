# Istruzioni per l'utilizzo della Collection Postman per API Eventi

Questa guida ti aiuterà a importare e utilizzare la collection Postman per testare l'API Eventi.

## Prerequisiti

- [Postman](https://www.postman.com/downloads/) installato sul tuo computer
- API Eventi in esecuzione (localmente o in ambiente di test)

## Importazione della Collection e dell'Environment

1. Estrai il file `eventi_api_postman.zip`
2. Apri Postman
3. Clicca sul pulsante "Import" in alto a sinistra
4. Trascina entrambi i file estratti (`eventi_api_postman_collection_with_tests.json` e `eventi_api_environment.json`) nella finestra di importazione o clicca su "Upload Files" e selezionali
5. Clicca su "Import"

## Configurazione dell'Environment

1. In alto a destra, clicca sul menu a tendina degli environment e seleziona "API Eventi - Ambiente"
2. Verifica che la variabile `base_url` sia impostata correttamente:
   - Per test locale: `http://localhost:8000`
   - Per ambiente di test: URL fornito dall'amministratore
3. La variabile `jwt_token` contiene già un token di test valido per l'ambiente di sviluppo

## Esecuzione delle Richieste

La collection è organizzata in cartelle per facilitare i test:

### Cartella "Autenticazione"
- **Test Autenticazione**: Verifica che l'autenticazione JWT funzioni correttamente

### Cartella "Status"
- **Stato del Servizio (JSON)**: Verifica lo stato del servizio in formato JSON
- **Stato del Servizio (XML)**: Verifica lo stato del servizio in formato XML

### Cartella "Eventi"
- **Lista Eventi (JSON)**: Ottiene la lista completa degli eventi in formato JSON
- **Lista Eventi (XML)**: Ottiene la lista completa degli eventi in formato XML
- **Ricerca Eventi per Data (JSON)**: Cerca eventi in un intervallo di date in formato JSON
- **Ricerca Eventi per Data (XML)**: Cerca eventi in un intervallo di date in formato XML
- **Ricerca Eventi con Date Invalide**: Testa la gestione degli errori con date invalide

### Cartella "Errori"
- **Richiesta senza Token**: Testa la risposta quando il token JWT è mancante
- **Richiesta con Token Malformato**: Testa la risposta quando il token JWT è malformato
- **Richiesta con Token Scaduto**: Testa la risposta quando il token JWT è scaduto

## Esecuzione dei Test Automatici

Ogni richiesta include test automatici che verificano:
- Lo stato della risposta HTTP
- Il Content-Type corretto
- La struttura e il contenuto della risposta

Per eseguire tutti i test:
1. Clicca con il tasto destro sulla cartella principale "API Eventi"
2. Seleziona "Run collection"
3. Nella finestra di dialogo, clicca su "Run API Eventi"
4. I risultati dei test verranno visualizzati nella scheda "Test Results"

## Generazione di un Nuovo Token JWT (per ambiente di sviluppo)

Se hai bisogno di generare un nuovo token JWT per i test, puoi utilizzare il seguente script Python:

```python
from app.core.security import create_test_token
from datetime import datetime, timedelta

token_data = {
    "sub": "test_user",
    "iss": "PDND",
    "aud": "https://govway.publisys.it/govway/Regone/Eventi/v1",
    "iat": datetime.utcnow(),
    "nbf": datetime.utcnow(),
    "jti": "123456789",
    "client_id": "test_client",
    "purpose": "test"
}

token = create_test_token(token_data, expires_delta=timedelta(hours=1))
print(token)
```

Esegui questo script dalla directory principale del progetto e aggiorna la variabile `jwt_token` nell'environment di Postman con il nuovo token generato.

## Note Importanti

- In ambiente di produzione, i token JWT verranno forniti da PDND e non generati localmente
- Assicurati che l'API sia in esecuzione prima di eseguire i test
- Se l'URL dell'API cambia, aggiorna la variabile `base_url` nell'environment
