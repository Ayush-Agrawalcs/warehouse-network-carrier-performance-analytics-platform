# Warehouse Network Carrier Performance Analytics Platform

## Project Structure

```text
.
├── Readme.md
├── architecture
│   └── Project_architecture_diagram.png
├── datasets
│   ├── csv
│   │   ├── FreightRates.csv
│   │   ├── OrderList.csv
│   │   ├── PlantPorts.csv
│   │   ├── ProductsPerPlant.csv
│   │   ├── VmiCustomers.csv
│   │   ├── WhCapacities.csv
│   │   └── WhCosts.csv
│   └── raw
│       └── Supply chain logisitcs problem.xlsx
├── documentation
│   └── Project_documentation.pdf
├── lambda
│   └── lambda_functions.py
├── pyspark_folder
│   └── elt
│       ├── __pycache__
│       ├── analytics.py
│       ├── config.py
│       ├── db_loader.py
│       ├── dimensions.py
│       ├── etl.py
│       ├── extraction.py
│       ├── loading.py
│       ├── main.py
│       └── transformation.py
├── requirement.txt
├── screenshots
│   ├── Join_Tables.jpeg
│   ├── Row_count.jpeg
│   ├── file_load.jpeg
│   └── s3_bucket_struct.png
├── scripts
│   └── read_data.py
├── sql
│   ├── analysis_queries
│   │   └── querry.py
│   └── schema
│       ├── __pycache__
│       ├── create_database.py
│       ├── create_schema.py
│       └── db_connection.py
└── visualizations
    ├── run_visualisation.py
    └── visualise.py

```

## Architecture

```text
CSV Files
    ↓
Amazon S3 (Raw Zone)
    ↓
S3 PUT Event
    ↓
AWS Lambda Trigger
    ↓
PySpark ETL Processing
    ↓
Amazon S3 (Curated Zone)
    ↓
Amazon RDS PostgreSQL
    ↓
SQL Analytics & Dashboards
```


## Architecture Diagram

<p align="center">
  <img src="architecture/Project_architecture_diagram.png" width="1000">
</p>