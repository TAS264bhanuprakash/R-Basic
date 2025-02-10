from fastapi import HTTPException
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from utils.helpers import json_friendly

def ml_combined_correlation(data1, data2):
    """
    Compute correlations where:
    - File 1 columns are correlated with all columns from both files
    - File 2 columns are correlated only with File 2 columns
    """
    if data1 is None or data2 is None:
        raise HTTPException(status_code=400, detail="Two datasets are required")

    correlation_results = {
        "file1_correlations": {},  # Correlations for file 1 columns with all columns
        "file2_correlations": {}   # Correlations for file 2 columns with file 2 columns only
    }

    data1 = data1.copy()
    data2 = data2.copy()

    # Ensure data1 and data2 are pandas DataFrames
    if not isinstance(data1, pd.DataFrame):
        raise HTTPException(status_code=400, detail="data1 is not a valid DataFrame")
    if not isinstance(data2, pd.DataFrame):
        raise HTTPException(status_code=400, detail="data2 is not a valid DataFrame")

    # Convert categorical columns to numerical using Label Encoding
    for df in [data1, data2]:
        for col in df.select_dtypes(include=["object", "category"]).columns:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))

    # Fill missing values with median, then ensure no NaNs remain
    for df in [data1, data2]:
        df.fillna(df.median(numeric_only=True), inplace=True)
        df.fillna(0, inplace=True)

    # Convert all columns to float32 for XGBoost compatibility
    data1 = data1.astype(np.float32)
    data2 = data2.astype(np.float32)

    def compute_xgb_importance(df, target_col):
        """Train an XGBoost model and get feature importance for the given target column."""
        if target_col not in df.columns:
            return None
        
        X = df.drop(columns=[target_col])
        y = df[target_col].values.ravel().astype(float)

        X_values = X.values.astype(np.float32)
        
        if not np.issubdtype(X_values.dtype, np.number):
            raise HTTPException(status_code=500, detail="X contains non-numeric data")

        if len(set(y)) == 1:
            return None

        X_train, X_test, y_train, y_test = train_test_split(X_values, y, test_size=0.2, random_state=42)

        # Create DMatrix objects
        dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=list(X.columns))
        dtest = xgb.DMatrix(X_test, label=y_test, feature_names=list(X.columns))

        params = {
            'objective': 'reg:squarederror',
            'eval_metric': 'rmse',
            'max_depth': 6,
            'eta': 0.3,
            'subsample': 0.8,
            'colsample_bytree': 0.8
        }

        try:
            model = xgb.train(
                params,
                dtrain,
                num_boost_round=100,
                evals=[(dtrain, 'train'), (dtest, 'test')],
                verbose_eval=False
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"XGBoost training error: {str(e)}")

        feature_importance = model.get_score(importance_type='gain')
        
        # Normalize feature importance scores
        total_importance = sum(feature_importance.values())
        if total_importance > 0:
            feature_importance = {k: v/total_importance for k, v in feature_importance.items()}
        
        # Ensure all features have an importance score
        for feature in X.columns:
            if feature not in feature_importance:
                feature_importance[feature] = 0.0

        # Calculate MSE and R-squared
        y_pred = model.predict(dtest)
        mse = mean_squared_error(y_test, y_pred)
        
        return {
            "correlations": {
                feature: json_friendly(importance)
                for feature, importance in sorted(
                    feature_importance.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            },
            "metrics": {
                "mse": json_friendly(mse)
            }
        }

    # Process File 1 columns (correlate with all columns)
    combined_df = pd.concat([data1, data2], axis=1, join="inner", keys=['file1', 'file2'])
    combined_df.columns = [f"{key}_{col}" for key, col in combined_df.columns]
    
    for col in data1.columns:
        target_col = f"file1_{col}"
        result = compute_xgb_importance(combined_df, target_col)
        if result:
            # Clean up column names in results
            cleaned_correlations = {}
            for feat, imp in result["correlations"].items():
                source, clean_name = feat.split('_', 1)
                cleaned_correlations[f"{clean_name} ({source})"] = imp
            
            correlation_results["file1_correlations"][col] = {
                "correlations": cleaned_correlations,
                "metrics": result["metrics"]
            }

    # Process File 2 columns (correlate only with File 2 columns)
    for col in data2.columns:
        result = compute_xgb_importance(data2, col)
        if result:
            correlation_results["file2_correlations"][col] = result

    return correlation_results


def combined_correlation(data1, data2):
        """Compute combined column correlations for two datasets and store results in a single dictionary"""
        if data1 is None or data2 is None:
            raise HTTPException(status_code=400, detail="Two datasets are required")

        correlation_results = {}

        data1 = data1.copy()
        data2 = data2.copy()

        # Convert categorical columns to numerical using Label Encoding
        encoders1 = {}
        for col in data1.select_dtypes(include=["object"]).columns:
            encoders1[col] = LabelEncoder()
            data1[col] = encoders1[col].fit_transform(data1[col].astype(str))

        encoders2 = {}
        for col in data2.select_dtypes(include=["object"]).columns:
            encoders2[col] = LabelEncoder()
            data2[col] = encoders2[col].fit_transform(data2[col].astype(str))

        data1.fillna(data1.median(numeric_only=True), inplace=True)
        data2.fillna(data2.median(numeric_only=True), inplace=True)

        # Calculate correlations within data1 and between data1 and data2
        for col1 in data1.columns:
            correlation_results[col1] = {"data1": {}, "data2": {}}
            for col2 in data1.columns:
                if col1 == col2:
                    continue
                correlation = data1[col1].corr(data1[col2])
                correlation_results[col1]["data1"][col2] = json_friendly(correlation)

            for col2 in data2.columns:
                correlation = data1[col1].corr(data2[col2])
                correlation_results[col1]["data2"][col2] = json_friendly(correlation)

        for col1 in data2.columns:
            if col1 not in correlation_results:
                correlation_results[col1] = {"data1": {}, "data2": {}}
            for col2 in data2.columns:
                if col1 == col2:
                    continue
                correlation = data2[col1].corr(data2[col2])
                correlation_results[col1]["data2"][col2] = json_friendly(correlation)

            for col2 in data1.columns:
                correlation = data2[col1].corr(data1[col2])
                correlation_results[col1]["data1"][col2] = json_friendly(correlation)

        return correlation_results
