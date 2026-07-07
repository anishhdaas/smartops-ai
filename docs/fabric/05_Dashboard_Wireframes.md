# SmartOps AI - Dashboard Wireframes

> **Theme**: SmartOps AI Enterprise (see `04_PowerBI_Theme.json`)  
> **Data Model**: Star schema with `DimRegions`, `DimServers`, `FactIncidents`, `FactHourlyMetrics`  
> **DAX Measures**: See `03_DAX_Measures.md` (40+ measures across 7 display folders)

---

## Page 1: Executive Dashboard

### Objective
Provide C-suite and operations leadership with a single-pane view of overall system health, incident volume trends, and critical risk indicators. Answer: "Is our infrastructure healthy right now?" and "Where should we focus attention?"

### Layout
- **Canvas**: 16:9 (1920 × 1080)
- **Grid**: 12-column responsive grid
- **Sections**: Header (row 1), KPI Row (row 2), Trend Row (row 3), Breakdown Row (row 4-5)

### Visuals

| # | Visual | Type | Position | Size | Measure/Fields |
|---|--------|------|----------|------|----------------|
| 1 | Title Bar | Text Box | (0,0) - (12,1) | Full width | "SmartOps AI — Executive Dashboard" |
| 2 | Total Incidents | Card | (0,1) - (3,2) | 3 col | `[Total Incidents]` |
| 3 | Critical Incidents | Card | (3,1) - (6,2) | 3 col | `[Critical Incidents]` (KPI: Target 0, Trend Down) |
| 4 | Health Score | Gauge | (6,1) - (9,2) | 3 col | `[Health Score]` (Min 0, Max 100, Target 90) |
| 5 | Availability % | KPI | (9,1) - (12,2) | 3 col | `[Availability %]` (Target 99.9%) |
| 6 | Incident Trend (30d) | Line Chart | (0,2) - (8,6) | 8 col × 4 row | X: `FactIncidents[event_date]`, Y: `[Daily Incidents]` |
| 7 | Severity Breakdown | Donut Chart | (8,2) - (12,4) | 4 col × 2 row | Legend: `FactIncidents[severity]`, Values: `[Total Incidents]` |
| 8 | Top 5 Regions | Bar Chart | (8,4) - (12,6) | 4 col × 2 row | Axis: `DimRegions[region_name]`, Values: `[Total Incidents]` |
| 9 | Incidents by Event Type | Stacked Column | (0,6) - (6,10) | 6 col × 4 row | Axis: `FactIncidents[event_type]`, Legend: `FactIncidents[severity]`, Values: `[Total Incidents]` |
| 10 | Regional Heat Map | Matrix | (6,6) - (12,10) | 6 col × 4 row | Rows: `DimRegions[region_name]`, Columns: `FactIncidents[event_type]`, Values: `[Total Incidents]`, `[Critical Incidents]`, `[Health Score]` |

### Slicers (Top Right, Floating)
| Slicer | Field | Type | Default |
|--------|-------|------|---------|
| Date Range | `FactIncidents[event_date]` | Between | Last 30 days |
| Region | `DimRegions[region_name]` | Dropdown Multi | All |
| Severity | `FactIncidents[severity]` | Checkbox | All |
| Event Type | `FactIncidents[event_type]` | Dropdown Multi | All |

### Drill-Through
- **Target Page**: Incident Analytics
- **Drill Fields**: `FactIncidents[incident_id]`, `DimRegions[region_name]`, `DimServers[server_name]`
- **Keep All Filters**: On

### Tooltip Pages
- **Tooltip_IncidentDetail**: Shows `incident_id`, `timestamp`, `server_name`, `region_name`, `event_type`, `severity`, `cpu_percent`, `memory_percent`, `api_latency_ms`, `metadata`
- **Tooltip_RegionSummary**: Shows `region_name`, `timezone`, `[Total Incidents]`, `[Critical Incidents]`, `[Health Score]`, `[Avg CPU]`, `[Avg Memory]`, `[Avg API Latency]`

