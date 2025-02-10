# main.py
from fastapi import FastAPI, HTTPException, UploadFile, File,Query
import pandas as pd  # Add this import statement for pandas
import numpy as np
import io
from models.correlation import ml_combined_correlation,combined_correlation
from models.fact_dimensions import detect_fact_dimension
from models.data_quality import data_quality
from models.business_rules import business_rule_violations
from models.granularity import analyze_granularity
from utils.helpers import json_friendly
from models.primary_foreign_keys import extract_pk_fk_relationships
import json
from typing import List
import sqlite3

app = FastAPI()

def get_db_connection():
    return sqlite3.connect("database.db")  # Replace with your actual database file

@app.get("/list-tables/")
def list_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"tables": tables}

@app.get("/table-columns/")
def get_table_columns(table_names: List[str] = Query(..., description="Enter table names separated by commas")):
    """
    Retrieve columns for multiple tables.
    Example: /table-columns/?table_names=category1&table_names=customer1
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    result = {}

    for table_name in table_names:
        cursor.execute(f"PRAGMA table_info({table_name.strip()})")
        columns = [row[1] for row in cursor.fetchall()]
        result[table_name.strip()] = columns if columns else "Table not found"
    
    conn.close()
    return result


@app.get("/data-quality")
def quality(table_names: str = None):
    table_names_list = table_names.split(",") if table_names else None
    return data_quality(table_names_list)


@app.post("/profile-data/")
async def profile_data(files: list[UploadFile] = File(...)):
    tables = {}

    # Read each uploaded file
    for file in files:
        df = pd.read_csv(io.StringIO(file.file.read().decode("utf-8")))
        tables[file.filename] = df

    result = extract_pk_fk_relationships(tables)

    return json.loads(json.dumps(result, indent=4))


@app.post("/fact-and-dimention-tables/")
async def classify_tables(files: list[UploadFile] = File(...)):
    tables = {}
    
    for file in files:
        df = pd.read_csv(io.StringIO(file.file.read().decode("utf-8")))
        tables[file.filename] = df
    
    result = detect_fact_dimension(tables)
    
    return json.loads(json.dumps(result))