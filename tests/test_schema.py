import pandas as pd, numpy as np, pytest
from dfclean import ColumnSchema, DataFrameSchema

def test_range():
    df=pd.DataFrame({"age":[25,-5,200,40]})
    r=DataFrameSchema({"age":ColumnSchema(dtype="float64",min_value=0,max_value=120)}).apply(df)
    assert r["age"].isna().sum()==2

def test_required_raises():
    with pytest.raises(ValueError):
        DataFrameSchema({"y":ColumnSchema(required=True)}).apply(pd.DataFrame({"x":[1]}))

def test_rename():
    df=pd.DataFrame({"OldName":[1,2,3]})
    r=DataFrameSchema({"OldName":ColumnSchema(rename="new_name")}).apply(df)
    assert "new_name" in r.columns
