# GCP E-Commerce Analytics Platform - Data Model

## Overview

This document defines the BigQuery data model for the GCP E-Commerce Analytics Platform. The model follows a star schema design with simplified, focused dimension and fact tables optimized for analytical queries.

**Current Scope**:
- Source Tables: Customers, Products, Orders
- Dimension Tables: dim_customer, dim_product, dim_date
- Fact Tables: fact_orders

---

## Source Tables (OLTP)

### Customers Table

Original customer data from the e-commerce platform.

| Column | Data Type | Description |
|--------|-----------|-------------|
| customer_id | STRING | Unique customer identifier (Primary Key) |
| customer_name | STRING | Customer's full name |
| email | STRING | Customer's email address |
| city | STRING | City of residence |
| state | STRING | State/Province of residence |
| signup_date | TIMESTAMP | Date customer registered |

**Sample Data**:
```
customer_id  | customer_name    | email                    | city         | state | signup_date
CUST_001     | John Doe         | john.doe@example.com     | New York     | NY    | 2024-01-15
CUST_002     | Jane Smith       | jane.smith@example.com   | Los Angeles  | CA    | 2024-02-20
```

---

### Products Table

Product catalog from the inventory management system.

| Column | Data Type | Description |
|--------|-----------|-------------|
| product_id | STRING | Unique product identifier (Primary Key) |
| product_name | STRING | Product name/title |
| category | STRING | Product category |
| price | DECIMAL(10,2) | Current retail price |
| brand | STRING | Product brand/manufacturer |

**Sample Data**:
```
product_id | product_name        | category      | price  | brand
PROD_001   | Wireless Headphones  | Electronics   | 79.99  | TechBrand
PROD_002   | USB-C Cable          | Accessories   | 12.99  | CableCo
PROD_003   | Phone Case           | Accessories   | 24.99  | ProtectMe
```

---

### Orders Table

Raw transactional order data from the e-commerce platform.

| Column | Data Type | Description |
|--------|-----------|-------------|
| order_id | STRING | Unique order identifier (Primary Key) |
| customer_id | STRING | Foreign key to Customers table |
| product_id | STRING | Foreign key to Products table |
| order_date | TIMESTAMP | Date/time of order |
| quantity | INT64 | Quantity ordered |
| amount | DECIMAL(10,2) | Total order amount |
| status | STRING | Order status (Pending, Confirmed, Shipped, Delivered, Cancelled) |

**Sample Data**:
```
order_id | customer_id | product_id | order_date           | quantity | amount  | status
ORD_001  | CUST_001    | PROD_001   | 2024-05-10 14:30:00  | 1        | 79.99   | Delivered
ORD_002  | CUST_002    | PROD_002   | 2024-05-11 09:15:00  | 2        | 25.98   | Shipped
ORD_003  | CUST_001    | PROD_003   | 2024-05-12 16:45:00  | 1        | 24.99   | Pending
```

---

## Dimension Tables (Analytics Layer)

Dimensions are optimized reference tables for analytical queries.

### DIM_CUSTOMER

Dimension table tracking customer information for analytics.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| customer_id | STRING | PK | Unique customer identifier (surrogate key) |
| customer_name | STRING | - | Customer's full name |
| email | STRING | - | Email address |
| city | STRING | - | City of residence |
| state | STRING | - | State/Province |
| signup_date | DATE | - | Customer registration date |
| customer_age_group | STRING | - | Derived: Age group for segmentation |
| created_at | TIMESTAMP | - | Record creation timestamp in analytics |
| updated_at | TIMESTAMP | - | Last update timestamp in analytics |

**DDL**:
```sql
CREATE OR REPLACE TABLE `project.dataset.DIM_CUSTOMER` (
  customer_id STRING NOT NULL,
  customer_name STRING,
  email STRING,
  city STRING,
  state STRING,
  signup_date DATE,
  customer_age_group STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY DATE(updated_at)
CLUSTER BY state, city;
```

**Sample Data**:
```
customer_id | customer_name | email              | city        | state | signup_date | customer_age_group | created_at          | updated_at
CUST_001    | John Doe      | john@example.com   | New York    | NY    | 2024-01-15  | 30-40             | 2024-01-15 10:00:00 | 2024-07-12 08:00:00
CUST_002    | Jane Smith    | jane@example.com   | Los Angeles | CA    | 2024-02-20  | 25-35             | 2024-02-20 14:30:00 | 2024-07-12 08:00:00
```