### KPI Cards (Row 2) - Conditional Formatting
| Card | Good | Warning | Critical |
|------|------|---------|----------|
| Critical Incidents | 0 | 1-5 | >5 |
| Health Score | ≥90 | 70-89 | <70 |
| Availability % | ≥99.9% | 99.5-99.89% | <99.5% |

---

## Page 2: Incident Analytics

### Objective
Enable incident responders and on-call engineers to investigate incident patterns, identify recurring failure modes, and perform root cause triage. Answer: "What incidents happened when?", "Which servers/types are problematic?", and "Is severity escalating?"

### Layout
- **Canvas**: 16:9 (1920 × 1080)
- **Grid**: 12-column
- **Sections**: Header, Time Series, Incident Explorer, Root Cause Panel

### Visuals

| # | Visual | Type | Position | Size | Measure/Fields |
|---|--------|------|----------|------|----------------|
| 1 | Title Bar | Text Box | (0,0) - (12,1) | Full | "Incident Analytics" |
| 2 | Incident Volume | Area Chart | (0,1) - (12,5) | 12 col × 4 row | X: `FactIncidents[incident_timestamp]` (Hour), Y: `[Hourly Event Count]`, Legend: `FactIncidents[severity]` |
| 3 | Incident Table | Table | (0,5) - (8,12) | 8 col × 7 row | `incident_id`, `incident_timestamp`, `server_name`, `region_name`, `event_type`, `severity`, `cpu_percent`, `memory_percent`, `api_latency_ms`, `auth_failure_count` |
| 4 | Severity Timeline | Stacked Area | (8,5) - (12,9) | 4 col × 4 row | X: `FactIncidents[event_date]`, Y: `[Total Incidents]`, Legend: `FactIncidents[severity]` |
| 5 | Event Type Trend | Line Chart | (8,9) - (12,12) | 4 col × 3 row | X: `FactIncidents[event_date]`, Y: `[Total Incidents]`, Legend: `FactIncidents[event_type]` |
| 6 | AI Root Cause Panel | Text Box + Card | (0,12) - (12,14) | Full width | `[Top Event Type]`, `[Top Server]`, `[Top Region]`, `[Anomaly Score]` |

### Slicers (Left Panel, Fixed Width 300px)
| Slicer | Field | Type |
|--------|-------|------|
| Date Range | `FactIncidents[event_date]` | Between (Relative: Last 7/30/90 days) |
| Region | `DimRegions[region_name]` | List with Search |
| Server | `DimServers[server_name]` | List with Search (cascades from Region) |
| Event Type | `FactIncidents[event_type]` | Checkbox |
| Severity | `FactIncidents[severity]` | Checkbox |

### Drill-Through
- **From**: Executive Dashboard, Regional Analysis
- **To**: This page
- **Fields**: `incident_id`, `region_name`, `server_name`
- **Back Button**: Custom button on top-right linking to Executive Dashboard

### Tooltip Pages
- **Tooltip_IncidentDetail**: (Same as Executive)
- **Tooltip_ServerHealth**: `server_name`, `[Server Uptime %]`, `[Total Incidents]`, `[Critical Incidents]`, `[Avg CPU]`, `[Avg Memory]`, `[Avg API Latency]`, `first_seen_at`, `last_seen_at`

### Conditional Formatting - Incident Table
| Column | Rule |
|--------|------|
| severity | CRITICAL: Red bg #FFF0F0, White text; WARNING: Yellow bg #FFF8E1, Dark text; INFO: Blue bg #E7F1FF, Dark text |
| cpu_percent | >90: Red; >75: Orange; >50: Yellow |
| memory_percent | >90: Red; >75: Orange; >50: Yellow |
| api_latency_ms | >1000: Red; >500: Orange; >200: Yellow |

---

## Page 3: Infrastructure Health

### Objective
Give platform engineers and SREs real-time visibility into CPU, memory, and API latency trends across the fleet. Answer: "Are servers running hot?", "Which resources are saturated?", and "Are we meeting SLA targets?"

### Layout
- **Canvas**: 16:9 (1920 × 1080)
- **Grid**: 12-column
- **Focus**: Real-time infrastructure metrics, server health scorecards

### Visuals

