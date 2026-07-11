# GCP E-Commerce Analytics Platform - Data Model

## Overview

This document defines the complete BigQuery data model for the GCP E-Commerce Analytics Platform. The model is built on a star schema with conformed dimensions and fact tables, supporting high-volume transactional and analytical queries.

**Capacity Target**: 50M+ orders/day
**Query Performance Target**: < 30 seconds for 95th percentile queries
**Data Retention Policy**: 7+ years for fact tables, 2-3 years history for dimensions

---

## Dimension Tables

Dimensions are slowly-changing dimensions (SCD) supporting historical tracking and point-in-time analysis.

### 1. DIM_CUSTOMER

Tracks customer information with historical versions for customer profile changes.

| Column | Data Type | Key | SCD Type | Description |
|--------|-----------|-----|----------|-------------|
| customer_id | STRING | PK | - | Unique customer identifier (surrogate key) |
| customer_source_id | STRING | - | - | Original customer ID from source system |
| first_name | STRING | - | 2 | Customer first name |
| last_name | STRING | - | 2 | Customer last name |
| email | STRING | - | 2 | Primary email address |
| phone | STRING | - | 2 | Contact phone number |
| date_of_birth | DATE | - | 1 | Customer DOB |
| customer_segment | STRING | - | 2 | Customer segment (Premium, Standard, Basic) |
| lifetime_value | DECIMAL(18,2) | - | 1 | Cumulative spend to date |
| account_status | STRING | - | 2 | Status (Active, Inactive, Suspended, Closed) |
| created_at | TIMESTAMP | - | - | Record creation timestamp |
| updated_at | TIMESTAMP | - | - | Last update timestamp |
| effective_date | DATE | - | - | SCD Type 2: when record became active |
| end_date | DATE | - | - | SCD Type 2: when record expired (NULL if current) |
| is_current | BOOLEAN | - | - | SCD Type 2: flags current version |

**Partitioning**: `TIMESTAMP(updated_at)` (monthly)
**Clustering**: `customer_segment`, `account_status`

---

### 2. DIM_PRODUCT

Product catalog with version tracking for changes to pricing, categories, or descriptions.

| Column | Data Type | Key | SCD Type | Description |
|--------|-----------|-----|----------|-------------|
| product_id | STRING | PK | - | Unique product identifier (surrogate key) |
| product_source_id | STRING | - | - | Original product ID from catalog system |
| product_name | STRING | - | 2 | Product name/title |
| category_id | STRING | FK | 1 | Foreign key to DIM_CATEGORY |
| subcategory_id | STRING | FK | 1 | Foreign key to DIM_SUBCATEGORY |
| sku | STRING | - | 1 | Stock keeping unit |
| upc_code | STRING | - | 1 | Universal product code |
| description | STRING | - | 2 | Product description |
| list_price | DECIMAL(18,2) | - | 2 | Manufacturer's suggested retail price |
| cost_price | DECIMAL(18,2) | - | 2 | Internal cost/acquisition price |
| supplier_id | STRING | FK | 1 | Foreign key to DIM_SUPPLIER |
| weight_kg | DECIMAL(10,3) | - | 1 | Product weight |
| dimensions | STRING | - | 1 | Product dimensions (L x W x H) |
| color | STRING | - | 2 | Product color |
| size | STRING | - | 2 | Product size |
| stock_quantity | INT64 | - | 1 | Current stock level |
| reorder_level | INT64 | - | 1 | Minimum stock level before reorder |
| is_active | BOOLEAN | - | 1 | Product active/discontinued flag |
| created_at | TIMESTAMP | - | - | Record creation timestamp |
| updated_at | TIMESTAMP | - | - | Last update timestamp |
| effective_date | DATE | - | - | SCD Type 2: when record became active |
| end_date | DATE | - | - | SCD Type 2: when record expired |
| is_current | BOOLEAN | - | - | SCD Type 2: flags current version |

