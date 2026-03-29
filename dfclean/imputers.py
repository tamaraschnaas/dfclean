from __future__ import annotations
import pandas as pd, numpy as np
from dfclean.utils import _col_null_pct

class NullImputer:
    def __init__(self, strategy="smart", numeric_strategy=None, categorical_strategy=None, fill_value=None, null_threshold=70.0):
        self.strategy=strategy; self.numeric_strategy=numeric_strategy
        self.categorical_strategy=categorical_strategy; self.fill_value=fill_value
        self.null_threshold=null_threshold; self._fill_values={}; self._cols_to_drop=[]

    def fit(self, df):
        self._fill_values={}; self._cols_to_drop=[]
        for col in df.columns:
            if _col_null_pct(df[col]) >= self.null_threshold:
                self._cols_to_drop.append(col); continue
            if pd.api.types.is_numeric_dtype(df[col]):
                strat = self.numeric_strategy or self.strategy
                if strat == "smart": strat = "median"
            else:
                strat = self.categorical_strategy or self.strategy
                if strat == "smart": strat = "mode"
            self._fill_values[col] = self._compute(df[col], strat)
        return self

    def transform(self, df):
        df=df.copy()
        drop=[c for c in self._cols_to_drop if c in df.columns]
        if drop: df=df.drop(columns=drop)
        for col, value in self._fill_values.items():
            if col not in df.columns: continue
            strat=(self.numeric_strategy or self.strategy if pd.api.types.is_numeric_dtype(df[col]) else self.categorical_strategy or self.strategy)
            if strat=="ffill": df[col]=df[col].ffill()
            elif strat=="bfill": df[col]=df[col].bfill()
            elif strat=="drop_rows": df=df.dropna(subset=[col])
            elif value is not None: df[col]=df[col].fillna(value)
        return df

    def fit_transform(self, df): return self.fit(df).transform(df)

    @staticmethod
    def _compute(series, strategy):
        if strategy=="median": return series.median()
        if strategy=="mean": return series.mean()
        if strategy=="mode":
            m=series.mode(); return m.iloc[0] if not m.empty else None
        return None