**ETL Logic** (Cloud Dataflow/Composer):
```python
# Deduplicate customers (keep latest)
SELECT DISTINCT ON (customer_id)
  customer_id,
  customer_name,
  email,
  city,
  state,
  signup_date,
  CASE 
    WHEN EXTRACT(YEAR FROM CURRENT_DATE()) - EXTRACT(YEAR FROM signup_date) >= 30 THEN '30+'
    WHEN EXTRACT(YEAR FROM CURRENT_DATE()) - EXTRACT(YEAR FROM signup_date) >= 25 THEN '25-30'
    ELSE '<25'
  END as customer_age_group,
  CURRENT_TIMESTAMP() as created_at,
  CURRENT_TIMESTAMP() as updated_at
FROM Customers
ORDER BY customer_id, signup_date DESC;
```

---

### DIM_PRODUCT

Dimension table for product catalog analytics.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| product_id | STRING | PK | Unique product identifier |
| product_name | STRING | - | Product name/title |
| category | STRING | - | Product category |
| brand | STRING | - | Brand name |
| price | DECIMAL(10,2) | - | Current retail price |
| price_range | STRING | - | Derived: Budget/Mid/Premium |
| created_at | TIMESTAMP | - | Record creation timestamp |
| updated_at | TIMESTAMP | - | Last update timestamp |

**DDL**:
```sql
CREATE OR REPLACE TABLE `project.dataset.DIM_PRODUCT` (
  product_id STRING NOT NULL,
  product_name STRING,
  category STRING,
  brand STRING,
  price DECIMAL(10,2),
  price_range STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY DATE(updated_at)
CLUSTER BY category, brand;
```

**Sample Data**:
```
product_id | product_name       | category    | brand     | price | price_range | created_at          | updated_at
PROD_001   | Wireless Headsets  | Electronics | TechBrand | 79.99 | Premium     | 2024-01-10 10:00:00 | 2024-07-12 08:00:00
PROD_002   | USB-C Cable        | Accessories | CableCo   | 12.99 | Budget      | 2024-01-10 10:05:00 | 2024-07-12 08:00:00
PROD_003   | Phone Case         | Accessories | ProtectMe | 24.99 | Mid         | 2024-01-10 10:10:00 | 2024-07-12 08:00:00
```

**ETL Logic**:
```python
SELECT DISTINCT ON (product_id)
  product_id,
  product_name,
  category,
  brand,
  price,
  CASE 
    WHEN price < 25 THEN 'Budget'
    WHEN price >= 25 AND price < 100 THEN 'Mid'
    ELSE 'Premium'
  END as price_range,
  CURRENT_TIMESTAMP() as created_at,
  CURRENT_TIMESTAMP() as updated_at
FROM Products
ORDER BY product_id, price DESC;
```

---

### DIM_DATE

Conformed date dimension for all temporal analysis.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| date_id | STRING | PK | Format: YYYYMMDD (e.g., "20240715") |
| calendar_date | DATE | - | Actual date |
| year | INT64 | - | Calendar year |
| quarter | INT64 | - | Quarter (1-4) |
| month | INT64 | - | Month (1-12) |
| month_name | STRING | - | Month name |
| week_of_year | INT64 | - | ISO week number |
| day_of_month | INT64 | - | Day of month |
| day_of_week | INT64 | - | Day of week (1=Monday, 7=Sunday) |
| day_name | STRING | - | Day name |
| is_weekend | BOOLEAN | - | Weekend flag |

**DDL**:
```sql
CREATE OR REPLACE TABLE `project.dataset.DIM_DATE` (
  date_id STRING NOT NULL,
  calendar_date DATE,
  year INT64,
  quarter INT64,
  month INT64,
  month_name STRING,
  week_of_year INT64,
  day_of_month INT64,
  day_of_week INT64,
  day_name STRING,
  is_weekend BOOLEAN
)
CLUSTER BY year, quarter;
```

**Sample Data**:
```
date_id  | calendar_date | year | quarter | month | month_name | week_of_year | day_of_month | day_of_week | day_name | is_weekend
20240715 | 2024-07-15    | 2024 | 3       | 7     | July       | 29           | 15           | 1           | Monday   | FALSE
20240716 | 2024-07-16    | 2024 | 3       | 7     | July       | 29           | 16           | 2           | Tuesday  | FALSE
20240720 | 2024-07-20    | 2024 | 3       | 7     | July       | 29           | 20           | 6           | Saturday | TRUE
```

