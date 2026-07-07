# dashboards/powerbi/visual_mapping.md

## 1. Executive Overview

| Visual | Power BI Visual Type | Fields | Measures | Tooltip | Drill-through | Formatting |
|--------|----------------------|--------|----------|---------|----------------|-------------|
| KPI Tiles (Total Incidents, Critical Incidents, Health Score, Incidents Today, Last 24 h) | Card | – | Total Incidents, Critical Incidents, Health Score, Incidents Today, Last 24 Hours | Value, last refresh date | Drill to Executive Detail page filtered by KPI | Dark background #1B1B1B, white text, large font (28 pt), accent #00B7C3 for Health Score |
| Incident Volume Trend (Last 30 Days) | Line chart | Date (Calendar[Date]) | Total Incidents | Date, incident count | Drill to Incident Timeline page (date range) | Axis labels #A19F9D, gridlines #3B3A39, line color #00B7C3 |
| Critical Incident % Donut | Donut chart | – | Critical Incident % | Percentage and absolute count | Drill to Critical Incident List page | Data colors: #FF6666 (critical) / #00B7C3 (non‑critical) |
| Server Health Multi‑row Card | Multi‑row card | Server Name, Region | Health Score | Server, health score | Drill to Server Detail page (server filter) | Background #201F1E, border #3B3A39, value font 28 pt, category font 13 pt |

## 2. Infrastructure Monitoring

| Visual | Power BI Visual Type | Fields | Measures | Tooltip | Drill-through | Formatting |
|--------|----------------------|--------|----------|---------|----------------|-------------|
| Avg CPU % by Server | Clustered column chart | Server Name | Avg CPU % | Server, CPU % | Drill to Server Detail page | Column color #3498DB, data labels 11 pt |
| Avg Memory % by Server | Clustered column chart | Server Name | Avg Memory % | Server, Memory % | Drill to Server Detail page | Column color #28B463 |
| API Latency Over Time | Line chart | Date (Calendar[Date]) | Avg API Latency | Date, latency (ms) | Drill to API Latency Detail page | Line color #FFB900 |
| Total Servers | Card | – | Total Servers | – | Drill to Server List page | Accent #1ABC9C |
| Top 10 Servers by Health Score | Table | Server Name, Region, Health Score | – | Hover shows last 24h CPU/Memory | Drill to Server Detail page | Header background #1B1B1B, alternating row color #201F1E |

## 3. AI Incident Intelligence

| Visual | Power BI Visual Type | Fields | Measures | Tooltip | Drill-through | Formatting |
|--------|----------------------|--------|----------|---------|----------------|-------------|
| Severity Distribution | Funnel chart | Severity (Critical, High, Medium, Low) | Total Incidents | Severity, count | Drill to Incident List filtered by severity | Gradient from #FF6666 (Critical) to #6CB4EE (Low) |
| Incidents vs CPU Scatter | Scatter chart | Server Name | Total Incidents, Avg CPU % | Server, incidents, CPU % | Drill to Server Detail page | Point size based on Critical Incident % |
| Incident Growth % (30 d) | Card | – | Incident Growth % | % change vs previous period | Drill to Growth Trend line chart | Accent #FFB900 |
| Slicer – Incident Type | Slicer | Incident Type | – | – | Filters all page visuals | Dropdown style |
| Recent Critical Incidents | Table | Incident ID, Date, Server, Description, Severity | – | Full description on hover | Drill to Incident Detail page | Conditional formatting red for Critical |

## 4. Data Warehouse

| Visual | Power BI Visual Type | Fields | Measures | Tooltip | Drill-through | Formatting |
|--------|----------------------|--------|----------|---------|----------------|-------------|
| Load Size by Source | Stacked column chart | Data Source, Load Date | Total Load (GB) | Source, load size, date | Drill to Source Detail page | Palette #00B7C3, #9B59B6, #8E44AD |
| Refresh Duration | Line chart | Refresh Date | Avg Refresh Duration (sec) | Date, duration | Drill to Refresh Log page | Line color #FF6666 |
| Number of Tables | Card | – | COUNTROWS('Tables') | – | Drill to Table Catalog page | Accent #1ABC9C |
| Row Count by Schema | Matrix | Schema, Table Name | Row Count | – | Drill to Table Detail page | Header background #1B1B1B |
| Data Quality Issues by Category | Donut chart | Issue Category | Issue Count | Category, count | Drill to Issue List page | Colors #FFB900 (Missing), #FF6666 (Invalid), #6CB4EE (Duplicate) |

## 5. Data Quality

| Visual | Power BI Visual Type | Fields | Measures | Tooltip | Drill-through | Formatting |
|--------|----------------------|--------|----------|---------|----------------|-------------|
| Total Issues | Card | – | Total Issues | – | Drill to Issues List page | Accent #FF6666 |
| Issues by Severity | Bar chart | Severity | Issue Count | Severity, count | Drill to Severity Detail page | Colors #FF6666 (Critical), #FFB900 (High), #6CB4EE (Medium) |
| Issue Trend (90 d) | Line chart | Date (Calendar[Date]) | Daily Issue Count | Date, count | Drill to Daily Issue Log page | Line color #9B59B6 |
| Top 20 Tables (Issue Rate) | Table | Table Name, Row Count, Issue Count | – | Hover shows % issue rate | Drill to Table Issue Detail page | Rows >5 % issue rate highlighted red |
| Issue Type Slicer | Slicer | Issue Type | – | – | Filters all page visuals | Dark background |
| Data Freshness (Avg Days Since Load) | Card | – | Avg Days Since Load | – | Drill to Stale Data Detail page | Accent #00B7C3 |
