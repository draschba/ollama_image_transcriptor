import os
import requests
import json
import base64
import shutil
import time
import csv

# --- KONFIGURATION ---
#MODEL = "qwen3.5:9b"  # Beispiel: Ein Modell, das Bilder versteht (Multimodal)
#MODEL = "qwen3-vl:8b"  # Beispiel: Ein Modell, das Bilder versteht (Multimodal)
MODEL = "ministral-3:14b"  # Beispiel: Ein Modell, das Bilder versteht (Multimodal)
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
*   Beschreibe den Hintergrund im Feld "Hintergrund, nur wenn dieser Besonderheiten aufweist" als String. Ignoriere schlichte, einfache weiße Hintergründe
*   Weitere Angaben als “Bemerkungen” als einzelnes Textfeld.
Lasse Felder zu denen keine Angaben gemacht wurden leer gebe aber die Feldnamen mit aus.
"""
#
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')

# Ordnerstruktur
INPUT_DIR = "Input"
OUTPUT_DIR = "Output"
ERROR_DIR = "Error"
LOG_FILE = "Ergebnis.csv"

# Verzeichnisse erstellen, falls sie nicht existieren
for folder in [INPUT_DIR, OUTPUT_DIR, ERROR_DIR]:
    os.makedirs(folder, exist_ok=True)

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_images():
    # Unterstützte Bildformate
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(valid_extensions)]
    
    total_start_time = time.time()
    
    # CSV Header schreiben (falls Datei neu)
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Dateiname', 'Status', 'Dauer_Sekunden', 'Fehlermeldung']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for filename in files:
            input_path = os.path.join(INPUT_DIR, filename)
            img_start_time = time.time()
            error_msg = ""
            status = "Erfolg"
            
            print(f"Verarbeite: {filename}...")
            
            try:
                # Bild in Base64 kodieren
                base64_img = image_to_base64(input_path)
                
                # Request Payload
                payload = {
                    "model": MODEL,
                    "prompt": PROMPT,
                    "images": [base64_img],
                    "stream": False
                }
                
                # API Call
                response = requests.post(OLLAMA_URL, json=payload, timeout=120)
                response.raise_for_status()
                
                result_text = response.json().get("response", "")
                
                # Erfolg: Verschieben in Output + Textdatei speichern
                txt_filename = os.path.splitext(filename)[0] + ".json"
                with open(os.path.join(OUTPUT_DIR, txt_filename), "w", encoding="utf-8") as f:
                    f.write(result_text)
                
                #shutil.move(input_path, os.path.join(OUTPUT_DIR, filename))
                
            except Exception as e:
                # Fehler: Verschieben in Error + Log-Datei speichern
                status = "Fehler"
                error_msg = str(e)
                #shutil.move(input_path, os.path.join(ERROR_DIR, filename))
                
                err_txt_name = os.path.splitext(filename)[0] + ".error.txt"
                with open(os.path.join(ERROR_DIR, err_txt_name), "w", encoding="utf-8") as f:
                    f.write(error_msg)
            
            img_duration = round(time.time() - img_start_time, 2)
            
            # In CSV loggen
            writer.writerow({
                'Dateiname': filename,
                'Status': status,
                'Dauer_Sekunden': img_duration,
                'Fehlermeldung': error_msg
            })
            
            print(f"Fertig: {filename} ({img_duration}s)")

    total_duration = round(time.time() - total_start_time, 2)
    print("-" * 30)
    print(f"Gesamtprozess beendet. Dauer: {total_duration}s")

if __name__ == "__main__":
    process_images()
