# Ollama Image Transcriptor

Dieses Projekt wurde entwickelt, um eine große Menge an Sterbeanzeigen aus Zeitungsanzeigen für die genealogische Forschung automatisiert zu transkribieren.

![Logo](logo.png)

Das Programm selbst wurde mit Hilfe von verschiedenen KI-Chatbots entwickelt und anschließend im Detail manuell minimal angepasst. Den Prompt für die Programmgenerierung findet man unter [generate_program.md](prompts/generate_program.md).

## Es erfüllt dabei folgende Grundfunktionen:

1. Der Ordner **Input** wird nach Bilddateien im jpg- oder png-Format durchsucht.
2. Für jedes Bild wird ein REST-API-Post-Request als Payload zusammengestellt. Die Bilddaten werden dafür base64-encoded.
3. Der Text für den Prompt ist im Programm als Variable hinterlegt.
4. Der REST-Request wird an einen Ollama-Server übermittelt.
5. Die Response wird als JSON-Struktur entgegengenommen. Das Bild und die JSON-Daten aus der Response werden im Ordner **Output** abgelegt.
6. Für jedes einzelne Bild wird die Dauer der Verarbeitung gemessen. Und die Gesamtdauer der Verarbeitung ermittelt.
7. Der Status sowie die Dauer der Verarbeitung des Bildes wird zusätzlich in einer CSV-Datei im Projektordner erfasst.


## Voraussetzungen

Das Programm wurde unter Ubuntu Linux 22.04 LTS entwickelt. Man benötigt eine aktuelle Python Umgebung mit **pip** und virtuellem Environment **venv**. Diese kann mit

```bash
sudo apt install python3-pip python3-venv
```

nachinstallieren sofern sie noch nicht vorhanden ist.

### Aktivieren der virtuellen Python Umgebung

Es gehört zur guten handwerklichen Praxis ein virtuelles Environment für Python anzulegen. Dort hinein werden die zusätzlich erforderlichen Python Pakate für das Projekt installiert. 

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```



