import sqlite3
import pandas as pd
from fastapi import FastAPI, HTTPException
from utils.helpers import json_friendly

app = FastAPI()
DATABASE = "database.db"

def get_db_connection():
    return sqlite3.connect(DATABASE)

def get_data_from_table(table_name):
    """Fetch data from a specific table in the SQLite3 database."""
    conn = get_db_connection()
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

def data_quality(table_names=None):
    """Compute data quality metrics for specified tables or all tables in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if table_names:
        tables = table_names
    else:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    def compute_metrics(data):
        total_rows = len(data)
        missing_values = data.isnull().sum().to_dict()
        duplicate_rows = data.duplicated().sum()
        completeness = (1 - data.isnull().mean()).to_dict()
        uniqueness = data.nunique().to_dict()
        
        return {
            "missing_values": {col: json_friendly(value) for col, value in missing_values.items()},
            "duplicate_rows": json_friendly(duplicate_rows),
            "null_values_percentage": {col: json_friendly(value / total_rows * 100) for col, value in missing_values.items()},
            "duplicate_percentage": json_friendly(duplicate_rows / total_rows * 100),
            "completeness_percentage": {col: json_friendly(value * 100) for col, value in completeness.items()},
            "uniqueness_percentage": {col: json_friendly(value / total_rows * 100) for col, value in uniqueness.items()},
        }
    
    results = {}
    for table in tables:
        data = get_data_from_table(table)
        results[table] = compute_metrics(data)
    
    return results
@app.get("/data-quality")
def quality(table_names: str = None):
    table_names_list = table_names.split(",") if table_names else None
    return data_quality(table_names_list)