from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class Status(BaseModel):
    """
    Modello per lo stato del servizio.
    """
    status: str


class EventoBase(BaseModel):
    """
    Modello base per un evento.
    """
    id: int = Field(..., description="ID oggetto")
    title: str = Field(..., description="Titolo modulo")
    description: str = Field(..., description="Descrizione modulo")
    url: str = Field(..., description="Indirizzo del modulo")
    start_event_date: date = Field(..., description="Datetime inizio evento")
    end_event_date: date = Field(..., description="Datetime completa fine evento")
    event_location: str = Field(..., description="Luogo evento")


class Eventi(BaseModel):
    """
    Modello per la lista di eventi.
    """
    articles: List[EventoBase]


class Evento(BaseModel):
    """
    Modello dettagliato per un singolo evento.
    """
    id: int
    nome: str
    descrizione: str
    dataInizio: datetime
    dataFine: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "nome": "Festival del Cinema di Matera",
                "descrizione": "Festival internazionale del cinema che si svolge nella città dei Sassi",
                "dataInizio": "2025-06-15T18:00:00",
                "dataFine": "2025-06-22T23:00:00"
            }
        }


class ErrorResponse(BaseModel):
    """
    Modello per le risposte di errore secondo RFC 7807.
    """
    type: str
    title: str
    status: int
    detail: str
    instance: Optional[str] = None