| # | Visual | Type | Position | Size | Measure/Fields |
|---|--------|------|----------|------|----------------|
| 1 | Title Bar | Text Box | (0,0) - (12,1) | Full | "Infrastructure Health" |
| 2 | CPU Utilization | Line Chart | (0,1) - (6,5) | 6 col × 4 row | X: `FactHourlyMetrics[hour_bucket]`, Y: `[Hourly Avg CPU]`, Series: `DimRegions[region_name]` |
| 3 | Memory Utilization | Line Chart | (6,1) - (12,5) | 6 col × 4 row | X: `FactHourlyMetrics[hour_bucket]`, Y: `[Hourly Avg Memory]`, Series: `DimRegions[region_name]` |
| 4 | API Latency | Line Chart | (0,5) - (6,9) | 6 col × 4 row | X: `FactHourlyMetrics[hour_bucket]`, Y: `[Hourly Avg API Latency]`, Series: `DimRegions[region_name]` |
| 5 | Event Volume | Column Chart | (6,5) - (12,9) | 6 col × 4 row | X: `FactHourlyMetrics[hour_bucket]`, Y: `[Hourly Event Count]`, Legend: `FactIncidents[severity]` (via relationship) |
| 6 | Server Health Grid | Matrix | (0,9) - (12,14) | 12 col × 5 row | Rows: `DimServers[server_name]`, Columns: `Region`, `Server Uptime %`, `[Total Incidents]`, `[Critical Incidents]`, `[Avg CPU]`, `[Avg Memory]`, `[Avg API Latency]`, `last_seen_at` |
| 7 | MTTR Trend | Line Chart | (0,14) - (6,17) | 6 col × 3 row | X: `FactIncidents[event_date]`, Y: `[MTTR]` |
| 8 | SLA Compliance | Gauge | (6,14) - (9,17) | 3 col × 3 row | `[SLA %]` (Target 95%) |
| 9 | Availability Trend | Area Chart | (9,14) - (12,17) | 3 col × 3 row | X: `FactIncidents[event_date]`, Y: `[Availability %]` |

### Slicers (Top Bar, Horizontal)
| Slicer | Field | Type |
|--------|-------|------|
| Time Range | `FactHourlyMetrics[hour_bucket]` | Relative: Last 24h / 7d / 30d |
| Region | `DimRegions[region_name]` | Dropdown Multi |
| Server | `DimServers[server_name]` | Dropdown Multi (Search) |

### Drill-Through
- **Target**: Incident Analytics (filtered to server)
- **Source**: Server Health Grid row context → `server_name`

### Tooltip Pages
- **Tooltip_ServerHealth**: (Same as Incident Analytics)
- **Tooltip_HourlyMetrics**: `hour_bucket`, `server_name`, `region_name`, `event_count`, `avg_cpu_percent`, `avg_memory_percent`, `avg_api_latency_ms`, `info_count`, `warning_count`, `critical_count`

### Conditional Formatting - Server Health Grid
| Column | Rules |
|--------|-------|
| Server Uptime % | ≥99.9%: Green; ≥99.5%: Yellow; <99.5%: Red |
| Critical Incidents | 0: Green; 1-2: Yellow; >2: Red |
| Avg CPU | <50: Green; 50-75: Yellow; >75: Red |
| Avg Memory | <50: Green; 50-75: Yellow; >75: Red |
| Avg API Latency | <200: Green; 200-500: Yellow; >500: Red |

---

## Page 4: Regional Analysis

### Objective
Allow regional managers and global operations to compare health across Bangalore, Singapore, and Tokyo. Answer: "Which region has the most incidents?", "Are there regional patterns in failure types?", and "How does server density correlate with health?"

### Layout
- **Canvas**: 16:9 (1920 × 1080)
- **Grid**: 12-column
- **Focus**: Cross-region comparison, geographic distribution

### Visuals

