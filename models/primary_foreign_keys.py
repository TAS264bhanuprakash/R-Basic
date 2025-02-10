from fastapi import HTTPException
from utils.helpers import json_friendly
import pandas as pd

def identify_keys(data1, data2):
    """Identify primary and foreign key candidates for both datasets separately"""
    if data1 is None or data2 is None:
        raise HTTPException(status_code=400, detail="No data uploaded")
    
    # Identify primary keys (unique & NOT NULL) in both files
    primary_keys_data1 = [col for col in data1.columns if data1[col].nunique() == len(data1) and data1[col].isna().sum() == 0]
    primary_keys_data2 = [col for col in data2.columns if data2[col].nunique() == len(data2) and data2[col].isna().sum() == 0]
    
    # Identify potential foreign keys in both files
    foreign_keys_data1 = [col for col in data1.columns if data1[col].nunique() < len(data1) and data1[col].nunique() > 1]
    foreign_keys_data2 = [col for col in data2.columns if data2[col].nunique() < len(data2) and data2[col].nunique() > 1]
    
   
    finaly_foreign_key1=[]
    for fk in primary_keys_data2:
        if fk in foreign_keys_data1:
            finaly_foreign_key1.append(fk)  

    return {
        "file1": {
            "primary_keys": json_friendly(primary_keys_data1),
            "foreign_keys": json_friendly(finaly_foreign_key1),
        },
        "file2": {
            "primary_keys": json_friendly(primary_keys_data2),
            "foreign_keys": json_friendly(foreign_keys_data2),
        }
    }
from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
import json

app = FastAPI()

def extract_pk_fk_relationships(tables):
    """Extracts Primary and Foreign Key relationships dynamically between uploaded tables."""
    table_info = {}
    pk_candidates = {}  # Store primary keys
    fk_candidates = {}  # Store foreign keys

    # Extract column information for each table
    for name, df in tables.items():
        unique_counts = {col: df[col].nunique() for col in df.columns}
        row_count = len(df)

        table_info[name] = {
            "columns": list(df.columns),
            "unique_counts": unique_counts,
            "row_count": row_count
        }

        # Identify Primary Keys (PKs)
        pk_candidates[name] = [
            col for col, unique_count in unique_counts.items() if unique_count == row_count
        ]

    # Identify Foreign Keys (FKs)
    pk_to_table = {pk: table for table, pks in pk_candidates.items() for pk in pks}

    for name, df in tables.items():
        fk_candidates[name] = [
            col for col in df.columns if col in pk_to_table and pk_to_table[col] != name
        ]

    # Build Relationship Structure
    relationships = {
        "primary_keys": pk_candidates,
        "foreign_keys": fk_candidates,
        "relations": []
    }

    # Define relationships where a table references another
    for fk_table, fks in fk_candidates.items():
        for fk in fks:
            pk_table = pk_to_table[fk]
            relationships["relations"].append({
                "from_table": fk_table,
                "foreign_key": fk,
                "to_table": pk_table,
                "primary_key": fk
            })

    return relationships


