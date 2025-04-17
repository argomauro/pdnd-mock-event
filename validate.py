"""
Script per testare l'avvio dell'applicazione e verificare che tutti i componenti funzionino correttamente.
"""
import os
import sys
import json
from pathlib import Path

# Verifica che tutti i file necessari esistano
def check_files():
    print("Verificando la presenza di tutti i file necessari...")
    
    required_files = [
        "app/main.py",
        "app/api/routes/eventi.py",
        "app/api/routes/auth.py",
        "app/api/schemas/models.py",
        "app/core/security.py",
        "app/core/utils.py",
        "app/data/eventi_mock.json",
        "tests/test_api.py",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = Path(__file__).parent / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ File mancanti:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("✅ Tutti i file necessari sono presenti")
    return True

# Verifica che i dati mock siano validi
def check_mock_data():
    print("Verificando i dati mock...")
    
    try:
        data_path = Path(__file__).parent / "app/data/eventi_mock.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not "eventi" in data or not "eventi_base" in data:
            print("❌ Struttura dati mock non valida")
            return False
        
        if len(data["eventi"]) == 0 or len(data["eventi_base"]) == 0:
            print("❌ Dati mock vuoti")
            return False
        
        print(f"✅ Dati mock validi: {len(data['eventi'])} eventi trovati")
        return True
    except Exception as e:
        print(f"❌ Errore nella verifica dei dati mock: {str(e)}")
        return False

# Verifica che l'applicazione possa essere importata
def check_app_import():
    print("Verificando l'importazione dell'applicazione...")
    
    try:
        sys.path.append(str(Path(__file__).parent))
        from app.main import app
        print("✅ Applicazione importata con successo")
        return True
    except Exception as e:
        print(f"❌ Errore nell'importazione dell'applicazione: {str(e)}")
        return False

# Esegui tutte le verifiche
def run_validation():
    print("=== VALIDAZIONE DELL'APPLICAZIONE ===\n")
    
    checks = [
        check_files(),
        check_mock_data(),
        check_app_import()
    ]
    
    if all(checks):
        print("\n✅ VALIDAZIONE COMPLETATA CON SUCCESSO")
        print("L'applicazione è pronta per essere avviata con:")
        print("  uvicorn app.main:app --reload")
        return True
    else:
        print("\n❌ VALIDAZIONE FALLITA")
        print("Correggere gli errori prima di avviare l'applicazione")
        return False

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    run_validation()
