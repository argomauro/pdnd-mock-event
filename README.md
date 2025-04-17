# API Eventi - Servizio per la Pubblica Amministrazione

## Descrizione del Servizio

Questo progetto implementa un'applicazione backend RESTful con FastAPI che fornisce un servizio "Eventi" per una Pubblica Amministrazione. Il servizio è progettato per essere erogato tramite GovWay in ambiente di collaudo ed è compatibile con le linee guida PDND.

### Funzionalità principali

- Consultazione di tutti gli eventi disponibili
- Ricerca di eventi per intervallo di date
- Verifica dello stato del servizio
- Autenticazione tramite JWT Bearer Token conforme alle specifiche PDND (RFC 8725)

Il servizio è stato sviluppato utilizzando dati mock relativi a eventi che si svolgono in Basilicata, come festival, fiere ed eventi culturali.

## Struttura del Progetto

```
eventi_api/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py       # Endpoint per test autenticazione
│   │   │   └── eventi.py     # Endpoint principali del servizio
│   │   └── schemas/
│   │       └── models.py     # Modelli Pydantic
│   ├── core/
│   │   ├── security.py       # Gestione autenticazione JWT
│   │   └── utils.py          # Funzioni di utilità
│   ├── data/
│   │   └── eventi_mock.json  # Dati mock degli eventi
│   └── main.py               # Applicazione principale FastAPI
└── tests/
    └── test_api.py           # Test unitari
```

## Requisiti

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Python-jose (per JWT)
- Pytest (per i test)
- Dicttoxml (per il supporto XML)

## Installazione

1. Clonare il repository:

```bash
git clone https://github.com/tuoente/eventi-api.git
cd eventi-api
```

2. Creare un ambiente virtuale e attivarlo:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows
```

3. Installare le dipendenze:

```bash
pip install fastapi uvicorn pydantic python-jose pytest dicttoxml httpx
```

## Test di validazione del progetto

Per verificare la stabilità del progetto. Lo script verifica:
- La presenza di tutti i file
- La presenza di tutti i dati mock
- La verifica della struttura del progetto


## Avvio Locale

Per avviare l'applicazione in locale:

```bash
cd eventi_api
uvicorn app.main:app --reload
```

L'applicazione sarà disponibile all'indirizzo: http://127.0.0.1:8000

## Documentazione API

La documentazione interattiva è disponibile ai seguenti endpoint:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## Endpoint Pubblicati

- `GET /status`: Restituisce lo stato del servizio
- `GET /eventi`: Restituisce la lista di tutti gli eventi
- `GET /eventi/date-search`: Ricerca eventi per intervallo di date
- `GET /auth-test`: Endpoint di test per l'autenticazione JWT

Tutti gli endpoint supportano il parametro `format=json|xml` per specificare il formato della risposta.

## Test JWT

Per testare l'autenticazione JWT, è possibile utilizzare il seguente comando curl:

```bash
# Generare un token di test (in un'applicazione reale questo verrebbe fornito da PDND)
TOKEN=$(python -c "from app.core.security import create_test_token; from datetime import datetime, timedelta; print(create_test_token({'sub': 'test_user', 'iss': 'PDND', 'exp': datetime.utcnow() + timedelta(minutes=30)}))")

# Utilizzare il token per accedere all'endpoint di test
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/auth-test
```

## Esecuzione dei Test

Per eseguire i test unitari:

```bash
cd eventi_api
pytest
```

I test verificano:
- Il funzionamento di tutti gli endpoint
- La corretta gestione dei formati JSON e XML
- Il comportamento in caso di JWT mancante, malformato o scaduto
- I casi limite e gli errori

## Integrazione con GovWay e PDND

L'API è progettata per essere registrata su GovWay come servizio erogato in modalità API Gateway. L'endpoint definitivo sarà simile a:

```
https://govway.publisys.it/govway/Regione/Eventi/v1
```

Il codice è pronto per la futura registrazione su PDND e pubblicazione su catalogo API.

## Note sulla Sicurezza

In ambiente di produzione:
- Le chiavi JWT dovrebbero essere gestite in modo sicuro (non hardcoded)
- Le configurazioni sensibili dovrebbero essere caricate da variabili d'ambiente
- Il servizio dovrebbe essere esposto solo tramite HTTPS

## Licenza

Questo progetto è rilasciato sotto licenza MIT.
