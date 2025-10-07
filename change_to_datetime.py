import pandas as pd

input_file = "data/Taxi_Data_improved.csv"
output_file = "data/Taxi_final.csv"
chunksize = 2_000_000

first_chunk = True

for chunk in pd.read_csv(input_file, chunksize=chunksize, low_memory=False):
    # Spalten in echtes datetime64 umwandeln
    chunk["tpep_pickup_datetime"] = pd.to_datetime(chunk["tpep_pickup_datetime"], errors="coerce")
    chunk["tpep_dropoff_datetime"] = pd.to_datetime(chunk["tpep_dropoff_datetime"], errors="coerce")

    # ins neue CSV schreiben
    chunk.to_csv(output_file, mode="a", index=False, header=first_chunk)
    first_chunk = False
