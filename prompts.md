# AI-Prompts für das Statistik-Projekt

Dieses Dokument enthält eine kuratierte Liste von Prompts für **Claude Sonnet 4.5**, **ChatGPT 5.0** und **Gemini 3 Pro**. Diese Prompts sind auf die Analyse des NYC Taxi-Datensatzes im Ordner `notebooks/` zugeschnitten.

## Nutzung
Wähle das entsprechende Modell und kopiere den Prompt, um Unterstützung bei der Datenbereinigung, dem Feature Engineering, der Visualisierung oder der statistischen Analyse zu erhalten.

## Prompt-Tabelle

| Modell | Prompt |
| :--- | :--- |
| **Claude Sonnet 4.5** | Ich habe einen großen Datensatz von NYC Taxifahrten, der aufgrund von Speicherbeschränkungen in strikten Chunks geladen wird. Wie kann ich beim Verarbeiten der Datei effizient Zeilen herausfiltern, in denen fare_amount negativ ist oder passenger_count 0 ist, und das über alle Chunks hinweg? |
| **CHATGPT 5.0** | Schreibe eine Python-Funktion mit Pandas, um die Spalten tpep_pickup_datetime und tpep_dropoff_datetime in Datetime-Objekte umzuwandeln. Erstelle dann eine neue Spalte trip_duration in Minuten und filtere alle Fahrten heraus, die weniger als 1 Minute oder länger als 3 Stunden dauern. |
| **Gemini 3 Pro** | Erstelle unter Verwendung von Seaborn und Matplotlib einen Code-Schnipsel, um die Verteilung von trip_distance zu visualisieren. Das Diagramm sollte eine Kerndichteschätzung (KDE) enthalten und robust gegenüber extremen Ausreißern sein (z. B. Begrenzung der x-Achse auf das 99. Perzentil). |
| **Claude Sonnet 4.5** | Ich führe eine Korrelationsanalyse auf dem Taxidatensatz durch. Welche statistische Methode sollte ich verwenden, um den Zusammenhang zwischen trip_distance und tip_amount zu prüfen? Bitte gib mir den Python-Code zur Berechnung der Korrelationskoeffizienten nach Pearson und Spearman. |
| **CHATGPT 5.0** | Ich muss Ausreißer in der Spalte total_amount behandeln, bevor ich ein Modell trainiere. Bitte schreibe ein Skript, das Ausreißer mithilfe der Interquartilsabstandsmethode (IQR) erkennt und sie durch die oberen oder unteren Grenzwerte ersetzt (Capping/Flooring). |
| **Gemini 3 Pro** | Wie kann ich die Taxidaten nach payment_type gruppieren (z. B. Kreditkarte vs. Bar) und den Durchschnitt von tip_amount und total_amount berechnen? Bitte stelle Code bereit, um diese Unterschiede nebeneinander in einem Balkendiagramm mit Fehlerbalken zu visualisieren. |
| **Claude Sonnet 4.5** | Ich vermute, dass Verkehrsstaus die Effizienz der Taxis beeinflussen. Wie kann ich die Stunde des Tages aus tpep_pickup_datetime extrahieren und die durchschnittliche trip_speed (berechnet aus Distanz und Dauer) für jede Stunde des Tages plotten, um Stoßzeiten zu identifizieren? |
| **CHATGPT 5.0** | Formuliere eine Nullhypothese ($H_0$) und eine Alternativhypothese ($H_1$), um zu testen, ob der durchschnittliche Trinkgeldbetrag bei Kreditkartenzahlungen signifikant höher ist als bei Barzahlungen. Stelle dann den Code bereit, um einen unabhängigen t-Test (Welch-t-Test) durchzuführen und dies zu überprüfen. |
| **Gemini 3 Pro** | Erkläre das Konzept eines Konfidenzintervalls im Kontext der Schätzung des mittleren fare_amount aller Taxifahrten in NYC. Stelle einen Python-Code-Schnipsel bereit, um das 95%-Konfidenzintervall für den Mittelwert basierend auf meinen Stichprobendaten zu berechnen. |

---
*Erstellt basierend auf dem Inhalt der Projekt-Notebooks: 06.01.2026*
