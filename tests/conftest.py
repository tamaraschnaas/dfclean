import pytest, pandas as pd, numpy as np

@pytest.fixture
def messy_df():
    np.random.seed(42); n=200
    df=pd.DataFrame({
        "age":    np.concatenate([np.random.randint(18,80,n-5),[999,-5,150,np.nan,np.nan]]),
        "salary": np.concatenate([np.random.normal(50000,15000,n-3),[1e9,np.nan,np.nan]]),
        "name":   ["Alice","Bob","  Charlie  ","",None]*(n//5),
        "join_date":["2020-01-15","2021-06-30","not-a-date",None,"2019-12-01"]*(n//5),
        "status": ["active","inactive","Active","INACTIVE",None]*(n//5),
        "constant_col":["same"]*n,
        "mostly_null": [np.nan]*(n-2)+[1,2],
    })
    return pd.concat([df,df.iloc[:10]],ignore_index=True)
