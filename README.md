# GCP E-Commerce Analytics Platform

A **production-grade, end-to-end data engineering platform** built on Google Cloud Platform (GCP) that delivers real-time and historical insights from e-commerce operations. This platform consolidates order, customer, product, and payment data into a centralized analytics hub enabling data-driven decision-making across the organization.

---

## 🎯 Project Overview

### Business Objectives

This platform is designed to:

1. **Enable Real-Time Analytics** - Provide near real-time visibility into order processing, payment status, and customer activity
2. **Support Historical Reporting** - Maintain 7+ years of historical data for trend analysis and compliance
3. **Achieve Scalability** - Handle 50+ million orders per day with high performance and reliability
4. **Establish Data Governance** - Implement centralized data quality standards and compliance frameworks
5. **Reduce Operational Complexity** - Automate pipelines and provide self-service analytics capabilities

### Key Features

- ✅ **Batch & Streaming Ingestion** - Support for CSV/Parquet files and real-time Pub/Sub streams
- ✅ **Data Lake Architecture** - Bronze (raw) → Silver (cleansed) → Gold (business-ready) layers
- ✅ **Advanced Processing** - PySpark transformations and Apache Beam streaming pipelines
- ✅ **Enterprise Data Warehouse** - BigQuery with star schema and slowly changing dimensions
- ✅ **Workflow Orchestration** - Cloud Composer/Airflow for automated pipeline scheduling
- ✅ **Real-Time Analytics** - Live dashboards and alerts powered by Looker Studio
- ✅ **Production-Grade Security** - IAM, encryption, audit logging, and compliance (GDPR, SOC 2)
- ✅ **Monitoring & Observability** - Cloud Monitoring, logging, and custom data quality checks

---

## 📊 Capacity & Performance Targets

| Metric | Target |
|--------|--------|
| **Daily Order Volume** | 50+ million orders/day |
| **Query Response Time** | < 30 seconds (p95) |
| **Data Freshness** | < 2 hours (batch), < 5 minutes (streaming) |
| **Platform Availability** | 99.5% SLA uptime |
| **Query Cost** | < $0.01 per query |
| **Concurrent Users** | 100+ simultaneous analysts |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│               GCP E-COMMERCE ANALYTICS PLATFORM                 │
└─────────────────────────────────────────────────────────────────┘

SOURCE SYSTEMS
├── Orders API & Batch Files
├── Customer Master & CDC Feeds
├── Product Catalog & Inventory
├── Payment Transactions
└── Shipment & Fulfillment Data
              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                         │
