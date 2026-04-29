# Prompt zur Transkription einer Sterbeanzeige:
---

Transkribiere folgende Sterbeanzeige wortgetreu als strukturierte Datenfelder im JSON Format:
*   den gesamten Text der Sterbeanzeige als Feld "Volltext".

Und zusätzlich, sofern die Daten angegeben sind: 
*   Vorname, Nachname und Geburtsname separiert,
*   Geburtsdatum und Geburtsort,
*   Sterbedatum und  Sterbeort,
*   Namen der Trauernden als Array von Strings,
*   Angaben zum Begräbnis, Beisetzung oder Trauerfeier im Feld "Beisetzung" als String,
*   Sofern Bildinformatinen in Form von Abbildungen enthalten sind beschreibe diese in einem Feld “Grafik” als String,
*   Beschreibe den Hintergrund im Feld "Hintergrund" als String, jedoch nur wenn dieser Besonderheiten aufweist. Ignoriere einfache weiße Hintergründe.
*   Weitere Angaben als “Bemerkungen” als einzelnes Textfeld.

Lasse Felder zu denen keine Angaben gemacht wurden leer gebe aber die Feldnamen mit aus.