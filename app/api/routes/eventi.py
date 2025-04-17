from fastapi import APIRouter, Query, HTTPException, Path, Depends
from typing import List, Optional, Union
from datetime import date
from app.api.schemas.models import Status, Eventi, Evento
from app.core.utils import load_mock_data, format_response

router = APIRouter()

@router.get("/status", response_model=Status, tags=["status"])
async def get_status(format: Optional[str] = Query(None, enum=["json", "xml"])):
    """
    Restituisce lo stato del servizio.
    
    - **format**: Formato della risposta (json o xml)
    """
    status_data = {"status": "online"}
    return format_response(status_data, format)


@router.get("/eventi", response_model=Eventi, tags=["eventi"])
async def get_eventi(format: Optional[str] = Query(None, enum=["json", "xml"])):
    """
    Restituisce la lista di tutti gli eventi.
    
    - **format**: Formato della risposta (json o xml)
    """
    mock_data = load_mock_data()
    eventi_data = {"articles": mock_data.get("eventi_base", [])}
    return format_response(eventi_data, format)


@router.get("/eventi/date-search", response_model=List[Evento], tags=["eventi"])
async def search_eventi_by_date(
    start_date: date = Query(..., description="Data di inizio intervallo (formato: YYYY-MM-DD)"),
    end_date: date = Query(..., description="Data di fine intervallo (formato: YYYY-MM-DD)"),
    format: Optional[str] = Query(None, enum=["json", "xml"])
):
    """
    Ricerca eventi per intervallo di date.
    
    - **start_date**: Data di inizio intervallo (formato: YYYY-MM-DD)
    - **end_date**: Data di fine intervallo (formato: YYYY-MM-DD)
    - **format**: Formato della risposta (json o xml)
    """
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="La data di inizio deve essere precedente alla data di fine")
    
    mock_data = load_mock_data()
    eventi = mock_data.get("eventi", [])
    
    # Filtra gli eventi in base all'intervallo di date
    filtered_events = []
    for evento in eventi:
        event_start = date.fromisoformat(evento["dataInizio"].split("T")[0])
        if start_date <= event_start <= end_date:
            filtered_events.append(evento)
    
    return format_response(filtered_events, format)
