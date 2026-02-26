import polars as pl
import io

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
                
            processed_dfs.append(df)
            
        except Exception as e:
            # In a production app, you would log this error rather than just printing
            print(f"Failed to process {file.name}: {e}")

    if processed_dfs:
        # Use diagonal to gracefully concat regardless of column schemas
        return pl.concat(processed_dfs, how="diagonal")
    
    return None