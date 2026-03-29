import pandas as pd, numpy as np
from dfclean import NullImputer

def test_median(messy_df):
    result=NullImputer(strategy="median").fit_transform(messy_df)
    assert result["age"].isna().sum()==0

def test_drops_high_null_col(messy_df):
    result=NullImputer(null_threshold=50).fit_transform(messy_df)
    assert "mostly_null" not in result.columns

def test_mode_categorical():
    df=pd.DataFrame({"cat":["a","a","b",None,"a"]})
    result=NullImputer(strategy="mode").fit_transform(df)
    assert result["cat"].iloc[3]=="a"
