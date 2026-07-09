# Data Pipeline Architecture - GCP Demo Project

## Overview
This document describes the complete data pipeline architecture for the GCP Demo Project. The pipeline automates data flow from generation to analytics visualization using GCP services and Airflow orchestration.

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA PIPELINE FLOW                             │
└─────────────────────────────────────────────────────────────────────────┘

  [Faker Data]
       ↓
  [MySQL DB]  ← generate_faker_data.py
       ↓
  [MySQL to GCS] ← mysql_to_gcs.py
       ↓
  [GCS Bucket]
       ↓
  [GCS to BigQuery] ← gcs_to_bigquery.py
       ↓
  [BigQuery Table]
       ↓
  [DataProc/PySpark] ← pyspark_jobs.py
       ↓
  [Processed Data]
       ↓
  [Looker Studio Dashboard] ← Analytics & Visualization
       
   ↑─────────────────────────────────────────────────↑
            AIRFLOW DAGs - Orchestration & Automation
```

## Directory Structure

```
GCP-Demo-Project/
│
├── src/                                    # Source code for pipeline components
│   ├── __init__.py
│   ├── faker_data_generator/              # Step 1: Generate fake data
│   │   ├── __init__.py
│   │   └── generate_faker_data.py
│   │
│   ├── mysql_to_gcs/                      # Step 2: MySQL → GCS
│   │   ├── __init__.py
│   │   └── mysql_to_gcs.py
│   │
│   ├── gcs_to_bigquery/                   # Step 3: GCS → BigQuery
│   │   ├── __init__.py
│   │   └── gcs_to_bigquery.py
│   │
│   ├── dataproc_jobs/                     # Step 4: PySpark/DataProc jobs
│   │   ├── __init__.py
│   │   ├── pyspark_jobs.py
│   │   └── transformations.py
│   │
│   ├── scripts/                           # Utility scripts
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   └── logging_utils.py
│   │
│   └── tests/                             # Unit tests
│       └── test_*.py
│
├── airflow/                                # Airflow orchestration
│   ├── __init__.py
│   ├── dags/                              # DAG definitions
│   │   ├── __init__.py
│   │   ├── data_pipeline_dag.py           # Main orchestration DAG
│   │   └── backup_dag.py                  # Backup/recovery DAG
│   ├── plugins/                           # Custom operators/hooks
│   │   ├── __init__.py
│   │   └── custom_operators.py
│   └── logs/                              # Airflow logs
│
├── configs/                                # Configuration files
│   ├── gcp_config.yaml                    # GCP credentials & project config
│   ├── mysql_config.yaml                  # MySQL connection config
│   ├── pipeline_config.yaml               # Pipeline parameters
│   └── airflow_config.yaml                # Airflow configuration
│
├── bigquery/                               # BigQuery schemas & queries
│   ├── schemas/
│   │   └── users_schema.json
│   └── queries/
│       ├── data_quality_checks.sql
│       └── analytics_queries.sql
│
├── gcs/                                    # GCS bucket configs
│   ├── upload_configs.yaml
│   └── bucket_structure.md
│
├── dataproc/                               # DataProc cluster configs
│   ├── cluster_config.yaml
│   └── spark_job_config.yaml
│
├── looker_studio/                          # Looker Studio dashboards
│   ├── dashboard_config.json
│   └── datasource_mappings.yaml
│
├── docs/                                   # Documentation
│   ├── DATA_PIPELINE_ARCHITECTURE.md       # This file
│   ├── SETUP.md
│   ├── GCP_SERVICES.md
│   └── AIRFLOW_SETUP.md
│
└── requirements.txt                        # Python dependencies

