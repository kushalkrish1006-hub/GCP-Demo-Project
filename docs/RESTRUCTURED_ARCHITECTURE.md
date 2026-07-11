# GCP Data Engineering End-to-End Project Architecture

## Overview
Production-grade E-commerce Analytics Platform on GCP covering batch processing, streaming ingestion, orchestration, monitoring, security and BI dashboards.

### Business Requirements
- 50M orders/day capacity
- Near real-time analytics
- Historical reporting capabilities
- Scalable architecture
- Data quality and governance
- Production-grade monitoring and security

---

## Project Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   GCP DATA ENGINEERING PLATFORM                        │
└─────────────────────────────────────────────────────────────────────────┘

SOURCE SYSTEMS
├── Faker/API (Test Data Generation)
├── Orders API
├── Customer Master
├── Product Master
├── CDC Feeds
└── Batch Files

                              ↓

DATA INGESTION LAYER
├── Batch: CSV/Parquet → GCS Bronze
├── Streaming: Pub/Sub → Dataflow
└── API: Direct integrations

                              ↓

DATA LAKE (GCS)
├── Bronze Layer (Raw Data)
├── Silver Layer (Cleansed Data)
└── Gold Layer (Business-Ready Data)

                              ↓

PROCESSING LAYER
├── Dataproc (PySpark) → Batch Processing
├── Dataflow → Streaming Processing
└── BigQuery → Data Warehouse

                              ↓

DATA WAREHOUSE (BigQuery)
├── Conformed Dimensions (Customer, Product, Date, Payment)
├── Fact Tables (Orders, Transactions, Snapshots)
├── Slowly Changing Dimensions (SCD Type 1/2)
└── Materialized Views (Aggregations)

                              ↓

ANALYTICS & BI
└── Looker Studio → Dashboards & Reports

                              ↓ (Orchestration)

COMPOSER/AIRFLOW
└── DAGs, Sensors, Operators, Scheduling

                              ↓ (Monitoring)

OBSERVABILITY
├── Cloud Monitoring
├── Cloud Logging
└── Alert Management
```

---

## Directory Structure

```
GCP-Demo-Project/
│
├── src/                                [SOURCE CODE]
│   ├── data_ingestion/                → Data Ingestion Layer
│   │   ├── batch/                     → Batch processing (CSV/Parquet)
│   │   ├── streaming/                 → Streaming (Pub/Sub, Kafka)
│   │   └── api/                       → API integrations
│   │
│   ├── data_processing/               → Transformation & Processing
│   │   ├── transformations/           → Business logic transformations
│   │   ├── spark_jobs/                → PySpark jobs for Dataproc
│   │   └── dataflow/                  → Apache Beam/Dataflow pipelines
│   │
│   ├── data_quality/                  → Data Quality & Validation
│   │   ├── validation/                → Data validation rules
│   │   ├── monitoring/                → Quality monitoring
│   │   └── testing/                   → Data tests & assertions
│   │
│   ├── data_storage/                  → Data Warehouse Management
│   │   ├── schemas/                   → BigQuery schemas
│   │   ├── queries/                   → SQL queries & templates
│   │   └── migrations/                → Schema migrations
│   │
│   ├── orchestration/                 → Workflow Orchestration
│   │   ├── dags/                      → Composer/Airflow DAGs
│   │   ├── operators/                 → Custom operators
│   │   └── sensors/                   → Custom sensors
│   │
│   ├── security/                      → Security & IAM
│   │   ├── iam/                       → IAM policies & roles
│   │   ├── secrets/                   → Secret management
│   │   └── audit/                     → Audit logging & compliance
│   │
│   ├── infrastructure/                → IaC & Deployment
│   │   ├── terraform/                 → Terraform modules
│   │   ├── deployment/                → Deployment scripts
│   │   └── cicd/                      → CI/CD pipelines (Cloud Build)
│   │
│   ├── analytics/                     → Analytics & BI
│   │   ├── looker/                    → Looker Studio configs
│   │   ├── dashboards/                → Dashboard definitions
│   │   └── reports/                   → Report templates
│   │
│   └── utils/                         → Utilities & Helpers
│       ├── logging/                   → Logging utilities
│       ├── config/                    → Configuration management
│       └── helpers/                   → Helper functions
│
├── configs/                           [CONFIGURATION FILES]
│   ├── gcp/                           → GCP project configs
│   ├── spark/                         → Spark configuration
│   ├── airflow/                       → Airflow configuration
│   └── databases/                     → Database connection configs
│
├── data/                              [DATA LAKE STRUCTURE]
│   ├── bronze/                        → Raw data layer
│   ├── silver/                        → Cleansed data layer
│   └── gold/                          → Business-ready layer
│
├── schemas/                           [BIGQUERY SCHEMAS]
│   ├── customers/                     → Customer dimension schema
│   ├── products/                      → Product dimension schema
│   ├── orders/                        → Order fact table schema
│   ├── payments/                      → Payment dimension schema
│   └── shipments/                     → Shipment fact table schema
│
├── tests/                             [TESTING]
│   ├── unit/                          → Unit tests
│   ├── integration/                   → Integration tests
│   └── e2e/                           → End-to-end tests
│
├── docs/                              [DOCUMENTATION]
│   ├── architecture/                  → Architecture diagrams & docs
│   ├── api_specs/                     → API specifications
│   ├── runbooks/                      → Operational runbooks
│   ├── RESTRUCTURED_ARCHITECTURE.md   → This file
│   └── GCP_Data_Engineering_Masterclass_25_Slides.pptx
│
├── notebooks/                         [JUPYTER NOTEBOOKS]
│   ├── 01_gcp_basics.ipynb
│   ├── 02_data_processing.ipynb
│   └── 03_analysis.ipynb
│
├── README.md                          → Main README
└── requirements.txt                   → Python dependencies