**Partitioning**: `TIMESTAMP(updated_at)` (monthly)
**Clustering**: `category_id`, `supplier_id`, `is_active`

---

### 3. DIM_PAYMENT_METHOD

Reference table for available payment methods.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| payment_method_id | STRING | PK | Unique payment method identifier |
| payment_method_name | STRING | - | Human-readable name (Credit Card, Debit Card, Digital Wallet, etc.) |
| payment_category | STRING | - | Category (Card, Bank Transfer, Digital Wallet, Other) |
| processor_name | STRING | - | Payment processor (Stripe, Square, PayPal, etc.) |
| is_active | BOOLEAN | - | Whether method is currently enabled |
| created_at | TIMESTAMP | - | Record creation timestamp |

**Clustering**: `payment_category`

---

### 4. DIM_GEOGRAPHY

Geographic information for delivery locations and business regions.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| geography_id | STRING | PK | Unique geography identifier |
| country | STRING | - | Country name |
| country_code | STRING | - | ISO 3166-1 alpha-2 country code |
| state_province | STRING | - | State or province |
| state_code | STRING | - | State abbreviation |
| city | STRING | - | City name |
| postal_code | STRING | - | ZIP/postal code |
| region | STRING | - | Business region (North America, EMEA, APAC) |
| latitude | DECIMAL(10,8) | - | Geographic latitude |
| longitude | DECIMAL(11,8) | - | Geographic longitude |
| timezone | STRING | - | IANA timezone identifier |
| is_service_area | BOOLEAN | - | Whether delivery service is available |
| created_at | TIMESTAMP | - | Record creation timestamp |

**Clustering**: `country_code`, `region`, `is_service_area`

---

### 5. DIM_DATE

Conformed date dimension for all date-based analysis.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| date_id | STRING | PK | Format: YYYYMMDD (e.g., "20240115") |
| calendar_date | DATE | - | Actual date |
| year | INT64 | - | Calendar year |
| quarter | INT64 | - | Calendar quarter (1-4) |
| month | INT64 | - | Calendar month (1-12) |
| month_name | STRING | - | Month name (January, February, etc.) |
| week_of_year | INT64 | - | ISO week of year (1-53) |
| day_of_month | INT64 | - | Day of month (1-31) |
| day_of_week | INT64 | - | Day of week (1=Monday, 7=Sunday) |
| day_name | STRING | - | Day name (Monday, Tuesday, etc.) |
| is_weekend | BOOLEAN | - | Weekend flag (Saturday/Sunday) |
| is_holiday | BOOLEAN | - | Holiday flag |
| holiday_name | STRING | - | Holiday name if applicable |
| fiscal_year | INT64 | - | Fiscal year (if different from calendar) |
| fiscal_quarter | INT64 | - | Fiscal quarter |

**Clustering**: `year`, `quarter`

---

### 6. DIM_SUPPLIER

Reference table for product suppliers.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| supplier_id | STRING | PK | Unique supplier identifier |
| supplier_name | STRING | - | Supplier company name |
| supplier_type | STRING | - | Type (Manufacturer, Distributor, Retailer) |
| contact_email | STRING | - | Primary contact email |
| contact_phone | STRING | - | Primary contact phone |
| address | STRING | - | Supplier address |
| country | STRING | - | Supplier country |
| payment_terms | STRING | - | Payment terms (Net 30, Net 60, etc.) |
| is_active | BOOLEAN | - | Active/inactive status |
| created_at | TIMESTAMP | - | Record creation timestamp |
| updated_at | TIMESTAMP | - | Last update timestamp |

**Clustering**: `supplier_type`, `country`, `is_active`

---

## Fact Tables

Fact tables store business events and transactions at granular levels.

### 1. FACT_ORDERS

