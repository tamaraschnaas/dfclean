from __future__ import annotations
import re, pandas as pd, numpy as np
from typing import Optional

class DataFrameCleaner:
    @staticmethod
    def standardize_column_names(df, case="snake"):
        def to_snake(n):
            n=re.sub(r"[\s\-\.]+","_",n.strip())
            n=re.sub(r"([A-Z])",r"_\1",n).lower().strip("_")
            return re.sub(r"_+","_",n)
        df=df.copy(); df.columns=[to_snake(c) for c in df.columns]; return df

    @staticmethod
    def drop_constant_columns(df):
        return df.drop(columns=[c for c in df.columns if df[c].nunique(dropna=True)<=1])

    @staticmethod
    def drop_high_null_columns(df, threshold=0.7):
        null_ratio=df.isna().mean(); return df[null_ratio[null_ratio<=threshold].index]

    @staticmethod
    def drop_duplicates(df, subset=None, keep="first"):
        return df.drop_duplicates(subset=subset,keep=keep)

    @staticmethod
    def strip_whitespace(df):
        df=df.copy()
        for col in df.select_dtypes(include=["object","string"]).columns: df[col]=df[col].str.strip()
        return df

    @staticmethod
    def normalize_strings(df, lowercase=True):
        df=df.copy()
        for col in df.select_dtypes(include=["object","string"]).columns:
            df[col]=df[col].str.strip().str.replace(r"\s+"," ",regex=True)
            if lowercase: df[col]=df[col].str.lower()
        return df

    @staticmethod
    def replace_empty_strings(df, replacement=np.nan):
        df=df.copy()
        for col in df.select_dtypes(include=["object","string"]).columns:
            df[col]=df[col].replace(r"^\s*$",replacement,regex=True)
        return df

    @staticmethod
    def memory_optimize(df):
        df=df.copy()
        for col in df.select_dtypes(include=["int64","int32"]).columns:
            df[col]=pd.to_numeric(df[col],downcast="integer")
        for col in df.select_dtypes(include=["float64"]).columns:
            df[col]=pd.to_numeric(df[col],downcast="float")
        for col in df.select_dtypes(include=["object"]).columns:
            if df[col].nunique()/len(df)<0.05: df[col]=df[col].astype("category")
        return df
