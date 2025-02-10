from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
import json

app = FastAPI()

def detect_fact_dimension(tables):
    """Classifies tables as Fact or Dimension based on dependencies."""
    table_info = {}

    # Extract column information for each table
    for name, df in tables.items():
        table_info[name] = {
            "columns": list(df.columns),
            "unique_counts": {col: df[col].nunique() for col in df.columns},
            "row_count": len(df)
        }

    # Identify Primary Keys (PKs)
    pk_candidates = {}
    for name, info in table_info.items():
        for col, unique_count in info["unique_counts"].items():
            if unique_count == info["row_count"]:  # Fully unique column
                pk_candidates.setdefault(name, []).append(col)

    # Identify Foreign Keys (FKs)
    fk_candidates = {}
    for name, info in table_info.items():
        for col in info["columns"]:
            for other_name, other_info in table_info.items():
                if name != other_name and col in other_info["unique_counts"]:
                    if info["unique_counts"][col] <= other_info["unique_counts"][col]:
                        fk_candidates.setdefault(name, []).append(col)

    # Classify Fact and Dimension Tables
    fact_tables = []
    dimension_tables = []
    pk_to_table = {pk: name for name, pks in pk_candidates.items() for pk in pks}  # Map PKs to tables

    for name, pks in pk_candidates.items():
        if any(pk in fk_candidates.get(other, []) for other, other_pks in pk_candidates.items() if other != name for pk in pks):
            dimension_tables.append(name)  # If its PK is an FK in another table, it's a dimension
        else:
            fact_tables.append(name)  # If it does not depend on any other table, it's a fact table

    return {
        "fact_tables": fact_tables,
        "dimension_tables": dimension_tables
    }