Transactional fact table capturing order information.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| order_id | STRING | PK | Unique order identifier |
| order_line_item_number | INT64 | PK | Line item sequence (1, 2, 3...) |
| order_date_id | STRING | FK | Foreign key to DIM_DATE |
| order_timestamp | TIMESTAMP | - | Exact order creation timestamp |
| customer_id | STRING | FK | Foreign key to DIM_CUSTOMER |
| delivery_geography_id | STRING | FK | Foreign key to DIM_GEOGRAPHY |
| product_id | STRING | FK | Foreign key to DIM_PRODUCT |
| quantity_ordered | INT64 | - | Units ordered |
| unit_price | DECIMAL(18,2) | - | Price per unit at time of order |
| line_item_total | DECIMAL(18,2) | - | quantity × unit_price |
| discount_amount | DECIMAL(18,2) | - | Discount applied to line item |
| tax_amount | DECIMAL(18,2) | - | Tax on line item |
| order_total | DECIMAL(18,2) | - | Total order value (all line items) |
| order_status | STRING | - | Order status (Pending, Confirmed, Shipped, Delivered, Cancelled, Returned) |
| shipment_date_id | STRING | FK | Foreign key to DIM_DATE for shipment |
| delivery_date_id | STRING | FK | Foreign key to DIM_DATE for delivery |
| expected_delivery_date | DATE | - | Projected delivery date |
| actual_delivery_date | DATE | - | Actual delivery date |
| is_returned | BOOLEAN | - | Return flag |
| return_reason | STRING | - | Reason for return if applicable |
| return_timestamp | TIMESTAMP | - | Return date/time |
| days_to_delivery | INT64 | - | Calculated: delivery_date - order_date |
| promotional_code | STRING | - | Applied promotional code if any |
| notes | STRING | - | Order notes or special requests |
| created_at | TIMESTAMP | - | Record creation timestamp |
| updated_at | TIMESTAMP | - | Last update timestamp |

**Partitioning**: `DATE(order_timestamp)` (daily)
**Clustering**: `customer_id`, `order_status`, `product_id`

---

### 2. FACT_PAYMENTS

Financial transactions related to orders.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| payment_id | STRING | PK | Unique payment identifier |
| order_id | STRING | FK | Foreign key to FACT_ORDERS |
| customer_id | STRING | FK | Foreign key to DIM_CUSTOMER |
| payment_date_id | STRING | FK | Foreign key to DIM_DATE |
| payment_timestamp | TIMESTAMP | - | Payment processing timestamp |
| payment_method_id | STRING | FK | Foreign key to DIM_PAYMENT_METHOD |
| amount_paid | DECIMAL(18,2) | - | Amount processed |
| payment_status | STRING | - | Status (Pending, Approved, Declined, Failed, Refunded, Chargeback) |
| currency_code | STRING | - | Currency (USD, EUR, GBP, etc.) |
| transaction_reference | STRING | - | External payment processor reference |
| gateway_response | STRING | - | Response from payment gateway |
| authorization_code | STRING | - | Payment authorization code |
| fraud_score | DECIMAL(5,2) | - | Fraud detection score (0-100) |
| is_fraud_flagged | BOOLEAN | - | Fraud flag |
| retry_count | INT64 | - | Number of retry attempts |
| original_amount | DECIMAL(18,2) | - | Original transaction amount (before adjustments) |
| fee_amount | DECIMAL(18,2) | - | Payment processor fee |
| net_amount | DECIMAL(18,2) | - | amount_paid - fee_amount |
| refund_amount | DECIMAL(18,2) | - | Refund amount if applicable |
| refund_timestamp | TIMESTAMP | - | Refund processing timestamp |
| chargeback_amount | DECIMAL(18,2) | - | Chargeback amount if applicable |
| created_at | TIMESTAMP | - | Record creation timestamp |
| updated_at | TIMESTAMP | - | Last update timestamp |

**Partitioning**: `DATE(payment_timestamp)` (daily)
**Clustering**: `customer_id`, `payment_status`, `payment_method_id`

---

### 3. FACT_SHIPMENTS

