from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from app.api.routes import eventi, auth
from app.core.security import verify_token
import json

# Creazione dell'applicazione FastAPI
app = FastAPI(
    title="Eventi API",
    description="""
    ## Servizio Eventi
    
    Questo servizio fornisce informazioni sugli eventi culturali e ricreativi che si svolgono in Basilicata.
    
    ### Funzionalità principali:
    
    * Consultazione di tutti gli eventi disponibili
    * Ricerca di eventi per intervallo di date
    * Verifica dello stato del servizio
    
    Il servizio è erogato da una Pubblica Amministrazione tramite GovWay ed è conforme alle linee guida PDND.
    Tutti gli endpoint sono protetti con autenticazione JWT Bearer Token come da specifiche PDND (RFC 8725).
    """,
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# Configurazione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestione degli errori
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_content = {
        "type": f"https://www.comune.regione.ce.it/errors/{exc.status_code}",
        "title": exc.detail,
        "status": exc.status_code,
        "detail": exc.detail
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_content,
        headers=exc.headers,
        media_type="application/problem+json"
    )

# Inclusione dei router
app.include_router(
    eventi.router,
    prefix="",
    dependencies=[Depends(verify_token)],
    tags=["eventi"]
)

app.include_router(
    auth.router,
    prefix="",
    tags=["auth"]
)

# Endpoint per la documentazione OpenAPI
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(
        title="Eventi API",
        version="1.0.0",
        description="API per la gestione degli eventi culturali e ricreativi",
        routes=app.routes,
    )

@app.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Eventi API - Documentazione Swagger"
    )

@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Eventi API - Documentazione ReDoc"
    )

# Endpoint radice
@app.get("/", include_in_schema=False)
async def root():
    return {
        "name": "Eventi API",
        "version": "1.0.0",
        "description": "API per la gestione degli eventi culturali e ricreativi",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    }