├── Batch (CSV/Parquet → GCS Bronze)                             │
├── Streaming (Pub/Sub → Dataflow)                               │
└── APIs (Direct integrations)                                   │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│           DATA LAKE (GCS) - Layered Architecture               │
├── Bronze Layer: Raw data (unchanged)                           │
├── Silver Layer: Cleansed & validated data                      │
└── Gold Layer: Business-ready aggregations                      │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   PROCESSING LAYER                              │
├── PySpark Jobs (Batch) - Dataproc                              │
├── Apache Beam (Streaming) - Dataflow                           │
└── Data Quality Checks & Validation                             │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│              DATA WAREHOUSE (BigQuery)                          │
├── Dimensions: Customer, Product, Payment, Date                 │
├── Facts: Orders, Payments, Shipments                           │
├── Materialized Views: Pre-aggregated data                       │
└── Conformed Schemas: SCD Type 1 & 2                            │
└─────────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────────┐
│              ANALYTICS & BI (Looker Studio)                    │
├── Executive Dashboards (KPIs, Revenue, Trends)                 │
├── Operational Views (Orders, Fulfillment, Payments)            │
└── Self-Service Analytics (Data Discovery, Ad-Hoc Queries)      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│         ORCHESTRATION & MONITORING (Background)                │
├── Cloud Composer (DAG Scheduling & Orchestration)              │
├── Cloud Monitoring & Logging                                   │
└── Alert Management & Incident Response                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
GCP-Demo-Project/
│
├── src/                                 # Source Code
│   ├── data_ingestion/                 # Batch & streaming ingestion
│   ├── data_processing/                # Spark & Beam transformations
│   ├── data_quality/                   # Validation & monitoring
│   ├── data_storage/                   # BigQuery schemas & queries
│   ├── orchestration/                  # Composer DAGs
│   ├── security/                       # IAM & secrets management
│   ├── infrastructure/                 # Terraform IaC
│   ├── analytics/                      # Looker configurations
│   └── utils/                          # Logging, config, helpers
│
├── configs/                             # Configuration Files
│   ├── gcp/                            # GCP project configs
│   ├── spark/                          # Spark settings
│   ├── airflow/                        # Airflow configuration
│   └── databases/                      # Database connections
│
├── data/                                # Data Lake Structure
│   ├── bronze/                         # Raw data layer
│   ├── silver/                         # Cleansed data layer
│   └── gold/                           # Business-ready layer
│
├── schemas/                             # BigQuery Schemas
│   ├── customers/                      # Customer dimensions
│   ├── products/                       # Product dimensions
│   ├── orders/                         # Order fact tables
│   ├── payments/                       # Payment dimensions
│   └── shipments/                      # Shipment fact tables
│
├── tests/                               # Test Suites
│   ├── unit/                           # Unit tests
│   ├── integration/                    # Integration tests
│   └── e2e/                            # End-to-end tests
│
├── docs/                                # Documentation
│   ├── PROJECT_OVERVIEW.md             # Project overview
│   ├── RESTRUCTURED_ARCHITECTURE.md    # Detailed architecture
│   ├── DATA_PIPELINE_ARCHITECTURE.md   # Pipeline design
│   └── api_specs/                      # API documentation
│
├── notebooks/                           # Jupyter Notebooks
│   ├── 01_gcp_basics.ipynb
│   ├── 02_data_processing.ipynb
│   └── 03_analysis.ipynb
│
├── business_requirement.md              # Business Requirements Document
├── README.md                            # This file
└── requirements.txt                     # Python dependencies
```

---

## 🏢 Stakeholder Requirements

### Executive Leadership
- High-level KPI dashboards for decision-making
- Monthly/quarterly business performance reports
- Predictive insights for revenue forecasting

### Finance Team
- Real-time revenue tracking and payment reconciliation
- Cost analytics and margin analysis by segment
- Fraud detection and anomaly alerts

### Marketing Team
- Customer segmentation and behavioral analytics
- Campaign performance tracking and ROI measurement
- Customer lifetime value (CLV) and churn prediction

### Operations Team
- Order fulfillment tracking and shipment analytics
- Inventory level monitoring and demand forecasting
- Performance SLA tracking and incident alerts

### Data Teams
- Complete data lineage and metadata management
- Self-service data exploration and discovery
- APIs for programmatic data access

---

## 💾 Data Model

### Dimensions (Business Context)
- **Customer**: Demographics, segments, lifetime value, SCD Type 2
- **Product**: Catalog, categories, pricing, suppliers
- **Payment**: Payment methods, providers, processing terms
- **Date**: Fiscal periods, holidays, day attributes

### Facts (Business Events)
- **Orders**: Order details, items, amounts, dates, status
- **Payments**: Payment transactions, amounts, reconciliation status
- **Shipments**: Fulfillment tracking, delivery details, carrier info

### Data Retention
- Fact Tables: 7+ years
- Dimension Tables: Current + 2 years history
- Staging: 30 days
- Logs: 90 days

---

## 🔒 Security & Compliance

### Security Features
- ✅ **Encryption**: AES-256 at rest, TLS 1.2+ in transit
- ✅ **Access Control**: RBAC with least privilege principle
- ✅ **Authentication**: Service accounts + enterprise IAM
- ✅ **Data Protection**: PII masking and column-level security
- ✅ **Audit Logging**: Complete audit trails for compliance

### Compliance Frameworks
- **GDPR**: Right to erasure, data portability, consent management
- **SOC 2 Type II**: Access controls, encryption, audit logging
- **Data Residency**: Region-specific data storage
- **Retention Policies**: Legal hold and disposal procedures

---

## 📈 Success Metrics

### Business Metrics
| Metric | Target |
|--------|--------|
| Decision-Making Latency | 80% reduction |
| Analytics Query Volume | 10,000+ queries/day |
| Data Accuracy | > 99.5% |
| User Satisfaction | > 4/5 rating |

### Technical Metrics
| Metric | Target |
|--------|--------|
| Pipeline Success Rate | > 99% |
| Query Performance (p95) | < 30 seconds |
| Platform Availability | 99.5% uptime |
| RTO/RPO | < 4 hours / < 1 hour |

---

## 🚀 Implementation Roadmap

### Week 1-2: Foundation
- GCP project setup and IAM configuration
- Data governance framework definition
- Source system discovery
- Team training on GCP tools

### Week 3-4: Ingestion & Storage
- Batch ingestion pipeline
- Streaming infrastructure setup
- BigQuery dataset creation
- Data quality framework

### Week 5-6: Processing & Transformation
- PySpark transformation jobs
- Data quality validation rules
- Dimension and fact table population
- Materialized views

### Week 7: Orchestration & Monitoring
- Cloud Composer DAG development
- Monitoring and alerting setup
- Security and IAM policies
- Documentation and runbooks

### Week 8: Analytics & Launch
- Looker Studio dashboard development
- User acceptance testing
- Team training and documentation
- Production deployment

---

## 🛠️ Technology Stack

### Cloud Services (GCP)
- **GCS**: Data Lake Storage (Bronze/Silver/Gold)
- **Pub/Sub**: Real-time message streaming
- **Dataflow**: Apache Beam stream processing
- **Dataproc**: Managed Spark clusters
- **BigQuery**: Petabyte-scale data warehouse
- **Cloud Composer**: Orchestration (Airflow)
- **Cloud Monitoring**: Metrics and alerting
- **Cloud Logging**: Centralized log aggregation
- **Secret Manager**: Secrets and credentials
- **IAM**: Identity and access management

### Processing & Languages
- **Python**: Primary development language
- **PySpark**: Batch data processing
- **Apache Beam**: Stream data processing
- **SQL**: BigQuery analytics and transformations

### BI & Visualization
- **Looker Studio**: Interactive dashboards and reports
- **BigQuery**: Query engine and data source

---

## 📚 Documentation

For detailed information, refer to:

- **[business_requirement.md](./business_requirement.md)** - Complete business requirements and success criteria
- **[docs/RESTRUCTURED_ARCHITECTURE.md](./docs/RESTRUCTURED_ARCHITECTURE.md)** - Detailed technical architecture
- **[docs/PROJECT_OVERVIEW.md](./docs/PROJECT_OVERVIEW.md)** - Project overview and directory structure
- **[docs/DATA_PIPELINE_ARCHITECTURE.md](./docs/DATA_PIPELINE_ARCHITECTURE.md)** - Data pipeline design

---

## 🎓 Getting Started

### Prerequisites
- Python 3.8+ installed
- GCP project with billing enabled
- Service account credentials configured
- Basic familiarity with SQL and cloud concepts

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/Project-01-GCP-Ecommerce-Analytics-Platform.git
   cd Project-01-GCP-Ecommerce-Analytics-Platform
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

3. **Configure GCP credentials**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```