Logistics and shipping tracking information.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| shipment_id | STRING | PK | Unique shipment identifier |
| order_id | STRING | FK | Foreign key to FACT_ORDERS |
| shipment_date_id | STRING | FK | Foreign key to DIM_DATE |
| shipment_timestamp | TIMESTAMP | - | Shipment creation timestamp |
| origin_geography_id | STRING | FK | Foreign key to DIM_GEOGRAPHY (warehouse) |
| destination_geography_id | STRING | FK | Foreign key to DIM_GEOGRAPHY (delivery) |
| carrier_name | STRING | - | Shipping carrier (FedEx, UPS, DHL, etc.) |
| tracking_number | STRING | - | Carrier tracking number |
| shipment_status | STRING | - | Status (Pending, Picked, Packed, Shipped, In Transit, Delivered, Failed) |
| expected_delivery_date | DATE | - | Projected delivery |
| actual_delivery_date | DATE | - | Actual delivery date |
| shipping_cost | DECIMAL(18,2) | - | Shipping charge to customer |
| weight_kg | DECIMAL(10,3) | - | Shipment weight |
| package_count | INT64 | - | Number of packages in shipment |
| signature_required | BOOLEAN | - | Signature required flag |
| insurance_amount | DECIMAL(18,2) | - | Insurance coverage amount |
| declared_value | DECIMAL(18,2) | - | Declared item value |
| delay_days | INT64 | - | Days delayed (negative if early) |
| is_on_time | BOOLEAN | - | On-time delivery flag |
| created_at | TIMESTAMP | - | Record creation timestamp |
| updated_at | TIMESTAMP | - | Last update timestamp |

**Partitioning**: `DATE(shipment_timestamp)` (daily)
**Clustering**: `carrier_name`, `shipment_status`, `origin_geography_id`

---

## Data Lineage & ETL Flow

### Ingestion Layer (Cloud Pub/Sub → Dataflow → Staging)

```
Source Systems
├── E-Commerce Platform API
├── Payment Gateway API
├── Shipping Provider API
└── ERP System

       ↓ (Event Streaming)

Cloud Pub/Sub Topics
├── orders.events
├── payments.events
├── shipments.events
└── products.events

       ↓ (Streaming + Batch Processing)

Dataflow Pipelines
├── Transformation & Validation
├── Data Quality Checks
└── Duplicate Detection

       ↓

BigQuery Staging Layer (raw_* tables)
├── raw_orders
├── raw_payments
├── raw_shipments
├── raw_products
└── raw_customers
```

### Analytics Layer (Staging → Dimensions → Facts)

```
Staging Tables (raw_*)
       ↓
Cloud Composer (Airflow) DAGs
├── dim_load_dag (nightly)
│   ├── Load DIM_DATE (full)
│   ├── Load DIM_CUSTOMER (SCD Type 2)
│   ├── Load DIM_PRODUCT (SCD Type 2)
│   └── Load DIM_GEOGRAPHY (incremental)
│
└── fact_load_dag (hourly)
    ├── Load FACT_ORDERS (incremental)
    ├── Load FACT_PAYMENTS (incremental)
    └── Load FACT_SHIPMENTS (incremental)

       ↓

BigQuery Analytics Dataset
├── Dimension Tables (dims_*)
├── Fact Tables (facts_*)
└── Aggregation Tables (agg_*)
```

---

## Slowly Changing Dimensions (SCD) Strategy

### SCD Type 1 (Overwrite)
Applied to: `date_of_birth`, `sku`, `upc_code`, `cost_price`
- Historical values are NOT preserved
- Attribute is updated in-place
- Use case: Corrections or data that has only one valid state

**Example - DIM_PRODUCT.cost_price:**
```sql
UPDATE project.dataset.DIM_PRODUCT
SET cost_price = 150.00, updated_at = CURRENT_TIMESTAMP()
WHERE product_id = 'PROD_001';
```

