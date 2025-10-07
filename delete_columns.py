import pandas as pd

def delete_columns(input_file, output_file, columns_to_delete):
    """
    Delete specific columns from a CSV file.

    :param input_file: Path to input CSV
    :param output_file: Path to output CSV
    :param columns_to_delete: List of column names to remove
    """
    chunksize = 4_000_000
    first_chunk = True  # to write header only once

    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        # Drop unwanted columns
        chunk = chunk.drop(columns=columns_to_delete, errors='ignore')

        # Append to output CSV
        chunk.to_csv(output_file, mode='a', index=False, header=first_chunk)
        first_chunk = False  # after first chunk, don’t write header again

if __name__ == "__main__":
    # Example usage
    input_file = "data/2023_Yellow_Taxi_Trip_Data.csv"
    output_file = "data/Taxi_Data_improved.csv"
    columns_to_delete = ["VendorID", "RatecodeID", "store_and_fwd_flag", "PULocationID", "DOLocationID", "mta_tax", "payment_type"]

    delete_columns(input_file, output_file, columns_to_delete)
    print(f"Columns {columns_to_delete} removed. New file saved as {output_file}.")

