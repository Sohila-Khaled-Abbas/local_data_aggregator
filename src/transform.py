import polars as pl

def standardize_dataframe(df: pl.DataFrame, required_columns: list[str]) -> pl.DataFrame:
    """
    Filters the dataframe to only include required columns and standardizes them.
    """
    # Check if the required columns actually exist in this specific file
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing required columns in data: {missing_cols}")

    # Polars select and cast operations
    cleaned_df = df.select([
        pl.col(col) for col in required_columns
    ])
    
    return cleaned_df