```

---

## Core Components

### 1. Data Ingestion Layer
**Location**: `src/data_ingestion/`

#### Batch Ingestion
- Load CSV/Parquet files from GCS
- File format conversions
- Schema validation
- Error handling and retries

#### Streaming Ingestion
- Pub/Sub → Dataflow pipelines
- Real-time data processing
- Windowing and watermarking
- Late arriving data handling

#### API Integration
- Direct API calls
- OAuth/Authentication
- Rate limiting and throttling
- Error recovery

---

### 2. Data Processing Layer
**Location**: `src/data_processing/`

#### PySpark Transformations
- Data cleaning and deduplication
- Joins and aggregations
- Window functions
- Data type conversions

#### Spark Optimization
- Partitioning strategy
- Broadcast joins
- Caching strategies
- Catalyst optimizer tuning

#### Dataflow Pipelines
- Apache Beam transformations
- Windowing (Fixed, Sliding, Session)
- Watermarking and triggering
- Dead letter queue handling

---

### 3. Data Quality Layer
**Location**: `src/data_quality/`

#### Validation Rules
- Schema validation
- Business rule checks
- Null/duplicate handling
- Data type validation

#### Monitoring
- Data freshness checks
- Row count validations
- Statistical checks
- Anomaly detection

#### Testing
- Unit tests for transformations
- Integration tests for pipelines
- Data quality assertions
- E2E pipeline tests

---

### 4. Data Storage (BigQuery)
**Location**: `src/data_storage/` & `schemas/`

#### Star Schema Design
- **Fact Tables**: Orders, Transactions, Snapshots
- **Dimensions**: Customer, Product, Date, Payment
- **Conformed Dimensions**: Shared across fact tables

#### Slowly Changing Dimensions
- **SCD Type 1**: Overwrite historical data
- **SCD Type 2**: Preserve historical versions
- Effective dating and surrogate keys

#### BigQuery Optimization
- Partitioning by date/order ID
- Clustering by customer/product
- Materialized views for aggregations
- MERGE statements for incremental loads

---

### 5. Orchestration (Composer/Airflow)
**Location**: `src/orchestration/`

#### DAG Management
- Dependency management
- Task scheduling
- Retry policies
- SLA monitoring

#### Custom Operators
- GCP-specific operators
- Dataproc job submission
- BigQuery operations
- GCS file operations

#### Sensors
- File sensors (GCS)
- Time-based sensors
- External task sensors
- SQL-based sensors

---

### 6. Security & IAM
**Location**: `src/security/`

#### Identity & Access Management
- Service accounts
- Custom roles
- Least privilege principle
- Resource-level permissions

#### Secrets Management
- API keys storage
- Database credentials
- Encryption keys
- Audit trail

#### Compliance & Audit
- Activity logging
- Data lineage tracking
- Compliance reports
- Security incidents

---

### 7. Infrastructure as Code
**Location**: `src/infrastructure/`

#### Terraform Modules
- GCS bucket creation
- BigQuery dataset setup
- Pub/Sub topics
- Dataproc cluster configuration
- IAM policies

#### CI/CD Pipeline
- Cloud Build configuration
- Automated testing
- Deployment pipelines
- Rollback procedures

---

### 8. Analytics & BI
**Location**: `src/analytics/`

#### Looker Studio Integration
- Dashboard configurations
- Data source connections
- Visualization definitions
- Report scheduling

#### Custom Reports
- Standard reports
- Ad-hoc queries
- Export configurations
- Email scheduling

---

### 9. Utilities
**Location**: `src/utils/`

#### Logging
- Structured logging
- Log aggregation
- Performance metrics
- Error tracking

#### Configuration
- Environment-based configs
- Secrets management
- Feature flags
- Service discovery

#### Helpers
- Common functions
- Data utilities
- String operations
- Date/time utilities

---

## Data Pipeline Workflow

### Batch Processing Flow
```
Raw Data (GCS Bronze)
    ↓
