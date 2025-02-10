from fastapi import FastAPI, HTTPException, UploadFile, File
import pandas as pd  # Add this import statement for pandas
import numpy as np
import io
from utils.helpers import json_friendly

def analyze_granularity(data):
    """Analyze dataset granularity (rows, columns, date detection)"""
    if data is None:
        raise HTTPException(status_code=400, detail="No data uploaded")
    
    date_columns = [col for col in data.columns if pd.to_datetime(data[col], errors="coerce").notna().all()]
    return {
        "rows": json_friendly(len(data)),
        "columns": json_friendly(len(data.columns)),
        "date_columns": json_friendly(date_columns),
    }