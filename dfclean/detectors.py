from __future__ import annotations
import pandas as pd, numpy as np
from dfclean.utils import _numeric_cols

class OutlierDetector:
    def __init__(self, method="iqr", treatment="clip", threshold=1.5, columns=None, contamination=0.05):
        self.method=method; self.treatment=treatment; self.threshold=threshold
        self.columns=columns; self.contamination=contamination; self._bounds={}

    def fit(self, df):
        cols=self.columns or _numeric_cols(df)
        self._cols=[c for c in cols if c in df.columns]
        if self.method=="iqr":
            for col in self._cols:
                q1,q3=df[col].quantile(0.25),df[col].quantile(0.75); iqr=q3-q1
                self._bounds[col]=(q1-self.threshold*iqr, q3+self.threshold*iqr)
        elif self.method=="zscore":
            for col in self._cols:
                mu,sigma=df[col].mean(),df[col].std()
                self._bounds[col]=(mu-self.threshold*sigma, mu+self.threshold*sigma)
        elif self.method in ("isolation_forest","lof"):
            try:
                from sklearn.ensemble import IsolationForest
                from sklearn.neighbors import LocalOutlierFactor
                X=df[self._cols].dropna()
                preds=(IsolationForest(contamination=self.contamination,random_state=42).fit_predict(X)
                       if self.method=="isolation_forest"
                       else LocalOutlierFactor(contamination=self.contamination).fit_predict(X))
                self._outlier_index=X.index[preds==-1]
            except ImportError:
                raise ImportError("pip install scikit-learn  for isolation_forest/lof")
        return self

    def transform(self, df):
        df=df.copy()
        if self.method in ("iqr","zscore"):
            for col,(lo,hi) in self._bounds.items():
                if col not in df.columns: continue
                mask=(df[col]<lo)|(df[col]>hi)
                if self.treatment=="remove": df=df[~mask]
                elif self.treatment=="clip": df[col]=df[col].clip(lo,hi)
                elif self.treatment=="nan": df.loc[mask,col]=np.nan
        elif self.method in ("isolation_forest","lof"):
            idx=[i for i in self._outlier_index if i in df.index]
            if self.treatment=="remove": df=df.drop(index=idx)
            elif self.treatment=="nan":
                for col in self._cols: df.loc[idx,col]=np.nan
        return df

    def fit_transform(self, df): return self.fit(df).transform(df)

    def outlier_summary(self, df):
        self.fit(df); rows=[]
        if self.method in ("iqr","zscore"):
            for col,(lo,hi) in self._bounds.items():
                n=((df[col]<lo)|(df[col]>hi)).sum()
                rows.append({"column":col,"outliers":int(n),"pct":round(n/len(df)*100,2),"lower_bound":round(lo,4),"upper_bound":round(hi,4)})
        return pd.DataFrame(rows)