### SCD Type 2 (Preserve History)
Applied to: `product_name`, `customer_segment`, `account_status`, `list_price`, `color`, `size`
- Historical versions are maintained with date ranges
- Each change creates a new row
- Use case: Tracking attribute changes over time for analysis

**Example - DIM_CUSTOMER segment change:**
```sql
-- Mark old record as expired
UPDATE project.dataset.DIM_CUSTOMER
SET end_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY),
    is_current = FALSE
WHERE customer_id = 'CUST_001' AND is_current = TRUE;

-- Insert new record
INSERT INTO project.dataset.DIM_CUSTOMER
SELECT 
  customer_id,
  customer_source_id,
  first_name,
  last_name,
  email,
  phone,
  date_of_birth,
  'Premium' as customer_segment,  -- New segment
  lifetime_value,
  account_status,
  created_at,
  CURRENT_TIMESTAMP() as updated_at,
  CURRENT_DATE() as effective_date,
  NULL as end_date,
  TRUE as is_current
FROM project.dataset.DIM_CUSTOMER
WHERE customer_id = 'CUST_001' AND is_current = TRUE;
```

---

## Relationships & Cardinality

### Dimension Key Relationships

```
DIM_CUSTOMER ──────────────┐
                            │
DIM_PRODUCT ───┐            │
               │            │
DIM_SUPPLIER ──┤            │
               │            │
DIM_CATEGORY ──┤            │
               │            ├──→ FACT_ORDERS
DIM_GEOGRAPHY ─┤            │
               │            │
DIM_PAYMENT_METHOD          │
               │            │
DIM_DATE ──────┼────────────┤
               │            │
               └─→ FACT_PAYMENTS
               │
               └─→ FACT_SHIPMENTS
```

### Cardinality Matrix

| From | To | Cardinality | Notes |
|------|----|-----------|----|
| DIM_CUSTOMER | FACT_ORDERS | 1:M | One customer has many orders |
| DIM_PRODUCT | FACT_ORDERS | 1:M | One product in many orders |
| DIM_PAYMENT_METHOD | FACT_PAYMENTS | 1:M | One method processes many payments |
| DIM_CUSTOMER | FACT_PAYMENTS | 1:M | One customer makes many payments |
| DIM_GEOGRAPHY | FACT_SHIPMENTS | 1:M | One location ships many packages |
| DIM_DATE | All Facts | 1:M | One date has many transactions |

---

## Sample Queries

### Query 1: Monthly Revenue by Customer Segment

```sql
SELECT
  DATE_TRUNC(dd.calendar_date, MONTH) as month,
  dc.customer_segment,
  COUNT(DISTINCT fo.order_id) as order_count,
  SUM(fo.line_item_total) as total_revenue,
  AVG(fo.line_item_total) as avg_order_value,
  COUNT(DISTINCT fo.customer_id) as customer_count
FROM project.dataset.FACT_ORDERS fo
JOIN project.dataset.DIM_DATE dd ON fo.order_date_id = dd.date_id
JOIN project.dataset.DIM_CUSTOMER dc ON fo.customer_id = dc.customer_id
WHERE dc.is_current = TRUE
  AND fo.order_status IN ('Delivered', 'Shipped')
  AND dd.calendar_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
GROUP BY month, customer_segment
ORDER BY month DESC, total_revenue DESC;
```

### Query 2: Product Performance - Top 10 By Revenue

```sql
SELECT
  dp.product_name,
  dp.category_id,
  COUNT(DISTINCT fo.order_id) as orders,
  SUM(fo.quantity_ordered) as units_sold,
  SUM(fo.line_item_total) as total_revenue,
  AVG(fo.line_item_total / NULLIF(fo.quantity_ordered, 0)) as avg_unit_price,
  ROUND(SUM(fo.line_item_total - (dp.cost_price * fo.quantity_ordered)), 2) as gross_profit
FROM project.dataset.FACT_ORDERS fo
JOIN project.dataset.DIM_PRODUCT dp ON fo.product_id = dp.product_id
WHERE dp.is_current = TRUE
  AND fo.order_status = 'Delivered'
  AND fo.order_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY dp.product_name, dp.category_id
ORDER BY total_revenue DESC
LIMIT 10;
```

