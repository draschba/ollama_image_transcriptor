Version 1: Gemini
Erstelle Python Programm mit folgender Funktionalität:
Im Projketordner git es drei Verzeichnisse: Input, Output und Error. 
In dem Iportordner liegen mehrere Bilddateien.  
Das Pythonprogramm soll nacheinander alle Bilddateien lesen. 
Die Daten enes Bildes werden eingelesen und es wird ein REST-Request an einen lokal laufenden Ollama Server formuiert werden.
Das Modell und der Prompt werden im Python-Programm durch Variablen definiert. 
Das Streaming von Tokens soll im Request deaktiviert sein. 
Das Bild wird mit dem Request an den Ollama Service gesendet. 
Das Textergebnis wird entgegengenommen. 
Im Falle einer fehlerfreien Verabreitung des Bildes wird das Bild zusammen mit einer Textdatei der Response im Outputordner verschoben. Im Faller eines Fehlers wird das Bild in den Error verschobeen und die Fehlermeldung mit dem selben Namen wie die Bilddatei im Error Ordner verschoben. Ollama bearbeitet immer nur einen Bildrequest zur Zeit. Messe die Zeit für den Gesamtduchgang und die Bearbeitetung  jedes einzelnen Bildes. 
Notiere die Informationen in einer Datei Ergebnis.csv tabellarisch im Projektordner.




Version 2:  (qwen3.5:14b)
Erstelle ein Python Programm mit folgender Funktionalität:  
Im Projketordner git es drei Verzeichnisse: Input, Output und Error.  
In dem Importordner liegen mehrere Bilddateien.  
Das Pythonprogramm soll nacheinander alle Bilddateien lesen.  
Die Daten enes Bildes werden eingelesen und es wird ein REST-Request an einen lokal laufenden Ollama Server formuiert werden.  Als Modell soll "mnistral-3:12b" vorgewählt sein.
Das Modell und der Prompt werden im Python-Programm durch Variablen definiert.  
Das Streaming von Tokens soll im Request deaktiviert sein.  
Das Bild wird mit dem Request an den Ollama Service gesendet.  
Die Response wird entgegengenommen. 
Im Falle einer fehlerfreien Verabreitung des Bildes wird das Bild zusammen mit einer Textdatei der Response in den Outputordner verschoben. 
Im Faller eines Fehlers wird das Bild in den Error verschobeen und die Fehlermeldung mit dem selben Namen wie die Bilddatei im Error Ordner verschoben. Ollama bearbeitet immer nur einen Bildrequest zur Zeit. Messe die Zeit für den Gesamtduchgang und die Bearbeitetung jedes einzelnen Bildes.  Protokoliere auf der Konsole das gerade verarbeitete Bild und gebe die Dauer der Verarbeitug an. 
Notiere die Informationen in einer Datei Ergebnis.csv tabellarisch im Projektordner.


Version 3: Copilot
Erstelle ein Python Programm mit folgender Funktionalität:  
Im Projketordner git es drei Verzeichnisse: Input, Output und Error.  
In dem Importordner liegen mehrere Bilddateien.  
Das Pythonprogramm soll nacheinander alle Bilddateien lesen.  
Die Daten enes Bildes werden eingelesen und es wird ein REST-Request an einen lokal laufenden Ollama Server formuiert werden.  Als Modell soll "ministral-3:14b" vorgewählt sein.
Das Modell und der Prompt werden im Python-Programm durch Variablen definiert.  
Das Streaming von Tokens soll im Request deaktiviert sein.  
Das Bild wird mit dem Request an den Ollama Service gesendet.  
Die Response wird entgegengenommen. 
Im Falle einer fehlerfreien Verabreitung des Bildes wird das Bild zusammen mit einer Textdatei der Response in den Outputordner verschoben. 
Im Faller eines Fehlers wird das Bild in den Error verschobeen und die Fehlermeldung mit dem selben Namen wie die Bilddatei im Error Ordner verschoben. Ollama bearbeitet immer nur einen Bildrequest zur Zeit. Messe die Zeit für den Gesamtduchgang und die Bearbeitetung jedes einzelnen Bildes.  Protokoliere auf der Konsole das gerade verarbeitete Bild und gebe die Dauer der Verarbeitug an. 
Notiere die Informationen in einer Excel-Datei Ergebniss.xlsx tabellarisch im Projektordner.