**ETL Logic** (Generate 7 years of dates):
```python
-- Run once to populate historical dates
WITH date_range AS (
  SELECT DATE_ADD(DATE('2020-01-01'), INTERVAL i DAY) as calendar_date
  FROM UNNEST(GENERATE_ARRAY(0, 2555)) as i
)
SELECT
  FORMAT_DATE('%Y%m%d', calendar_date) as date_id,
  calendar_date,
  EXTRACT(YEAR FROM calendar_date) as year,
  EXTRACT(QUARTER FROM calendar_date) as quarter,
  EXTRACT(MONTH FROM calendar_date) as month,
  FORMAT_DATE('%B', calendar_date) as month_name,
  EXTRACT(ISOWEEK FROM calendar_date) as week_of_year,
  EXTRACT(DAY FROM calendar_date) as day_of_month,
  EXTRACT(DAYOFWEEK FROM calendar_date) as day_of_week,
  FORMAT_DATE('%A', calendar_date) as day_name,
  CASE WHEN EXTRACT(DAYOFWEEK FROM calendar_date) IN (6, 7) THEN TRUE ELSE FALSE END as is_weekend
FROM date_range
ORDER BY calendar_date;
```

---

## Fact Table (Analytics Layer)

### FACT_ORDERS

Transactional fact table capturing order events.

| Column | Data Type | Key | Description |
|--------|-----------|-----|-------------|
| order_id | STRING | PK | Unique order identifier |
| customer_id | STRING | FK | Foreign key to DIM_CUSTOMER |
| product_id | STRING | FK | Foreign key to DIM_PRODUCT |
| order_date_id | STRING | FK | Foreign key to DIM_DATE (order date) |
| order_timestamp | TIMESTAMP | - | Exact order creation timestamp |
| quantity | INT64 | - | Quantity ordered |
| amount | DECIMAL(10,2) | - | Order amount |
| status | STRING | - | Order status |
| created_at | TIMESTAMP | - | Record creation in analytics |
| updated_at | TIMESTAMP | - | Last update in analytics |

**DDL**:
```sql
CREATE OR REPLACE TABLE `project.dataset.FACT_ORDERS` (
  order_id STRING NOT NULL,
  customer_id STRING NOT NULL,
  product_id STRING NOT NULL,
  order_date_id STRING,
  order_timestamp TIMESTAMP,
  quantity INT64,
  amount DECIMAL(10,2),
  status STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY DATE(order_timestamp)
CLUSTER BY customer_id, product_id, status;
```

**Sample Data**:
```
order_id | customer_id | product_id | order_date_id | order_timestamp      | quantity | amount | status    | created_at          | updated_at
ORD_001  | CUST_001    | PROD_001   | 20240510      | 2024-05-10 14:30:00  | 1        | 79.99  | Delivered | 2024-05-10 14:30:00 | 2024-07-12 08:00:00
ORD_002  | CUST_002    | PROD_002   | 20240511      | 2024-05-11 09:15:00  | 2        | 25.98  | Shipped   | 2024-05-11 09:15:00 | 2024-07-12 08:00:00
ORD_003  | CUST_001    | PROD_003   | 20240512      | 2024-05-12 16:45:00  | 1        | 24.99  | Pending   | 2024-05-12 16:45:00 | 2024-07-12 08:00:00
```

**ETL Logic** (Incremental load via Cloud Composer):
```python
SELECT
  o.order_id,
  o.customer_id,
  o.product_id,
  FORMAT_DATE('%Y%m%d', DATE(o.order_date)) as order_date_id,
  o.order_date as order_timestamp,
  o.quantity,
  o.amount,
  o.status,
  CURRENT_TIMESTAMP() as created_at,
  CURRENT_TIMESTAMP() as updated_at
FROM Orders o
JOIN DIM_CUSTOMER c ON o.customer_id = c.customer_id
JOIN DIM_PRODUCT p ON o.product_id = p.product_id
WHERE o.order_date >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
ORDER BY o.order_date DESC;
```

---

## Data Model Diagram

```
┌─────────────────────┐
│   DIM_CUSTOMER      │
├─────────────────────┤
│ customer_id (PK)    │
│ customer_name       │
│ email               │
│ city                │
│ state               │
│ signup_date         │
│ customer_age_group  │
└──────────┬──────────┘
           │
           │ (1:M)
           │
    ┌──────┴─────────────────────┐
    │                             │
    │                             │
┌───┴─────────────┐  ┌──────────┴────────────┐
│  FACT_ORDERS    │  │   DIM_PRODUCT        │
├─────────────────┤  ├──────────────────────┤
│ order_id (PK)   │  │ product_id (PK)      │
│ customer_id(FK)─┼──┤ product_name         │
│ product_id(FK)──┼──┤ category             │
│ order_date_id(FK)─┐ │ brand                │
│ quantity        │ │ │ price                │
│ amount          │ │ │ price_range          │
│ status          │ │ └──────────────────────┘
└─────┬───────────┘ │
      │             │
      └──────┬──────┘
             │ (M:1)
             │
      ┌──────┴────────┐
      │   DIM_DATE    │
      ├───────────────┤
      │ date_id (PK)  │
      │ calendar_date │
      │ year          │
      │ quarter       │
      │ month         │
      │ day_of_week   │
      │ is_weekend    │
      └───────────────┘
```

