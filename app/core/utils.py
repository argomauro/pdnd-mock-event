import json
import os
from fastapi import HTTPException
from fastapi.responses import JSONResponse, Response
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

def load_mock_data():
    """
    Carica i dati mock dal file JSON.
    """
    try:
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(current_dir,"app", "data", "eventi_mock.json")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel caricamento dei dati mock: {str(e)}")

def format_response(data, format_type=None):
    """
    Formatta la risposta in base al tipo richiesto (JSON o XML).
    
    Args:
        data: I dati da formattare
        format_type: Il formato richiesto ('json' o 'xml')
        
    Returns:
        La risposta formattata
    """
    if format_type == "xml":
        xml = dicttoxml(data, custom_root='response', attr_type=False)
        pretty_xml = parseString(xml).toprettyxml()
        return Response(content=pretty_xml, media_type="application/xml")
    
    # Default: JSON
    return data

def create_error_response(status_code: int, detail: str, type_url: str = None, title: str = None):
    """
    Crea una risposta di errore secondo RFC 7807.
    
    Args:
        status_code: Codice di stato HTTP
        detail: Dettaglio dell'errore
        type_url: URL che identifica il tipo di errore
        title: Titolo dell'errore
        
    Returns:
        JSONResponse con i dettagli dell'errore
    """
    if type_url is None:
        type_url = f"https://www.regione.it/errors/{status_code}"
    
    if title is None:
        titles = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            422: "Unprocessable Entity",
            500: "Internal Server Error"
        }
        title = titles.get(status_code, "Error")
    
    error_content = {
        "type": type_url,
        "title": title,
        "status": status_code,
        "detail": detail
    }
    
    return JSONResponse(
        status_code=status_code,
        content=error_content,
        media_type="application/problem+json"
    )
