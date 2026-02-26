from pathlib import Path

def discover_files(raw_data_dir: str) -> list[Path]:
    target_folder = Path(raw_data_dir)
    if not target_folder.exists():
        raise FileNotFoundError(f"Directory {raw_data_dir} not found.")
    
    csv_files = list(target_folder.rglob("*.csv"))
    excel_files = list(target_folder.rglob("*.xlsx"))
    
    return csv_files + excel_files