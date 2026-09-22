# Superset Dashboard Setup & Instructions

## Quick Start (Docker)

```bash
# 1. Start Docker containers (Redis, PostgreSQL, Superset)
docker-compose up -d

# Wait ~30s for Superset to initialize

# 2. Access Superset at http://localhost:8088
#    Default login: admin / admin

# 3. Create database connection to CSV
#    - Navigate to Data > Databases > + Database
#    - Or use the CSV upload feature to import audit_metrics.csv

# 4. Create dashboard "Featured Charts"
#    - Go to Dashboards > + Dashboard
#    - Title: "Featured Charts"
#    - Add charts (see below)
```

## Dashboard Charts to Create

### 1. Incident Detection Count (by mode)
- Chart Type: Bar
- Metric: Count of rows
- Group by: mode (alert, suggest-pr, auto-staging)
- Title: "Incident Detection by Mode"

### 2. Success Rate (%)
- Chart Type: Gauge
- Metric: Count of rows where result='success'
- Formula: Count(success) / Count(total) * 100
- Title: "Overall Success Rate"

### 3. Rollback Events
- Chart Type: Table
- Columns: time, mode, diagnosis_class, rollback, result
- Filters: where rollback='true'
- Title: "Rollback Events"

### 4. Detection Confidence Distribution
- Chart Type: Histogram
- Metric: confidence
- Bins: 10
- Title: "Agent Confidence Score Distribution"

### 5. MTTR Estimate (Time to Resolve)
- Chart Type: Table
- Columns: input, diagnosis_class, mode, status, result
- Title: "Incident Timeline"

## Manual Dashboard Creation

If you prefer to skip Docker and create charts manually:

1. **Import audit_metrics.csv** into your Superset instance (Admin > Upload Data)
2. Create a dataset from the CSV table
3. Use the SQL Lab to query data and create visualizations
4. Save charts to the "Featured Charts" dashboard

## Example SQL Queries

```sql
-- Success rate by mode
SELECT mode, 
       COUNT(*) as total,
       SUM(CASE WHEN result='success' THEN 1 ELSE 0 END) as success_count,
       ROUND(100.0 * SUM(CASE WHEN result='success' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM agent_audit_metrics
GROUP BY mode;

-- Confidence distribution
SELECT 
  ROUND(confidence, 1) as confidence_bucket,
  COUNT(*) as incident_count
FROM agent_audit_metrics
GROUP BY ROUND(confidence, 1)
ORDER BY confidence_bucket;

-- Rollback count
SELECT COUNT(*) as rollback_count FROM agent_audit_metrics WHERE rollback='true';
```

## Stop Superset

```bash
docker-compose down
```

## Cleanup (remove volumes)

```bash
docker-compose down -v
```