| # | Visual | Type | Position | Size | Measure/Fields |
|---|--------|------|----------|------|----------------|
| 1 | Title Bar | Text Box | (0,0) - (12,1) | Full | "Regional Analysis" |
| 2 | Region KPI Cards | Multi-Row Card | (0,1) - (3,3) | 3 col × 2 row | `[Distinct Regions]`, `[Distinct Servers]`, `[Total Incidents]`, `[Critical Incidents]`, `[Health Score]` (per region via SELECTEDVALUE) |
| 3 | Regional Comparison | Clustered Bar | (3,1) - (9,5) | 6 col × 4 row | Axis: `DimRegions[region_name]`, Values: `[Total Incidents]`, `[Critical Incidents]`, `[Warning Incidents]`, `[Info Incidents]` |
| 4 | Region Health Score | Gauge | (9,1) - (12,3) | 3 col × 2 row | `[Region Health Score]` (uses SELECTEDVALUE DimRegions[region_name]) |
| 5 | Incidents by Region/Type | Stacked Bar | (0,3) - (6,7) | 6 col × 4 row | Axis: `DimRegions[region_name]`, Legend: `FactIncidents[event_type]`, Values: `[Total Incidents]` |
| 6 | Regional Trend | Line Chart | (6,3) - (12,7) | 6 col × 4 row | X: `FactIncidents[event_date]`, Y: `[Daily Incidents]`, Series: `DimRegions[region_name]` |
| 7 | Server Count by Region | Donut Chart | (0,7) - (4,11) | 4 col × 4 row | Legend: `DimRegions[region_name]`, Values: `[Distinct Servers]` |
| 8 | Critical % by Region | 100% Stacked Bar | (4,7) - (8,11) | 4 col × 4 row | Axis: `DimRegions[region_name]`, Values: `[Critical %]`, `[Warning %]`, `[Info %]` |
| 9 | Regional Detail Table | Table | (8,7) - (12,14) | 4 col × 7 row | `region_name`, `timezone`, `active_servers`, `total_incidents`, `critical_incidents`, `avg_cpu_percent`, `avg_memory_percent`, `avg_api_latency_ms`, `last_incident_at` |
| 10 | Region-to-Region Comparison | Scatter Plot | (0,11) - (8,14) | 8 col × 3 row | X: `[Avg CPU]`, Y: `[Avg API Latency]`, Size: `[Total Incidents]`, Color: `DimRegions[region_name]`, Detail: `DimServers[server_name]` |

### Slicers (Left Panel)
| Slicer | Field | Type |
|--------|-------|------|
| Date Range | `FactIncidents[event_date]` | Between |
| Region | `DimRegions[region_name]` | List (Single Select for Region Health Score gauge) |
| Event Type | `FactIncidents[event_type]` | Checkbox |

### Drill-Through
- **From**: Executive Dashboard (Top 5 Regions bar chart)
- **To**: This page with `region_name` filter applied
- **Back Button**: Returns to Executive Dashboard

### Tooltip Pages
- **Tooltip_RegionSummary**: (Same as Executive)
- **Tooltip_RegionComparison**: Side-by-side comparison of selected region vs. all regions average

### Navigation Buttons (Top Right)
| Button | Action | Style |
|--------|--------|-------|
| Executive Dashboard | Page Navigation | Primary |
| Incident Analytics | Page Navigation | Secondary |
| Infrastructure Health | Page Navigation | Secondary |
| AI Root Cause | Page Navigation | Secondary |

---

## Page 5: AI Root Cause Analysis

### Objective
Empower incident responders with AI-driven root cause analysis, anomaly detection, and predictive insights. Answer: "What caused this incident?", "Which servers are at risk?", and "What failure pattern is emerging?"

### Layout
- **Canvas**: 16:9 (1920 × 1080)
- **Grid**: 12-column
- **Focus**: AI-powered insights, anomaly detection, predictive analytics

### Visuals

