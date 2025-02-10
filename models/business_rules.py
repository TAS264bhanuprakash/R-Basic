# models/business_rules.py
from utils.helpers import json_friendly

def business_rule_violations(data1):
    """Detect violations of basic business rules"""
    if data1 is None:
        raise HTTPException(status_code=400, detail="No data uploaded")
    
    violations = {}
    if "QuantitySold" in data1.columns:
        violations["negative_QuantitySold"] = int((data1["QuantitySold"] < 0).sum())
    
    return {key: json_friendly(value) for key, value in violations.items()}
