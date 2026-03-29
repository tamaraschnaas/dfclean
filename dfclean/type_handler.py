from __future__ import annotations
import re, pandas as pd, numpy as np
from dfclean.utils import _object_cols

_PATTERNS = {
    "email": re.compile(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$", re.I),
    "phone": re.compile(r"^[\+\d][\d\s\-().]{6,}$"),
    "url":   re.compile(r"^https?://\S+$", re.I),
    "postal_code": re.compile(r"^\d{4,6}$"),
}

class TypeHandler:
    def __init__(self, category_threshold=0.05, parse_dates=True, downcast=True):
        self.category_threshold=category_threshold; self.parse_dates=parse_dates
        self.downcast=downcast; self._conversions={}; self._semantic_tags={}

    def fit(self, df):
        self._conversions={}; self._semantic_tags={}
        for col in _object_cols(df):
            series=df[col].dropna().astype(str)
            if len(series)==0: continue
            if pd.to_numeric(series,errors="coerce").notna().mean()>0.9:
                self._conversions[col]="numeric"; continue
            if self.parse_dates:
                try:
                    parsed=pd.to_datetime(series,infer_datetime_format=True,errors="coerce")
                    if parsed.notna().mean()>0.85: self._conversions[col]="datetime"; continue
                except Exception: pass
            if series.nunique()/len(series)<=self.category_threshold:
                self._conversions[col]="category"; continue
            for tag,pat in _PATTERNS.items():
                if series.head(50).apply(lambda x: bool(pat.match(x))).mean()>0.8:
                    self._semantic_tags[col]=tag; break
        return self

    def transform(self, df):
        df=df.copy()
        for col,dtype in self._conversions.items():
            if col not in df.columns: continue
            try:
                if dtype=="numeric": df[col]=pd.to_numeric(df[col],errors="coerce")
                elif dtype=="datetime": df[col]=pd.to_datetime(df[col],infer_datetime_format=True,errors="coerce")
                elif dtype=="category": df[col]=df[col].astype("category")
            except Exception: pass
        if self.downcast:
            for col in df.select_dtypes(include=["int64","int32"]).columns:
                df[col]=pd.to_numeric(df[col],downcast="integer")
            for col in df.select_dtypes(include=["float64"]).columns:
                df[col]=pd.to_numeric(df[col],downcast="float")
        return df

    def fit_transform(self, df): return self.fit(df).transform(df)
    @property
    def semantic_tags(self): return dict(self._semantic_tags)
    @property
    def type_conversions(self): return dict(self._conversions)
