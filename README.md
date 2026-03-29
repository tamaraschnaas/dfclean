# 🧹 dfclean

> Automatic DataFrame cleaning — nulls, duplicates, types, outliers — with a fluent pipeline API.

[![PyPI](https://img.shields.io/pypi/v/dfclean)](https://pypi.org/project/dfclean/)
[![CI](https://github.com/YOUR_USERNAME/dfclean/actions/workflows/publish.yml/badge.svg)](https://github.com/YOUR_USERNAME/dfclean/actions)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/dfclean/blob/main/notebooks/tutorial.ipynb)

## Install
\`\`\`bash
pip install dfclean
\`\`\`

## Quick start
\`\`\`python
from dfclean import CleanPipeline

pipeline = (
    CleanPipeline(verbose=True)
    .standardize_columns()
    .replace_empty_strings()
    .drop_duplicates()
    .drop_high_null_columns(threshold=0.6)
    .impute_nulls(strategy="smart")
    .fix_types()
    .remove_outliers(method="iqr", treatment="clip")
)

df_clean = pipeline.fit_transform(df_raw)
pipeline.report()
\`\`\`