Data Quality Validation
    ↓
PySpark Transformations (Dataproc)
    ↓
Data Quality Checks
    ↓
Silver Layer (Cleansed Data)
    ↓
BigQuery Load (Fact/Dimension)
    ↓
Materialized Views Refresh
    ↓
Looker Studio Dashboard
```

### Streaming Processing Flow
```
Source Systems (API/CDC)
    ↓
Pub/Sub Topic
    ↓
Dataflow Pipeline
    ↓
Windowing & Aggregation
    ↓
BigQuery Real-time Insert
    ↓
Looker Studio Live Dashboard
```

### Complete Orchestration
```
Composer DAG
├── Task 1: Check data availability (Sensor)
├── Task 2: Ingest data from source
├── Task 3: Validate data quality
├── Task 4: Run PySpark transformations
├── Task 5: Load to BigQuery
├── Task 6: Refresh materialized views
├── Task 7: Update Looker dashboards
└── Task 8: Send notifications
```

---

## GCP Services Used

| Service | Purpose | Component |
|---------|---------|-----------|
| **GCS** | Data lake storage | Bronze/Silver/Gold layers |
| **Pub/Sub** | Real-time messaging | Streaming ingestion |
| **Dataflow** | Stream processing | Real-time transformations |
| **Dataproc** | Spark cluster | Batch processing |
| **BigQuery** | Data warehouse | OLAP analytics |
| **Composer** | Workflow orchestration | DAG scheduling |
| **IAM** | Access control | Security |
| **Secret Manager** | Secrets storage | Credentials |
| **Cloud Monitoring** | Metrics & alerts | Observability |
| **Cloud Logging** | Log aggregation | Debugging |
| **Looker Studio** | BI & Dashboards | Analytics |

---

## Dataset Design

### Dimensions
- **Customers**: Customer ID, Name, Email, Address, Segment
- **Products**: Product ID, Name, Category, Price, Supplier
- **Payments**: Payment Method, Provider, Transaction Type
- **Dates**: Date, Year, Month, Quarter, Day of Week

### Facts
- **Orders**: Order ID, Customer ID, Product ID, Amount, Quantity, Date
- **Payments**: Payment ID, Order ID, Amount, Status, Timestamp
- **Shipments**: Shipment ID, Order ID, Status, Delivery Date

---

## Implementation Roadmap

### Week 1: Foundation
- [ ] GCP project setup
- [ ] Service account creation
- [ ] IAM roles configuration
- [ ] GCS buckets setup (Bronze/Silver/Gold)

### Week 2: Data Ingestion
- [ ] Batch ingestion pipeline
- [ ] Pub/Sub topic creation
- [ ] Dataflow streaming pipeline
- [ ] API integration

### Week 3: Processing
- [ ] PySpark jobs development
- [ ] Data quality checks
- [ ] Transformation logic
- [ ] Dataproc cluster setup

### Week 4: Storage & Analytics
- [ ] BigQuery dataset creation
- [ ] Dimension & fact tables
- [ ] Materialized views
- [ ] Looker Studio dashboards

### Week 5: Orchestration
- [ ] Composer DAG development
- [ ] Scheduling configuration
- [ ] Sensor creation
- [ ] Error handling

### Week 6: Security & Monitoring
- [ ] IAM policies
- [ ] Secret management
- [ ] Monitoring & alerts
- [ ] Audit logging

### Week 7-8: Testing & Deployment
- [ ] Unit testing
- [ ] Integration testing
- [ ] E2E testing
- [ ] Production deployment

---

## Next Steps

1. Review the PPTX slides for detailed content
2. Set up GCP project and credentials
3. Create GCS buckets for data lake
4. Begin batch ingestion implementation
5. Develop PySpark transformation jobs
6. Configure BigQuery datasets and tables
7. Create Composer DAGs for orchestration
8. Set up monitoring and alerting

---

## References

- [GCP Data Engineering Path](https://cloud.google.com/architecture/data-engineering)
- [BigQuery Best Practices](https://cloud.google.com/bigquery/docs/best-practices)
- [Dataproc Documentation](https://cloud.google.com/dataproc/docs)
- [Composer Documentation](https://cloud.google.com/composer/docs)
- [Dataflow Documentation](https://cloud.google.com/dataflow/docs)

---

*Last Updated: July 12, 2026*
*Restructured based on: GCP Data Engineering Masterclass 25 Slides*
