import os
import shutil
import json
import time
import csv
import base64
import requests
from pathlib import Path
from datetime import datetime

# --- KONFIGURATION ---
# Pfad zum aktuellen Script-Ordner (Wurzel des Projekts)
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"
ERROR_DIR = BASE_DIR / "Error"
RESULT_CSV = BASE_DIR / "Ergebnis.csv"

# Konfiguration für den Ollama Server
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434/api/generate')

#
MODEL_NAME = "ministral-3:14b" # Beispiel: Llava, llava-phi, llama3.2-vision, etc.
#
PROMPT = """
Transkribiere folgende Sterbeanzeige wortgetreu als strukturierte Datenfelder im JSON Format:
*   den gesamten Text der Sterbeanzeige als Feld "Volltext".
Und zusätzlich, sofern die Daten angegeben sind:  
*   Vorname, Nachname und Geburtsname separiert,
*   Geburtsdatum und Geburtsort,
*   Sterbedatum und  Sterbeort,
*   Namen der Trauernden als Array von Strings,
*   Angaben zum Begräbnis, Beisetzung oder Trauerfeier im Feld "Beisetzung" als String,
*   Sofern Bildinformatinen in Form von Abbildungen enthalten sind beschreibe diese in einem Feld “Grafik” als String,
*   Beschreibe den Hintergrund im Feld "Hintergrund, nur wenn dieser Besonderheiten aufweist" als String,
*   Weitere Angaben als “Bemerkungen” als einzelnes Textfeld.
Lasse Felder zu denen keine Angaben gemacht wurden leer gebe aber die Feldnamen mit aus.
"""

# --- INITIALISIERUNG ---

def ensure_directories():
    """Stellt sicher, dass die Verzeichnisse existieren."""
    for dir_path in [INPUT_DIR, OUTPUT_DIR, ERROR_DIR]:
        dir_path.mkdir(exist_ok=True)
    if not RESULT_CSV.exists():
        RESULT_CSV.write_text("") # Erstes Mal initialisieren

def image_to_base64(image_path):
    """Konvertiert ein Bild in Base64-Code, da Ollama das für die API erwartet."""
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    return encoded_string

def process_image(file_path):
    """Verarbeitet ein einzelnes Bild und ruft Ollama auf."""
    filename = file_path.name
    status = "success"
    error_msg = ""
    response_data = None
    duration = 0

    try:
        # Berechnung der Startzeit
        start_time = time.time()
        
        # 1. Bild konvertieren (Base64)
        try:
            image_data = image_to_base64(file_path)
        except Exception as e:
            # Fehler beim Lesen der Bilddatei
            move_to_error(file_path, str(e))
            duration = time.time() - start_time
            log_result(filename, duration, status, response_data, error_msg)
            return

        # 2. Payload für Ollama vorbereiten
        payload = {
            "model": MODEL_NAME,
            "prompt": PROMPT,
            "images": [image_data],
            "stream": False, # Streaming deaktiviert
            "format": "json" # Antwort als JSON (optional, aber gut für CSV)
        }

        # 3. Request an Ollama
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        
        # Fehlerbehandlung im HTTP Status
        if response.status_code != 200:
            raise Exception(f"Ollama API Error: {response.status_code} - {response.text}")

        response_data = response.json()
        
        # 4. Berechnung der Endzeit
        duration = time.time() - start_time
        
        status = "success"
        error_msg = ""
        
        # 5. Erfolg: Datei nach Output verschieben
        output_path = OUTPUT_DIR / filename
        if output_path.exists():
            # Verhindern, dass der Name überschrieben wird (optional: Zufälliger Suffix)
            output_path = OUTPUT_DIR / f"{filename}.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        shutil.move(str(file_path), str(output_path))
        
        # 6. Antwort (JSON) speichern
        response_json_path = OUTPUT_DIR / f"{filename}.json"
        with open(response_json_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)
            
        # 7. CSV updaten
        log_result(filename, duration, status, response_data, error_msg)

        print(f"[OK] {filename} -> {output_path}")

    except Exception as e:
        # Fehlerbehandlung
        duration = time.time() - start_time
        status = "error"
        error_msg = str(e)
        
        print(f"[FAIL] {filename}: {e}")
        move_to_error(file_path, error_msg)
        log_result(filename, duration, status, None, error_msg)

def move_to_error(file_path, error_message):
    """Verschiebt die Bilddatei in den Error Ordner und schreibt eine Logdatei."""
    # Verschieben der Bilddatei in Error Ordner
    # Hinweis: Wir verwenden hier den Originalnamen, damit der Bildname im Error Ordner steht.
    error_file_path = ERROR_DIR / file_path.name
    shutil.move(str(file_path), str(error_file_path))
    
    # Erstellen der Fehlermeldungsdatei. 
    # Um Kollisionen mit der Bilddatei zu vermeiden, fügen wir einen Suffix hinzu.
    # Z.B. Bilddatei: image.jpg -> Fehlerdatei: image.jpg.err
    error_log_path = ERROR_DIR / f"{file_path.name}.err" 
    with open(error_log_path, "w", encoding="utf-8") as f:
        f.write(error_message)
        f.write("\n")

def log_result(filename, duration, status, response_data, error_msg):
    """Schreibt den Status in die CSV Datei."""
    # CSV Zeilenstruktur
    # Wir entziehen den Inhalt der Antwort (response_data['response']) aus dem JSON
    # um Formatierungsprobleme im CSV zu vermeiden (Zeilenumbrüche).
    
    with open(RESULT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # CSV Header nur beim ersten Aufruf? (Hier schreiben wir nur zur Datei, Header wird beim Start erstellt)
        # Um CSV sauber zu halten, können wir prüfen, ob es leer ist.
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            filename,
            f"{duration:.4f}", # Sekunden
            status,
            response_data.get('response', '') if status == "success" else error_msg
        ])

def print_summary():
    """Druckt eine Zusammenfassung der Ergebnisse."""
    if RESULT_CSV.exists():
        print("\n=== STATISTIK ===")
        with open(RESULT_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if rows:
                # Erste Zeile ist Header
                total = len(rows) - 1
                success = sum(1 for r in rows[1:] if r[3] == "success")
                errors = total - success
                print(f"Verarbeitete Dateien: {total}")
                print(f"Erfolgreich: {success}")
                print(f"Fehler: {errors}")
                print(f"CSV Datei: {RESULT_CSV}")
            else:
                print("Keine Ergebnisse gefunden.")
    else:
        print("Keine Ergebnisse vorhanden.")

# --- HAUPTROUTINE ---

def main():
    ensure_directories()
    
    if not RESULT_CSV.exists() or RESULT_CSV.stat().st_size == 0:
        # CSV Header schreiben, falls Datei leer
        with open(RESULT_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Datum", "Dateiname", "Dauer_Sekunden", "Status", "Antwort/Fehler"])
            print("CSV Datei initialisiert.")
        
    if not INPUT_DIR.exists() or not INPUT_DIR.iterdir():
        print("Keine Bilddateien im Input-Ordner gefunden.")
        print_summary()
        return

    files_listed = list(INPUT_DIR.iterdir())
    print(f"Initialisierung gestartet. {len(files_listed)} Dateien gefunden.")
    
    start_overall = time.time()
    
    for file_path in files_listed:
        if file_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            process_image(file_path)
            
    total_time = time.time() - start_overall
    
    print_summary()
    print(f"\nGesamtverarbeitungszeit: {total_time:.2f} Sekunden")

if __name__ == "__main__":
    main()