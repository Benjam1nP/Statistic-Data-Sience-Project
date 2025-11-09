import pandas as pd

input_file = "data/Taxi_sample_1M.csv"
output_file = "data/Taxi_final_1M.csv"
chunksize = 100_000

first_chunk = True

for chunk in pd.read_csv(input_file, chunksize=chunksize, low_memory=False):
    # Datums-Spalten umwandeln
    chunk["tpep_pickup_datetime"] = pd.to_datetime(chunk["tpep_pickup_datetime"], errors="coerce")
    chunk["tpep_dropoff_datetime"] = pd.to_datetime(chunk["tpep_dropoff_datetime"], errors="coerce")

    # von Meilen in Kilometer
    if "trip_distance" in chunk.columns:
        chunk["trip_distance"] = chunk["trip_distance"] * 1.60934

    # Neue Spalte: trip_duration (in Minuten)
    chunk["trip_duration"] = (chunk["tpep_dropoff_datetime"] - chunk["tpep_pickup_datetime"]).dt.total_seconds() / 60

    # Neue Spalte: average_speed (in km/h)
    if "trip_distance" in chunk.columns:
        chunk["average_speed"] = (chunk["trip_distance"]) / (chunk["trip_duration"] / 60)
    else:
        chunk["average_speed"] = None  # falls Spalte fehlt

    # Neue Werte auf eine Nachkommastelle runden
    for col in ["trip_distance", "trip_duration", "average_speed"]:
        if col in chunk.columns:
            chunk[col] = chunk[col].round(1)

    # Ergebnis in neue CSV schreiben
    chunk.to_csv(output_file, mode="a", index=False, header=first_chunk)
    first_chunk = False
