#!/usr/bin/env python3
# clean_parts.py
import csv
import glob
import os
from typing import List
import pandas as pd

# Erwartete Spalten (deine ursprüngliche Header-Liste)
EXPECTED_COLUMNS: List[str] = [
    "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime",
    "passenger_count", "trip_distance", "RatecodeID", "store_and_fwd_flag",
    "PULocationID", "DOLocationID", "payment_type", "fare_amount",
    "extra", "mta_tax", "tip_amount", "tolls_amount",
    "improvement_surcharge", "total_amount", "congestion_surcharge"
]

# Spalten, die du löschen willst (anpassen)
DROP_COLUMNS = ["VendorID", "RatecodeID", "store_and_fwd_flag", "PULocationID", "DOLocationID", "mta_tax"]

OUT_DIR = "cleaned"

def process_part_file(path: str,
                      expected_columns: List[str],
                      drop_columns: List[str],
                      out_dir: str = OUT_DIR):
    n_expected = len(expected_columns)
    header_tokens = set(expected_columns)

    skipped_headers = 0
    padded = 0
    truncated = 0
    total_rows = 0
    accepted_rows = []

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            # Wenn eine Zelle exakt einem bekannten Header entspricht => Header-Zeile (wiederholt)
            if any(cell in header_tokens for cell in row):
                skipped_headers += 1
                continue
            total_rows += 1
            # Normalisiere Zeilenlänge
            if len(row) < n_expected:
                row = row + [''] * (n_expected - len(row))
                padded += 1
            elif len(row) > n_expected:
                row = row[:n_expected]
                truncated += 1
            accepted_rows.append(row)

    if not accepted_rows:
        print(f"[WARN] {path}: keine Datenzeilen nach Entfernen von Headern gefunden.")
        return

    # DataFrame aus normalisierten Zeilen
    df = pd.DataFrame(accepted_rows, columns=expected_columns)

    # Spalten zum löschen filtern (nur vorhandene löschen)
    to_drop = [c for c in drop_columns if c in df.columns]
    if to_drop:
        df = df.drop(columns=to_drop)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, os.path.basename(path) + ".clean.csv")
    df.to_csv(out_path, index=False, encoding='utf-8-sig')

    print(f"Processed {path} -> {out_path}")
    print(f"  Eingelesene Zeilen: {total_rows}, akzeptierte Zeilen: {len(accepted_rows)}")
    print(f"  Header-Zeilen übersprungen: {skipped_headers}")
    print(f"  Zeilen gepadded: {padded}, Zeilen gekürzt: {truncated}")
    print(f"  Gelöschte Spalten (falls vorhanden): {to_drop}")
    print("")

if __name__ == "__main__":
    files = sorted(glob.glob("part_aa"))
    if not files:
        print("Keine part_aa Dateien im aktuellen Verzeichnis gefunden.")
    else:
        for p in files:
            process_part_file(p, EXPECTED_COLUMNS, DROP_COLUMNS)

