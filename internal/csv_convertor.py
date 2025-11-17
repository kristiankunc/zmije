import csv
import pandas as pd
from pathlib import Path

def convert_csv_to_dict(csv_file_path: Path) -> dict[tuple[str, ...], str]:
    df = pd.read_csv(csv_file_path, keep_default_na=False)
    
    result = {}
    for idx, row in df.iterrows():
        english = row.iloc[0]
        czech = row.iloc[1]
        # Skip if no English keyword found

        print(f"Processing row {idx}: English='{english}', Czech='{czech}'")
        
        if pd.isna(english) or english == "":
            continue

        # Skip if no Czech translation found
        if pd.isna(czech) or czech == "":
            continue
        
        # Create tuple key from Czech (can be multi-word like "právě když")
        key_tuple = tuple(czech.split())
        result[key_tuple] = english
    
    print("Generated KEYWORD_MAP:", result)
    return result

if __name__ == "__main__":
    keyword_map = convert_csv_to_dict(Path("internal/data.csv"))
    print(keyword_map)