---

## Key Analytics Queries

### Query 1: Total Revenue by Month

```sql
SELECT
  EXTRACT(YEAR_MONTH FROM dd.calendar_date) as year_month,
  SUM(fo.amount) as total_revenue,
  COUNT(DISTINCT fo.order_id) as order_count,
  COUNT(DISTINCT fo.customer_id) as unique_customers,
  AVG(fo.amount) as avg_order_value
FROM `project.dataset.FACT_ORDERS` fo
JOIN `project.dataset.DIM_DATE` dd ON fo.order_date_id = dd.date_id
WHERE fo.status IN ('Delivered', 'Shipped')
GROUP BY year_month
ORDER BY year_month DESC;
```

**Expected Output**:
```
year_month | total_revenue | order_count | unique_customers | avg_order_value
202407     | 5234.50       | 45          | 32               | 116.32
202406     | 4125.75       | 38          | 28               | 108.57
```

---

### Query 2: Top 10 Customers by Revenue

```sql
SELECT
  dc.customer_id,
  dc.customer_name,
  dc.city,
  dc.state,
  COUNT(DISTINCT fo.order_id) as lifetime_orders,
  SUM(fo.amount) as lifetime_revenue,
  AVG(fo.amount) as avg_order_value,
  MAX(fo.order_timestamp) as last_order_date
FROM `project.dataset.FACT_ORDERS` fo
JOIN `project.dataset.DIM_CUSTOMER` dc ON fo.customer_id = dc.customer_id
WHERE fo.status IN ('Delivered', 'Shipped')
GROUP BY dc.customer_id, dc.customer_name, dc.city, dc.state
ORDER BY lifetime_revenue DESC
LIMIT 10;
```

---

### Query 3: Sales by Product Category

```sql
SELECT
  dp.category,
  dp.brand,
  COUNT(DISTINCT fo.order_id) as orders,
  SUM(fo.quantity) as total_quantity,
  SUM(fo.amount) as total_revenue,
  AVG(dp.price) as avg_product_price,
  ROUND(SUM(fo.amount) / SUM(fo.quantity), 2) as avg_selling_price
FROM `project.dataset.FACT_ORDERS` fo
JOIN `project.dataset.DIM_PRODUCT` dp ON fo.product_id = dp.product_id
WHERE fo.order_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY dp.category, dp.brand
ORDER BY total_revenue DESC;
```

---

### Query 4: Order Status Distribution

```sql
SELECT
  fo.status,
  COUNT(DISTINCT fo.order_id) as order_count,
  COUNT(DISTINCT fo.customer_id) as customer_count,
  SUM(fo.amount) as total_amount,
  ROUND(COUNT(DISTINCT fo.order_id) * 100.0 / SUM(COUNT(DISTINCT fo.order_id)) 
        OVER (), 2) as pct_of_total
FROM `project.dataset.FACT_ORDERS` fo
GROUP BY fo.status
ORDER BY order_count DESC;
```

---

### Query 5: Daily Sales Trend

```sql
SELECT
  dd.calendar_date,
  dd.day_name,
  COUNT(DISTINCT fo.order_id) as orders,
  SUM(fo.amount) as daily_revenue,
  COUNT(DISTINCT fo.customer_id) as daily_customers
FROM `project.dataset.FACT_ORDERS` fo
JOIN `project.dataset.DIM_DATE` dd ON fo.order_date_id = dd.date_id
WHERE dd.calendar_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY dd.calendar_date, dd.day_name
ORDER BY dd.calendar_date DESC;
```

---

## ETL Pipeline Overview

### Data Flow

