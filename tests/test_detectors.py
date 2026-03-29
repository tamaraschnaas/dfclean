import pandas as pd, numpy as np, pytest
from dfclean import OutlierDetector

@pytest.fixture
def df_out():
    np.random.seed(0)
    return pd.DataFrame({"v":np.concatenate([np.random.normal(50,5,100),[200,-100,300]])})

def test_iqr_clip(df_out):
    r=OutlierDetector("iqr","clip").fit_transform(df_out); assert r["v"].max()<200

def test_iqr_remove(df_out):
    r=OutlierDetector("iqr","remove").fit_transform(df_out); assert len(r)<len(df_out)

def test_summary(df_out):
    s=OutlierDetector("iqr").outlier_summary(df_out); assert s["outliers"].sum()>=3
