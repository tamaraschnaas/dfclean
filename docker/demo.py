import pandas as pd, numpy as np
from dfclean import CleanPipeline

np.random.seed(42)
df = pd.DataFrame({
    "Age":    [25, 30, None, 999, 22, 30, 25],
    "Salary": [50000, None, 60000, 55000, 1e9, 60000, 50000],
    "Status": ["active", "INACTIVE", "", None, "active", "inactive", "active"],
    "Email":  ["a@b.com","c@d.com","bad","e@f.com",None,"g@h.com","a@b.com"],
})

print("=== BEFORE ==="); print(df.to_string())

pipeline = (CleanPipeline(verbose=True)
    .standardize_columns().replace_empty_strings()
    .drop_duplicates().impute_nulls(strategy="smart")
    .fix_types().remove_outliers(method="iqr", treatment="clip"))

clean = pipeline.fit_transform(df)
print("\n=== AFTER ==="); print(clean.to_string())
pipeline.report()