| # | Visual | Type | Position | Size | Measure/Fields |
|---|--------|------|----------|------|----------------|
| 1 | Title Bar | Text Box | (0,0) - (12,1) | Full | "AI Root Cause Analysis" |
| 2 | Health Score | Card (Large) | (0,1) - (3,3) | 3 col × 2 row | `[Health Score]` (Font 48px, Color conditional) |
| 3 | Anomaly Alert | Card | (3,1) - (6,3) | 3 col × 2 row | `[Anomaly Score]` (1=Anomaly, 0=Normal) - Red/Green conditional |
| 4 | Failure Rate | KPI | (6,1) - (9,3) | 3 col × 2 row | `[Failure Rate]` (Target <5%) |
| 5 | Incident Trend (Slope) | Card | (9,1) - (12,3) | 3 col × 2 row | `[Incident Trend 7D]` (Positive=Increasing, Negative=Decreasing) |
| 6 | Top Contributors | Table | (0,3) - (6,7) | 6 col × 4 row | `DimRegions[region_name]`, `DimServers[server_name]`, `FactIncidents[event_type]`, `[Total Incidents]`, `[Critical Incidents]`, `[Health Score]` - sorted by Incident Count desc |
| 7 | Anomaly Timeline | Scatter Plot | (6,3) - (12,7) | 6 col × 4 row | X: `FactIncidents[incident_timestamp]`, Y: `[Total Incidents]` (hourly), Color: `[Anomaly Score]` (Red/Blue), Size: `[Critical Incidents]` |
| 8 | Event Type Correlation | Matrix | (0,7) - (6,11) | 6 col × 4 row | Rows: `FactIncidents[event_type]`, Columns: `FactIncidents[severity]`, Values: `[Total Incidents]`, `[Avg CPU]`, `[Avg Memory]`, `[Avg API Latency]` |
| 9 | Predicted Risk | Table | (6,7) - (12,11) | 6 col × 4 row | `DimServers[server_name]`, `DimRegions[region_name]`, `[Health Score]`, `[Server Uptime %]`, `[Incident Trend 7D]`, `[Anomaly Score]` - Filtered: Health Score < 70 OR Anomaly Score = 1 |
| 10 | Root Cause Narrative | Text Box (Dynamic) | (0,11) - (12,14) | Full × 3 row | DAX-driven narrative: "Top risk: [Top Server] in [Top Region] with [Top Event Type]. Health Score: [Health Score]. Anomaly detected: [Anomaly Score]. Recommended action: Investigate [Top Server] for [Top Event Type] spikes." |
| 11 | Metadata Explorer | Table | (0,14) - (12,17) | Full × 3 row | `incident_id`, `server_name`, `region_name`, `event_type`, `severity`, `metadata` (parsed JSON: error_code, stack_trace, request_id) - Filtered: severity = CRITICAL |

### Slicers (Collapsible Panel Left)
| Slicer | Field | Type |
|--------|-------|------|
| Date Range | `FactIncidents[event_date]` | Relative: Last 7/30 days |
| Region | `DimRegions[region_name]` | List |
| Server | `DimServers[server_name]` | List (Search) |
| Min Health Score | `[Health Score]` | Numeric Range (0-100) |
| Show Anomalies Only | `[Anomaly Score]` | Checkbox (1 = Anomaly) |

### Drill-Through
- **From**: Any page (Incident Table, Server Health Grid)
- **To**: This page with `incident_id`, `server_name`, `region_name` context
- **Metadata Explorer**: Click row → Opens detailed JSON viewer (custom visual)

### Tooltip Pages
- **Tooltip_IncidentDetail**: (Same as Executive)
- **Tooltip_ServerRiskProfile**: `server_name`, `region_name`, `[Health Score]`, `[Server Uptime %]`, `[Total Incidents]`, `[Critical Incidents]`, `[Incident Trend 7D]`, `[Anomaly Score]`, recent 10 incidents mini-timeline

