import polars as pl
import io

# Strict schema enforcement to prevent concatenation crashes
EXPECTED_SCHEMA = {
    "Date": pl.String, 
    "Revenue": pl.Float64,
    "Region": pl.String
}

def process_uploaded_files(uploaded_files) -> pl.DataFrame | None:
    processed_dfs = []
    
    for file in uploaded_files:
        try:
            # Streamlit provides an UploadedFile object (a subclass of BytesIO)
            # Polars can read directly from these byte buffers
            if file.name.endswith('.csv'):
                df = pl.read_csv(file)
            elif file.name.endswith('.xlsx'):
                # fastexcel requires reading the bytes explicitly
                file_bytes = file.read()
                df = pl.read_excel(file_bytes, engine="fastexcel")
            else:
                continue # Skip unsupported
                
            # Schema Validation: Ensure required columns exist
            missing_cols = [col for col in EXPECTED_SCHEMA.keys() if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Missing columns: {missing_cols}")
                
            # Cast strictly to defined types
            clean_df = df.select([
                pl.col(col).cast(dtype) for col, dtype in EXPECTED_SCHEMA.items()
            ])
            
            processed_dfs.append(clean_df)
            
        except Exception as e:
            # In a production app, you would log this error rather than just printing
            print(f"Failed to process {file.name}: {e}")

    if processed_dfs:
        return pl.concat(processed_dfs, how="vertical")
    
    return None