### Query 3: Shipping Performance Analysis

```sql
SELECT
  fs.carrier_name,
  dg.state_code,
  COUNT(DISTINCT fs.shipment_id) as shipment_count,
  ROUND(AVG(fs.delay_days), 2) as avg_delay_days,
  ROUND(SUM(CASE WHEN fs.is_on_time THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as on_time_pct,
  ROUND(AVG(fs.shipping_cost), 2) as avg_shipping_cost
FROM project.dataset.FACT_SHIPMENTS fs
JOIN project.dataset.DIM_GEOGRAPHY dg ON fs.destination_geography_id = dg.geography_id
WHERE fs.actual_delivery_date IS NOT NULL
  AND fs.shipment_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY fs.carrier_name, dg.state_code
ORDER BY on_time_pct ASC;
```

### Query 4: Payment Method Performance

```sql
SELECT
  dpm.payment_method_name,
  COUNT(DISTINCT fp.payment_id) as transaction_count,
  SUM(fp.amount_paid) as total_volume,
  ROUND(AVG(fp.amount_paid), 2) as avg_transaction_amount,
  ROUND(SUM(CASE WHEN fp.payment_status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as approval_rate,
  ROUND(SUM(CASE WHEN fp.is_fraud_flagged THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fraud_flag_pct,
  ROUND(SUM(fp.fee_amount), 2) as total_fees
FROM project.dataset.FACT_PAYMENTS fp
JOIN project.dataset.DIM_PAYMENT_METHOD dpm ON fp.payment_method_id = dpm.payment_method_id
WHERE fp.payment_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 60 DAY)
GROUP BY dpm.payment_method_name
ORDER BY total_volume DESC;
```

### Query 5: Customer Lifetime Value Analysis

```sql
SELECT
  dc.customer_id,
  dc.first_name,
  dc.last_name,
  dc.customer_segment,
  COUNT(DISTINCT fo.order_id) as lifetime_orders,
  ROUND(SUM(fo.line_item_total), 2) as lifetime_value,
  ROUND(AVG(fo.line_item_total), 2) as avg_order_value,
  MAX(fo.order_timestamp) as last_order_date,
  DATE_DIFF(CURRENT_DATE(), DATE(MAX(fo.order_timestamp)), DAY) as days_since_last_order
FROM project.dataset.DIM_CUSTOMER dc
LEFT JOIN project.dataset.FACT_ORDERS fo ON dc.customer_id = fo.customer_id
WHERE dc.is_current = TRUE
GROUP BY 
  dc.customer_id,
  dc.first_name,
  dc.last_name,
  dc.customer_segment
HAVING COUNT(DISTINCT fo.order_id) > 0
ORDER BY lifetime_value DESC
LIMIT 100;
```

---

## Data Quality & Validation Rules

### Dimension Table Validations

| Table | Rule | SQL Validation | Threshold |
|-------|------|---|-----------|
| DIM_CUSTOMER | No duplicate active records | `SELECT customer_source_id, COUNT(*) FROM DIM_CUSTOMER WHERE is_current=TRUE GROUP BY 1 HAVING COUNT(*) > 1` | 0 rows |
| DIM_PRODUCT | No orphaned foreign keys | `SELECT * FROM DIM_PRODUCT WHERE supplier_id NOT IN (SELECT supplier_id FROM DIM_SUPPLIER)` | 0 rows |
| DIM_DATE | No gaps in date sequence | Check daily load completes | 100% |
| DIM_GEOGRAPHY | Valid coordinates | `SELECT * WHERE latitude NOT BETWEEN -90 AND 90` | 0 rows |

### Fact Table Validations