### Conditional Formatting
| Visual | Rule |
|--------|------|
| Health Score Card | ≥90: Green (#198754); 70-89: Yellow (#FFC107); <70: Red (#DC3545) |
| Anomaly Alert | 1: Red bg, White text "⚠ ANOMALY DETECTED"; 0: Green bg, "✓ Normal" |
| Predicted Risk Table | Health Score < 70: Row Red; Anomaly Score = 1: Row Orange; Both: Row Dark Red |
| Root Cause Narrative | Dynamic color based on Health Score |

### AI Insight Measures Used
- `[Health Score]` - Composite infrastructure + severity score
- `[Anomaly Score]` - Z-score > 2 detection on hourly incident volume
- `[Incident Trend 7D]` - Linear regression slope (7-day)
- `[Failure Rate]` - (Critical + Warning) / Total
- `[Top Region]`, `[Top Server]`, `[Top Event Type]` - TOPN calculations
- `[Region Health Score]` - Per-region variant of Health Score

---

## Navigation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GLOBAL NAVIGATION BAR                     │
│  [Executive] [Incidents] [Infrastructure] [Regional] [AI]   │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │Executive │  │Incidents │  │ Infra    │  │ Regional │ AI │
│  │ Dashboard│──│ Analytics│──│ Health   │──│ Analysis │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│       │           │             │             │             │
│       └───────────┴─────────────┴─────────────┘             │
│                           │                                  │
│                    DRILL-THROUGH                            │
│                           │                                  │
│                    ┌────────────┐                           │
│                    │ Tooltip    │                           │
│                    │ Pages (2)  │                           │
│                    └────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

### Page Navigation Buttons (All Pages - Top Right)
- **Style**: Primary (current page), Secondary (others)
- **Icon**: Home, List, Server, Globe, Brain
- **Tooltip**: Page name

### Drill-Through Flow
1. **Executive Dashboard** → Click region bar → **Regional Analysis** (filtered)
2. **Executive Dashboard** → Click incident row → **Incident Analytics** (filtered)
3. **Infrastructure Health** → Click server row → **Incident Analytics** (filtered)
4. **Regional Analysis** → Click server → **Incident Analytics** (filtered)
5. **Any Page** → Right-click incident → **AI Root Cause Analysis** (context)

### Tooltip Page Definitions

#### Tooltip_IncidentDetail
- **Canvas**: 400 × 500
- **Visuals**: Card (incident_id), Card (timestamp), Card (server), Card (region), Card (event_type), Card (severity), Card (cpu), Card (memory), Card (latency), Text Box (metadata JSON pretty-print)

#### Tooltip_RegionSummary
- **Canvas**: 350 × 400
- **Visuals**: Card (region_name), Card (timezone), Card (Total Incidents), Card (Critical Incidents), Card (Health Score), Card (Avg CPU), Card (Avg Memory), Card (Avg Latency), Mini bar chart (severity breakdown)

#### Tooltip_ServerHealth
- **Canvas**: 350 × 450
- **Visuals**: Card (server_name), Card (region), Card (Uptime %), Card (Total Incidents), Card (Critical), Card (Avg CPU), Card (Avg Memory), Card (Avg Latency), Card (First Seen), Card (Last Seen), Mini line chart (24h CPU trend)

#### Tooltip_ServerRiskProfile
- **Canvas**: 400 × 500
- **Visuals**: Card (server), Card (region), Card (Health Score), Card (Uptime %), Card (Trend 7D), Card (Anomaly), Table (Recent 10 incidents: timestamp, type, severity, cpu, memory, latency)

---

## Responsive Behavior

| Breakpoint | Layout Adjustment |
|------------|-------------------|
| Desktop (≥1920) | Full 12-col grid, all visuals visible |
| Laptop (1366-1919) | KPI cards stack 2×2, charts resize, side slicers collapse to hamburger |
| Tablet (768-1365) | Single column stack, slicers in dropdown, tooltips on tap |
| Mobile (<768) | Not supported (Power BI Mobile uses phone layout) |

---

## Accessibility

- **Color Contrast**: All theme colors meet WCAG AA (4.5:1)
- **Focus Order**: Logical tab sequence (Title → Slicers → Visuals → Navigation)
- **Alt Text**: All visuals have descriptive titles
- **Color Blind Safe**: Palette tested for Deuteranopia/Protanopia/Tritanopia
- **Keyboard Navigation**: All slicers, buttons, drill-through accessible via keyboard

---

## Performance Notes

- **Query Reduction**: Use `SELECTEDVALUE` for single-select slicers
- **Aggregation**: Prefer `FactHourlyMetrics` for trend charts (pre-aggregated)
- **Cardinality**: Limit table visuals to Top N (50 rows) with "Show items with no data" Off
- **Measures**: Avoid `ALL`/`REMOVEFILTERS` in row context; use variables
- **Incremental Refresh**: Configure on `FactIncidents` (event_date) and `FactHourlyMetrics` (hour_bucket)