```

## Pipeline Components

### 1. Faker Data Generator
**Location**: `src/faker_data_generator/generate_faker_data.py`
- Generates 50+ fake user records with realistic data
- Inserts data into MySQL database
- Output: MySQL table with user data

### 2. MySQL to GCS Uploader
**Location**: `src/mysql_to_gcs/mysql_to_gcs.py`
- Reads data from MySQL database
- Formats data (CSV/JSON/Parquet)
- Uploads to Google Cloud Storage bucket
- Output: GCS bucket with raw data files

### 3. GCS to BigQuery Loader
**Location**: `src/gcs_to_bigquery/gcs_to_bigquery.py`
- Reads files from GCS bucket
- Creates/updates BigQuery table
- Handles schema management
- Output: BigQuery table with imported data

### 4. DataProc/PySpark Jobs
**Location**: `src/dataproc_jobs/pyspark_jobs.py`
- Reads data from BigQuery
- Applies transformations and aggregations
- Creates processed datasets
- Output: Processed data for analytics

### 5. Looker Studio Dashboard
**Location**: `looker_studio/`
- Connects to BigQuery as data source
- Creates visualizations and dashboards
- Real-time analytics and KPIs

### 6. Airflow Orchestration
**Location**: `airflow/dags/`
- Orchestrates entire pipeline
- Schedules and monitors tasks
- Handles error recovery
- Logs and monitoring

## Workflow Steps

### Step 1: Generate Fake Data
```bash
python src/faker_data_generator/generate_faker_data.py
```
- Generates 50 fake user records
- Inserts into MySQL (gcp_demo.users table)

### Step 2: Extract from MySQL
```bash
python src/mysql_to_gcs/mysql_to_gcs.py
```
- Extracts data from MySQL
- Uploads to GCS bucket (gs://your-bucket/raw-data/)

### Step 3: Load to BigQuery
```bash
python src/gcs_to_bigquery/gcs_to_bigquery.py
```
- Reads from GCS
- Creates BigQuery table (gcp_demo_dataset.users)

### Step 4: Transform with PySpark
```bash
python src/dataproc_jobs/pyspark_jobs.py
```
- Runs on DataProc cluster
- Creates aggregated/transformed tables

### Step 5: Visualize in Looker Studio
- Connect Looker Studio to BigQuery
- Create dashboard with processed data

### Step 6: Automate with Airflow
```bash
airflow dags list
airflow dags trigger data_pipeline_dag
```
- Automates entire pipeline
- Runs on schedule (daily/hourly)

## Configuration Files

### gcp_config.yaml
```yaml
project_id: your-gcp-project
region: us-central1
credentials_path: /path/to/credentials.json

gcs:
  bucket_name: your-bucket
  raw_data_folder: raw-data/

bigquery:
  dataset: gcp_demo_dataset
  table: users

dataproc:
  cluster_name: gcp-demo-cluster
  zone: us-central1-a
```

### mysql_config.yaml
```yaml
host: localhost
port: 3306
user: root
password: your_password
database: gcp_demo
```

## Dependencies

- Python 3.8+
- mysql-connector-python
- faker
- google-cloud-storage
- google-cloud-bigquery
- google-cloud-dataproc
- pyspark
- apache-airflow
- pandas
- pyarrow

## Running the Pipeline

### Manual Execution
```bash
# 1. Generate data
python src/faker_data_generator/generate_faker_data.py

# 2. Upload to GCS
python src/mysql_to_gcs/mysql_to_gcs.py

# 3. Load to BigQuery
python src/gcs_to_bigquery/gcs_to_bigquery.py

# 4. Transform with PySpark
python src/dataproc_jobs/pyspark_jobs.py
```

### Automated Execution (Airflow)
```bash
# Start Airflow
airflow webserver
airflow scheduler

# Trigger DAG
airflow dags trigger data_pipeline_dag
```

## Monitoring & Logging

- **Airflow Web UI**: Monitor DAG execution, task status, logs
- **GCS**: Track uploaded files and versions
- **BigQuery**: View table schemas, row counts, query history
- **DataProc**: Monitor job execution and cluster status
- **Looker Studio**: Real-time dashboard analytics

## Error Handling

- Automatic retries on failures
- Data validation checks
- Logging and alerting
- Backup and recovery procedures

## Next Steps

1. Update configuration files with your GCP credentials
2. Create GCS bucket and BigQuery dataset
3. Set up Airflow environment
4. Test each component individually
5. Deploy complete pipeline
6. Set up monitoring and alerts

---
*Last Updated: July 9, 2026*
