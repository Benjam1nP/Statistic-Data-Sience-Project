** Generieren des benötigten Datensatzes **
1.  lade den Datensatz als csv file in das Projekt (namen: 2023_Yellow_Taxi_Trip_Data.csv)

2.  führe folgendes file aus --> delete_columns.py 
    es löscht alle Spalten die für unser Projekt nicht von belangen sind

3.  führe danachfolgendes file aus --> change_to_datetime.py (braucht 30min)
    es wechselt die Angabe von abfahrt und ankunft in datetime

4.  Nach diesen Schritten sollte Taxi_final.csv generiert worden sein.

5.  führe jetzt get_representative_sample.py aus
    es generiert eine ausführbare Menge an Daten, welche aus den geshuffelten Ursprungsdaten ausgewählt werden,
    diese solltne repräsentativ sein.