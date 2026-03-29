import pytest, pandas as pd
from dfclean import CleanPipeline

def test_basic_pipeline(messy_df):
    p=(CleanPipeline().standardize_columns().replace_empty_strings()
       .drop_duplicates().drop_constant_columns()
       .drop_high_null_columns(threshold=0.6).impute_nulls()
       .fix_types().remove_outliers())
    clean=p.fit_transform(messy_df)
    assert len(clean)<len(messy_df)
    assert clean.isna().sum().sum()==0
    assert "constant_col" not in clean.columns
    assert "mostly_null" not in clean.columns

def test_report_generated(messy_df):
    p=CleanPipeline().drop_duplicates().impute_nulls()
    p.fit_transform(messy_df); assert p.report_ is not None

def test_transform_before_fit_raises(messy_df):
    with pytest.raises(RuntimeError):
        CleanPipeline().impute_nulls().transform(messy_df)

def test_sklearn_api(messy_df):
    train,test=messy_df.iloc[:150].copy(),messy_df.iloc[150:].copy()
    p=CleanPipeline().impute_nulls().fix_types()
    p.fit(train); assert isinstance(p.transform(test),pd.DataFrame)
