from fastapi import FastAPI, File, UploadFile, HTTPException,Query
import sqlite3
import pandas as pd
import os


app = FastAPI()
DATABASE = "database.db"

def get_db_connection():
    return sqlite3.connect(DATABASE)

def create_table_from_csv(file_path: str, table_name: str, conn):
    df = pd.read_csv(file_path)
    cursor = conn.cursor()
    
    # Identify primary key (assume first column if unique)
    primary_key = None
    for col in df.columns:
        if df[col].is_unique:
            primary_key = col
            break
    
    # Create table SQL statement
    columns = []
    for col in df.columns:
        dtype = "TEXT"
        if df[col].dtype == "int64":
            dtype = "INTEGER"
        elif df[col].dtype == "float64":
            dtype = "REAL"
        
        col_def = f"{col} {dtype}"
        if col == primary_key:
            col_def += " PRIMARY KEY"
        columns.append(col_def)
    
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
    cursor.execute(create_table_sql)
    
    # Insert data
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    
    return primary_key

@app.post("/upload-csv/")
def upload_csv(files: list[UploadFile]):
    conn = get_db_connection()
    cursor = conn.cursor()
    primary_keys = {}
    
    for file in files:
        file_path = file.filename
        table_name = os.path.splitext(file.filename)[0]
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        primary_key = create_table_from_csv(file_path, table_name, conn)
        primary_keys[table_name] = primary_key
    
    # Foreign Key Detection
    for table, pk in primary_keys.items():
        if not pk:
            continue
        for other_table in primary_keys:
            if other_table != table:
                # If column name matches a primary key of another table, add FK
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [row[1] for row in cursor.fetchall()]
                if pk in columns:
                    alter_sql = f"ALTER TABLE {table} ADD FOREIGN KEY ({pk}) REFERENCES {other_table}({pk});"
                    try:
                        cursor.execute(alter_sql)
                    except sqlite3.OperationalError:
                        pass
    
    conn.commit()
    conn.close()
    return {"message": "CSV files uploaded and processed.", "tables": list(primary_keys.keys())}

