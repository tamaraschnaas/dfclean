# 🧹 dfclean

> Limpieza automática de DataFrames: nulos, duplicados, tipos y outliers — con una API fluent compatible con scikit-learn.

[![PyPI](https://img.shields.io/pypi/v/dfclean?color=e94560)](https://pypi.org/project/dfclean/)
[![CI](https://github.com/tamaraschnaas/dfclean/actions/workflows/publish.yml/badge.svg)](https://github.com/tamaraschnaas/dfclean/actions)
[![Python](https://img.shields.io/pypi/pyversions/dfclean)](https://pypi.org/project/dfclean/)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-yellow.svg)](LICENSE)
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tamaraschnaas/dfclean/blob/main/notebooks/tutorial.ipynb)

---

## ¿Qué es dfclean?

`dfclean` resuelve el problema más repetitivo del análisis de datos: **limpiar un DataFrame antes de poder usarlo**. En lugar de escribir decenas de líneas de pandas manualmente, defines un pipeline declarativo en una sola expresión encadenada.
```python
from dfclean import CleanPipeline

df_limpio = (
    CleanPipeline(verbose=True)
    .standardize_columns()
    .replace_empty_strings()
    .drop_duplicates()
    .drop_high_null_columns(threshold=0.6)
    .impute_nulls(strategy="smart")
    .fix_types()
    .remove_outliers(method="iqr", treatment="clip")
    .fit_transform(df_sucio)
)
```

---

## Instalación
```bash
pip install dfclean
```

Con soporte para Isolation Forest y LOF (requiere scikit-learn):
```bash
pip install "dfclean[ml]"
```

---

## Características principales

| Módulo | Descripción |
|---|---|
| **CleanPipeline** | API fluent encadenable, compatible con sklearn (`fit` / `transform`) |
| **NullImputer** | 7 estrategias: `smart`, `mean`, `median`, `mode`, `ffill`, `bfill`, `drop_rows` |
| **OutlierDetector** | IQR, Z-score, Isolation Forest, LOF — con tratamiento `clip`, `remove` o `nan` |
| **TypeHandler** | Detecta fechas, numéricos y categorías; downcast automático para ahorrar memoria |
| **DataFrameSchema** | Validación declarativa por columna: rangos, valores permitidos, renombrar |
| **CleanReport** | Reporte antes/después en texto, dict, JSON y HTML |

---

## Guía de uso

### Pipeline completo
```python
import pandas as pd
from dfclean import CleanPipeline

df = pd.read_csv("datos_sucios.csv")

pipeline = (
    CleanPipeline(verbose=True)
    .standardize_columns()               # Normaliza nombres a snake_case
    .replace_empty_strings()             # "" y "  " se convierten en NaN
    .drop_duplicates()                   # Elimina filas duplicadas
    .drop_constant_columns()             # Elimina columnas con un solo valor
    .drop_high_null_columns(threshold=0.6)   # Elimina cols con >60% nulos
    .impute_nulls(strategy="smart")          # Mediana para numéricos, moda para categóricos
    .fix_types()                         # Detecta fechas, categorías y numéricos
    .remove_outliers(method="iqr", treatment="clip")  # Recorta outliers
    .memory_optimize()                   # Downcast para ahorrar RAM
)

df_limpio = pipeline.fit_transform(df)
pipeline.report()
```

### Reutilizar en datos de prueba (estilo scikit-learn)
```python
pipeline.fit(df_entrenamiento)
df_prueba_limpio = pipeline.transform(df_prueba)
```

### Reporte HTML
```python
pipeline.report_.save_html("reporte_limpieza.html")
```

### Schema declarativo por columna
```python
from dfclean import ColumnSchema, DataFrameSchema

schema = DataFrameSchema({
    "edad":   ColumnSchema(dtype="float64", min_value=0, max_value=120, nullable=False),
    "status": ColumnSchema(allowed_values=["activo", "inactivo"]),
    "email":  ColumnSchema(required=True, rename="correo"),
})

df_validado = schema.apply(df)
print(schema.validation_report())
```

### Resumen de outliers
```python
from dfclean import OutlierDetector

det = OutlierDetector(method="iqr", treatment="clip")
print(det.outlier_summary(df))
```

---

## Docker
```bash
# Ejecutar pruebas
docker compose run tests

# Demo interactivo
docker compose run demo
```

---

## Desarrollo local
```bash
git clone https://github.com/tamaraschnaas/dfclean.git
cd dfclean
pip install -e ".[dev]"
pytest tests/ -v
```

---

## Estructura del proyecto
```
dfclean/
├── dfclean/
│   ├── pipeline.py       # CleanPipeline — API principal
│   ├── imputers.py       # NullImputer
│   ├── detectors.py      # OutlierDetector
│   ├── type_handler.py   # TypeHandler
│   ├── schema.py         # DataFrameSchema
│   ├── reporter.py       # CleanReport
│   └── cleaner.py        # Helpers estáticos
├── tests/                # Suite de pruebas con pytest
├── notebooks/            # Tutorial interactivo en Google Colab
├── .github/workflows/    # CI + publicación automática a PyPI
└── docker-compose.yml
```

---

## Licencia

MIT © tamaraschnaas
