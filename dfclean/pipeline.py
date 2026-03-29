from __future__ import annotations
import time, pandas as pd
from typing import Optional
from dfclean.cleaner import DataFrameCleaner
from dfclean.imputers import NullImputer
from dfclean.detectors import OutlierDetector
from dfclean.type_handler import TypeHandler
from dfclean.reporter import CleanReport

class CleanPipeline:
    """Fluent, sklearn-compatible DataFrame cleaning pipeline."""
    def __init__(self, verbose=False):
        self.verbose=verbose; self._steps=[]; self._is_fitted=False; self.report_=None
        self._imputer=None; self._outlier=None; self._type_handler=None
        self._dc=DataFrameCleaner()

    def standardize_columns(self, case="snake"):
        self._steps.append({"name":"standardize_columns","kwargs":{"case":case}}); return self
    def replace_empty_strings(self):
        self._steps.append({"name":"replace_empty_strings","kwargs":{}}); return self
    def strip_whitespace(self):
        self._steps.append({"name":"strip_whitespace","kwargs":{}}); return self
    def normalize_strings(self, lowercase=True):
        self._steps.append({"name":"normalize_strings","kwargs":{"lowercase":lowercase}}); return self
    def drop_duplicates(self, subset=None, keep="first"):
        self._steps.append({"name":"drop_duplicates","kwargs":{"subset":subset,"keep":keep}}); return self
    def drop_constant_columns(self):
        self._steps.append({"name":"drop_constant_columns","kwargs":{}}); return self
    def drop_high_null_columns(self, threshold=0.7):
        self._steps.append({"name":"drop_high_null_columns","kwargs":{"threshold":threshold}}); return self
    def memory_optimize(self):
        self._steps.append({"name":"memory_optimize","kwargs":{}}); return self

    def impute_nulls(self, strategy="smart", numeric_strategy=None, categorical_strategy=None, null_threshold=70.0):
        self._imputer=NullImputer(strategy=strategy,numeric_strategy=numeric_strategy,
            categorical_strategy=categorical_strategy,null_threshold=null_threshold)
        self._steps.append({"name":"impute_nulls","kwargs":{"strategy":strategy}}); return self

    def fix_types(self, category_threshold=0.05, parse_dates=True, downcast=True):
        self._type_handler=TypeHandler(category_threshold=category_threshold,parse_dates=parse_dates,downcast=downcast)
        self._steps.append({"name":"fix_types","kwargs":{}}); return self

    def remove_outliers(self, method="iqr", treatment="clip", threshold=1.5, columns=None, contamination=0.05):
        self._outlier=OutlierDetector(method=method,treatment=treatment,threshold=threshold,columns=columns,contamination=contamination)
        self._steps.append({"name":"remove_outliers","kwargs":{"method":method,"treatment":treatment}}); return self

    def fit(self, df):
        work=df.copy()
        for step in self._steps: work=self._apply_step(step,work,fitting=True)
        self._is_fitted=True; return self

    def transform(self, df):
        if not self._is_fitted: raise RuntimeError("Call fit() or fit_transform() first.")
        result=df.copy()
        for step in self._steps: result=self._apply_step(step,result,fitting=False)
        return result

    def fit_transform(self, df):
        before=df.copy(); t0=time.perf_counter(); log=[]; work=df.copy()
        for step in self._steps:
            rb,nb=len(work),work.isna().sum().sum()
            work=self._apply_step(step,work,fitting=True)
            detail=f"rows:{rb}->{len(work)}, nulls:{nb}->{work.isna().sum().sum()}"
            log.append({"step":step["name"],"detail":detail})
            if self.verbose: print(f"  ok {step['name']:30s} {detail}")
        if self.verbose: print(f"  Done in {time.perf_counter()-t0:.3f}s")
        self._is_fitted=True; self.report_=CleanReport(before,work,log); return work

    def _apply_step(self, step, df, fitting):
        n,kw=step["name"],step["kwargs"]
        if n=="standardize_columns":    return self._dc.standardize_column_names(df,**kw)
        if n=="replace_empty_strings":  return self._dc.replace_empty_strings(df)
        if n=="strip_whitespace":       return self._dc.strip_whitespace(df)
        if n=="normalize_strings":      return self._dc.normalize_strings(df,**kw)
        if n=="drop_duplicates":        return self._dc.drop_duplicates(df,**kw)
        if n=="drop_constant_columns":  return self._dc.drop_constant_columns(df)
        if n=="drop_high_null_columns": return self._dc.drop_high_null_columns(df,**kw)
        if n=="memory_optimize":        return self._dc.memory_optimize(df)
        if n=="impute_nulls" and self._imputer:
            return self._imputer.fit_transform(df) if fitting else self._imputer.transform(df)
        if n=="fix_types" and self._type_handler:
            return self._type_handler.fit_transform(df) if fitting else self._type_handler.transform(df)
        if n=="remove_outliers" and self._outlier:
            return self._outlier.fit_transform(df) if fitting else self._outlier.transform(df)
        return df

    def report(self):
        if self.report_ is None: raise RuntimeError("Run fit_transform() first.")
        print(self.report_); return self.report_

    def __repr__(self):
        return f"CleanPipeline([{chr(32).join(s['name'] for s in self._steps)}])"
