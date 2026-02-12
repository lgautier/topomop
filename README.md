# Data (engineering) tooling for the OMOP Common Data Model

## Why this?

Current definitions for the OMOP Common Data Model, and utilities
to generate definitions for a few SQL/DDL dialects are written in R.

This package is currently an experiment to facilitate the use of Python,
a popular language in data engineering circles, and its rich ecosystem
of packages for it, to implement data pipelines aiming at using
OMOP.

Initially, this package extract the OMOP CDM definitions from CSV files
distributed with the R package `CommonDataModel` into an intermediate
abstraction that can be used to translate OMOP into SQLAlchemy,
an Object-Relational Mapping (ORM) for Python.

## Installation

From this source tree:

```sh
pip install `.[sqlalchemy]'
```

## CLI

The CDM definitions in the R package `CommonDataModel` can be converted
to Python modules that use SQLAlchemy from command line. That



```sh
topomop-convert \
  -s path/to/sourcetree/CommonDataModel/inst/csv/ \
  -d path/to/python/conversion.py \
  v5.4
```


```sh
topomop-convert \
  -s $(Rscript -e "cat(system.file(\"csv\", package = \"CommonDataModel\"))"
  path/to/sourcetree/CommonDataModel/inst/csv/ \
  -d path/to/python/conversion.py \
  v5.4
```

