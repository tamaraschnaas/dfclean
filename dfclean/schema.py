from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any
import pandas as pd, numpy as np

@dataclass
class ColumnSchema:
    dtype: Optional[str] = None
    required: bool = False
    nullable: bool = True
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    allowed_values: Optional[list] = None
    rename: Optional[str] = None

class DataFrameSchema:
    def __init__(self, columns: dict):
        self.columns=columns; self._issues=[]

    def apply(self, df):
        df=df.copy(); self._issues=[]
        for col,spec in self.columns.items():
            if spec.required and col not in df.columns:
                raise ValueError(f"Required column '{col}' is missing.")
            if col not in df.columns: continue
            if spec.dtype:
                try: df[col]=df[col].astype(spec.dtype)
                except Exception as e: self._issues.append({"column":col,"issue":str(e)})
            if spec.min_value is not None:
                mask=df[col]<spec.min_value
                if mask.any(): self._issues.append({"column":col,"issue":f"{mask.sum()} below min"}); df.loc[mask,col]=np.nan
            if spec.max_value is not None:
                mask=df[col]>spec.max_value
                if mask.any(): self._issues.append({"column":col,"issue":f"{mask.sum()} above max"}); df.loc[mask,col]=np.nan
            if spec.allowed_values is not None:
                mask=~df[col].isin(spec.allowed_values)&df[col].notna()
                if mask.any(): self._issues.append({"column":col,"issue":f"{mask.sum()} invalid values"}); df.loc[mask,col]=np.nan
            if not spec.nullable:
                n=df[col].isna().sum()
                if n: self._issues.append({"column":col,"issue":f"Dropped {n} null rows"}); df=df.dropna(subset=[col])
            if spec.rename and spec.rename!=col:
                df=df.rename(columns={col:spec.rename})
        return df

    def validation_report(self):
        if not self._issues: return pd.DataFrame(columns=["column","issue"])
        return pd.DataFrame(self._issues)
