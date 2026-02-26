import polars as pl
from discovery import discover_files
from ingestion import ingest_file
from transform import standardize_dataframe

def run_pipeline():
    raw_dir = "../data/raw"
    output_path = "../data/processed/unified_report.csv"
    
    # Define the strict schema you want to extract
    target_columns = ["Date", "Revenue", "Region"] 
    
    files_to_process = discover_files(raw_dir)
    processed_dataframes = []

    for file in files_to_process:
        try:
            # 1. Ingest
            raw_df = ingest_file(file)
            
            # 2. Transform
            clean_df = standardize_dataframe(raw_df, target_columns)
            
            # 3. Append to list
            processed_dataframes.append(clean_df)
            print(f"Successfully processed: {file.name}")
            
        except Exception as e:
            print(f"Error processing {file.name}: {e}")

    # 4. Aggregate & Export
    if processed_dataframes:
        # Vertical concatenation requires identical schemas
        final_report = pl.concat(processed_dataframes, how="vertical")
        final_report.write_csv(output_path)
        print(f"Pipeline complete. Report saved to {output_path}")
    else:
        print("No data processed. Pipeline halted.")

if __name__ == "__main__":
    run_pipeline()