```
Source Systems (OLTP)
  ├── Customers table
  ├── Products table
  └── Orders table
        ↓
   Cloud Pub/Sub / Dataflow
   (Real-time streaming ingestion)
        ↓
   BigQuery Staging Layer
   ├── raw_customers
   ├── raw_products
   └── raw_orders
        ↓
   Cloud Composer (Airflow)
   ├── dim_load_dag (nightly at 2 AM UTC)
   │  ├── Load DIM_DATE (full refresh)
   │  ├── Load DIM_CUSTOMER (incremental merge)
   │  └── Load DIM_PRODUCT (incremental merge)
   │
   └── fact_load_dag (hourly)
      └── Load FACT_ORDERS (incremental append)
        ↓
   BigQuery Analytics Layer
   ├── DIM_CUSTOMER
   ├── DIM_PRODUCT
   ├── DIM_DATE
   └── FACT_ORDERS
```

### Transformation Rules

| Table | Logic | Frequency |
|-------|-------|-----------|
| DIM_CUSTOMER | Deduplicate on customer_id; add age_group calculation | Nightly |
| DIM_PRODUCT | Map prices to range categories; keep latest version | Nightly |
| DIM_DATE | Generate dates for 7-year period (one-time setup) | One-time |
| FACT_ORDERS | Join with dimensions; filter last 24h new orders | Hourly |

---

## Data Quality Rules

| Table | Rule | Validation SQL | Threshold |
|-------|------|---|-----------|
| FACT_ORDERS | No null amounts | `SELECT COUNT(*) FROM FACT_ORDERS WHERE amount IS NULL` | 0 rows |
| FACT_ORDERS | Amount > 0 | `SELECT COUNT(*) FROM FACT_ORDERS WHERE amount <= 0` | 0 rows |
| FACT_ORDERS | Valid customer_id | `SELECT COUNT(*) FROM FACT_ORDERS WHERE customer_id NOT IN (SELECT customer_id FROM DIM_CUSTOMER)` | 0 rows |
| FACT_ORDERS | Valid product_id | `SELECT COUNT(*) FROM FACT_ORDERS WHERE product_id NOT IN (SELECT product_id FROM DIM_PRODUCT)` | 0 rows |
| DIM_CUSTOMER | Unique customers | `SELECT COUNT(*) FROM DIM_CUSTOMER GROUP BY customer_id HAVING COUNT(*) > 1` | 0 rows |
| DIM_PRODUCT | Unique products | `SELECT COUNT(*) FROM DIM_PRODUCT GROUP BY product_id HAVING COUNT(*) > 1` | 0 rows |

---

## Performance Optimization

### Partitioning Strategy

- **FACT_ORDERS**: Partitioned by `DATE(order_timestamp)` (daily)
  - Reduces query cost by scanning only relevant date ranges
  - Recommended: Filter on `order_date` in WHERE clause

- **DIM_CUSTOMER**: Partitioned by `DATE(updated_at)` (daily)
- **DIM_PRODUCT**: Partitioned by `DATE(updated_at)` (daily)

### Clustering Strategy

- **FACT_ORDERS**: Clustered by `customer_id`, `product_id`, `status`
  - Optimizes queries filtering by these columns
  - Speeds up JOIN operations with dimension tables

- **DIM_CUSTOMER**: Clustered by `state`, `city`
- **DIM_PRODUCT**: Clustered by `category`, `brand`

### Query Optimization Tips

```sql
-- ✅ Good: Uses partition and cluster columns
SELECT * FROM FACT_ORDERS
WHERE DATE(order_timestamp) >= '2024-07-01'
  AND customer_id = 'CUST_001'
ORDER BY order_timestamp DESC;

-- ✅ Good: Partitioned query
SELECT customer_id, SUM(amount)
FROM FACT_ORDERS
WHERE order_timestamp >= TIMESTAMP('2024-07-01')
GROUP BY customer_id;

-- ❌ Avoid: Full table scan
SELECT * FROM FACT_ORDERS
WHERE CAST(order_id AS INT64) > 100;
```

---

## Deployment Checklist

- [ ] BigQuery datasets created (`analytics`, `staging`)
- [ ] DIM_DATE table created and populated with 7 years of dates
- [ ] DIM_CUSTOMER table created from Customers source
- [ ] DIM_PRODUCT table created from Products source
- [ ] FACT_ORDERS table created from Orders source
- [ ] Partitioning and clustering policies applied
- [ ] Cloud Composer DAGs deployed for daily and hourly loads
- [ ] Data quality validation rules configured
- [ ] Sample queries tested and validated
- [ ] Access controls configured (readers, analysts)
- [ ] Documentation shared with analytics team

---

## References

- [Business Requirements](../business_requirement.md)
- [Project README](../README.md)
- [BigQuery Best Practices](https://cloud.google.com/bigquery/docs/best-practices)
- [BigQuery Schema Design](https://cloud.google.com/bigquery/docs/schemas)

