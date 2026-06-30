# Warehouse Network Carrier Performance Analytics Platform

## Project Structure

```text
warehouse-network-carrier-performance-analytics-platform/
├── README.md
├── documentation/
│   └── Project_Documentation.docx
├── architecture/
│   └── architecture_diagram.png
├── datasets/
│   ├── raw/
│   └── sample/
├── sql/
│   ├── schema/
│           └── create_database.py
│           └── create_schema.py
│           └── db_connection.py
│   └── analysis_queries/
├── pyspark/
│   ├── extraction/
│   ├── transformation/
│   └── loading/
├── screenshots/
├── testing/
│   └── test_cases.xlsx
└── visualizations/
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