4. **Explore the codebase**
   - Start with `docs/PROJECT_OVERVIEW.md`
   - Review architecture in `docs/RESTRUCTURED_ARCHITECTURE.md`
   - Examine schemas in `schemas/` directory

5. **Review notebooks** for hands-on examples
   ```bash
   jupyter notebook notebooks/01_gcp_basics.ipynb
   ```

---

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run all tests with coverage
pytest tests/ --cov=src/ --cov-report=html
```

---

## 📋 Development Workflow

### Creating a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### Making Changes
```bash
# Make your changes
git add .
git commit -m "Description of changes"

# Push to remote
git push origin feature/your-feature-name
```

### Creating a Pull Request
- Create PR against `main` branch
- Ensure all tests pass
- Request code review from team members
- Merge after approval

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support & Questions

For questions or issues:
1. Check the [docs](./docs/) directory
2. Review existing GitHub issues
3. Create a new issue with detailed description
4. Contact the data engineering team

---

## 📄 License

This project is part of the internal GCP initiative. Please refer to your organization's licensing policies.

---

## 👥 Team

**Data Engineering Team**
- Data Architect
- Lead Data Engineers (2)
- Data Engineers (3)

---

## 📝 Document Information

| Item | Details |
|------|---------|
| **Last Updated** | July 12, 2026 |
| **Version** | 1.0 |
| **Status** | Active Development |
| **Document** | [business_requirement.md](./business_requirement.md) |

---

*For the latest architecture details and implementation roadmap, see [business_requirement.md](./business_requirement.md)*
