import polars as pl
from pathlib import Path

def ingest_file(file_path: Path) -> pl.DataFrame:
    """
    Evaluates the file extension and applies the correct Polars read function.
    """
    extension = file_path.suffix.lower()
    
    if extension == '.csv':
        # Eager load for simplicity in this pipeline, though scan_csv is faster for large files
        return pl.read_csv(file_path) 
    
    elif extension == '.xlsx':
        # Requires 'fastexcel' or 'calamine' engine installed
        return pl.read_excel(file_path, engine="fastexcel")
        
    else:
        raise ValueError(f"Unsupported file format: {extension}")