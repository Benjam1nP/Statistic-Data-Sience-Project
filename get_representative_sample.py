import pandas as pd
import random

input_file = "data/Taxi_final.csv"
output_file = "data/Taxi_sample_6M.csv"
target_rows = 6_000_000
chunksize = 5_000_000

print("Starte chunkweises Zufallssampling...")

# Gesamtzahl Zeilen zählen (ohne Header)
with open(input_file, "r", encoding="utf-8") as f:
    total_lines = sum(1 for _ in f) - 1  # minus Header

print(f"Gesamtzeilen (ohne Header): {total_lines:,}")

# Anteil berechnen, den wir insgesamt behalten wollen
sample_frac = target_rows / total_lines
print(f"Zufälliger Anteil pro Chunk: {sample_frac:.4f}")

sample_list = []
total_rows = 0

# Chunks einlesen und zufällig aus jedem ein Teil-Sample ziehen
for i, chunk in enumerate(pd.read_csv(input_file, chunksize=chunksize)):
    # ziehe denselben relativen Anteil aus diesem Chunk
    sample = chunk.sample(frac=sample_frac, random_state=random.randint(0, 5_000_000))
    sample_list.append(sample)
    total_rows += len(sample)

    print(f"Chunk {i+1}: {len(sample):,} Zeilen gezogen (gesamt: {total_rows:,})")

# Alle Samples zusammenführen
df_sample = pd.concat(sample_list, ignore_index=True)

# Ergebnis speichern
df_sample.to_csv(output_file, index=False)

print(f"\nFertig! Zufälliges Sample mit {len(df_sample):,} Zeilen gespeichert unter:")
print(output_file)


