from __future__ import annotations
import pandas as pd, numpy as np
def _numeric_cols(df): return df.select_dtypes(include=[np.number]).columns.tolist()
def _object_cols(df):  return df.select_dtypes(include=["object","string"]).columns.tolist()
def _col_null_pct(s):  return s.isna().mean() * 100
def _describe_change(before, after):
    return {"rows_before":len(before),"rows_after":len(after),"rows_removed":len(before)-len(after),
            "cols_before":len(before.columns),"cols_after":len(after.columns),
            "nulls_before":int(before.isna().sum().sum()),"nulls_after":int(after.isna().sum().sum()),
            "duplicates_before":int(before.duplicated().sum()),"duplicates_after":int(after.duplicated().sum())}
