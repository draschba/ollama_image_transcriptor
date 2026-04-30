import os
import time
import shutil
import requests
import base64
import csv

# ==============================
# Konfiguration
# ==============================
INPUT_DIR = "Input"
OUTPUT_DIR = "Output"
ERROR_DIR = "Error"

OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434/api/generate')

MODEL = "ministral-3:14b"
#MODEL = "gemma4:latest"
#MODEL = "qwen3-vl:8b"

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
*   Beschreibe den Hintergrund im Feld "Hintergrund" als String, jedoch nur wenn dieser Besonderheiten aufweist. Ignoriere einfache einfarbige Hintergründe.
*   Weitere Angaben als “Bemerkungen” als einzelnes Textfeld.

Lasse Felder zu denen keine Angaben gemacht wurden leer, gebe aber die Feldnamen mit aus.
"""

# Unterstützte Bildformate
VALID_EXTENSIONS = (".png", ".jpg", ".jpeg")


# ==============================
# Hilfsfunktionen
# ==============================
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def send_request(image_path):
    image_base64 = encode_image_to_base64(image_path)

    payload = {
        "model": MODEL,
        "prompt": PROMPT,
        "images": [image_base64],
        "stream": False,
        "format" : 'json'
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        raise Exception(f"HTTP Fehler: {response.status_code} - {response.text}")

    return response.json()


def save_text_file(path, content):
    #content = content.replace("```json", "")
    #content = content.replace("```", "")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ==============================
# Hauptlogik
# ==============================
def main():
    start_total = time.time()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(ERROR_DIR, exist_ok=True)

    image_files = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(VALID_EXTENSIONS)
    ]

    csv_path = "Ergebnis.csv"

    with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        writer.writerow(["Dateiname", "Status", "Dauer (Sekunden)", "Fehlermeldung"])

        for image_name in image_files:
            input_path = os.path.join(INPUT_DIR, image_name)
            base_name, _ = os.path.splitext(image_name)

            print(f"Verarbeite: {image_name}")
            start_time = time.time()

            try:
                result = send_request(input_path)

                duration = time.time() - start_time

                response_text = result.get("response", "")

                # Zielpfade
                output_image_path = os.path.join(OUTPUT_DIR, image_name)
                output_text_path = os.path.join(OUTPUT_DIR, base_name + ".json")

                # Bild verschieben
                #shutil.move(input_path, output_image_path)

                # Text speichern
                save_text_file(output_text_path, response_text)

                print(f"Fertig: {image_name} ({duration:.2f} Sekunden)")

                writer.writerow([image_name, "OK", f"{duration:.2f}", ""])

            except Exception as e:
                duration = time.time() - start_time
                error_msg = str(e)

                error_image_path = os.path.join(ERROR_DIR, image_name)
                error_text_path = os.path.join(ERROR_DIR, base_name + ".txt")

                # Bild verschieben
                #shutil.move(input_path, error_image_path)

                # Fehler speichern
                save_text_file(error_text_path, error_msg)

                print(f"Fehler bei: {image_name} ({duration:.2f} Sekunden)")
                print(f"Grund: {error_msg}")

                writer.writerow([image_name, "ERROR", f"{duration:.2f}", error_msg])

    total_duration = time.time() - start_total
    print(f"\nGesamtdauer: {total_duration:.2f} Sekunden")


# ==============================
# Startpunkt
# ==============================
if __name__ == "__main__":
    main()