| Table | Rule | SQL Validation | Threshold |
|-------|------|---|-----------|
| FACT_ORDERS | Amount > 0 | `SELECT COUNT(*) FROM FACT_ORDERS WHERE line_item_total <= 0` | 0 rows |
| FACT_ORDERS | Foreign keys exist | `SELECT * FROM FACT_ORDERS WHERE customer_id NOT IN (SELECT customer_id FROM DIM_CUSTOMER WHERE is_current=TRUE)` | 0 rows |
| FACT_PAYMENTS | No duplicate payments | `SELECT transaction_reference, COUNT(*) FROM FACT_PAYMENTS GROUP BY 1 HAVING COUNT(*) > 1` | 0 rows |
| FACT_SHIPMENTS | Delivery after shipment | `SELECT COUNT(*) FROM FACT_SHIPMENTS WHERE actual_delivery_date < DATE(shipment_timestamp)` | 0 rows |

---

## Data Governance & Privacy

### PII Handling

Personally Identifiable Information (PII) in the data model:
- **DIM_CUSTOMER**: `first_name`, `last_name`, `email`, `phone`, `date_of_birth`
- **DIM_GEOGRAPHY**: `latitude`, `longitude` (quasi-PII)
- **FACT_PAYMENTS**: `authorization_code` (partial)

**Access Control**:
- PII columns are in a separate authorized dataset with row-level security
- Column-level security masks PII in non-production environments
- Audit logging tracks all PII access

### Data Retention Policy

| Table | Retention | Rationale | Deletion Strategy |
|-------|-----------|-----------|-------------------|
| FACT_ORDERS | 7+ years | Regulatory/tax compliance | Delete partitions > 7 years |
| FACT_PAYMENTS | 7+ years | Financial audit trail | Delete partitions > 7 years |
| FACT_SHIPMENTS | 3 years | Warranty/claims support | Delete partitions > 3 years |
| DIM_CUSTOMER | Current + 2 years | Customer history analysis | Archive to Cold Storage after 2 years |
| DIM_PRODUCT | Current + 2 years | Product history | Archive to Cold Storage after 2 years |
| Staging (raw_*) | 30 days | Reprocessing capability | Auto-delete daily partitions |
| Logs | 90 days | Debugging/troubleshooting | Auto-delete daily |

### GDPR Compliance

**Right to Be Forgotten**:
```sql
-- Anonymize customer
UPDATE project.dataset.DIM_CUSTOMER
SET first_name = 'REDACTED',
    last_name = 'REDACTED',
    email = CONCAT('deleted_', customer_id, '@redacted.internal'),
    phone = 'REDACTED',
    date_of_birth = NULL
WHERE customer_source_id = @customer_id;

-- Archive related fact data
INSERT INTO archive_dataset.FACT_ORDERS
SELECT * FROM project.dataset.FACT_ORDERS
WHERE customer_id = (SELECT customer_id FROM DIM_CUSTOMER WHERE customer_source_id = @customer_id);

-- Delete from analytics
DELETE FROM project.dataset.FACT_ORDERS
WHERE customer_id = (SELECT customer_id FROM DIM_CUSTOMER WHERE customer_source_id = @customer_id);
```

---

## Deployment Checklist

- [ ] BigQuery datasets created (`analytics`, `staging`, `archive`)
- [ ] Dimension table schemas validated
- [ ] Fact table schemas validated
- [ ] Service accounts and IAM roles configured
- [ ] Data quality rules deployed in Cloud Composer
- [ ] Partitioning and clustering policies applied
- [ ] Backup and recovery procedures documented
- [ ] Access controls and row-level security configured
- [ ] Data dictionary updated in metadata store
- [ ] Documentation reviewed by data governance team

---

## References

- [Business Requirements](../business_requirement.md)
- [Architecture Documentation](./RESTRUCTURED_ARCHITECTURE.md)
- [BigQuery Best Practices](https://cloud.google.com/bigquery/docs/best-practices)
- [Google Cloud Data Governance](https://cloud.google.com/architecture/framework-for-cloud-governance)

