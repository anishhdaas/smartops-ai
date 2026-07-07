# SmartOps AI - DAX Measures for Microsoft Fabric

> **Source Tables**: `DimRegions`, `DimServers`, `FactIncidents`, `FactHourlyMetrics`  
> **Relationships**: `FactIncidents[region_key] → DimRegions[region_id]` (Many-to-One)  
> **Relationships**: `FactIncidents[server_id] → DimServers[server_id]` (Many-to-One)  
> **Relationships**: `FactHourlyMetrics[server_id] → DimServers[server_id]` (Many-to-One)  
> **Relationships**: `FactHourlyMetrics[region_key] → DimRegions[region_id]` (Many-to-One)

---

## 📁 Display Folder: **Incident KPIs**

### Total Incidents
```dax
Total Incidents =
VAR _Total = COUNTROWS ( FactIncidents )
RETURN
    _Total
```

### Critical Incidents
```dax
Critical Incidents =
VAR _Critical = CALCULATE (
    COUNTROWS ( FactIncidents ),
    FactIncidents[severity] = "CRITICAL"
)
RETURN
    _Critical
```

### Warning Incidents
```dax
Warning Incidents =
VAR _Warning = CALCULATE (
    COUNTROWS ( FactIncidents ),
    FactIncidents[severity] = "WARNING"
)
RETURN
    _Warning
```

### Incident %
```dax
Incident % =
VAR _Current = [Total Incidents]
VAR _All = CALCULATE ( [Total Incidents], ALL ( FactIncidents ) )
VAR _Pct = DIVIDE ( _Current, _All, 0 )
RETURN
    _Pct
```

---

## 📁 Display Folder: **Infrastructure**

### Avg CPU
```dax
Avg CPU =
VAR _Avg = AVERAGE ( FactIncidents[cpu_percent] )
RETURN
    _Avg
```

### Avg Memory
```dax
Avg Memory =
VAR _Avg = AVERAGE ( FactIncidents[memory_percent] )
RETURN
    _Avg
```

### Avg API Latency
```dax
Avg API Latency =
VAR _Avg = AVERAGE ( FactIncidents[api_latency_ms] )
RETURN
    _Avg
```

---

## 📁 Display Folder: **Incident KPIs** (Time Intelligence)

### Daily Incidents
```dax
Daily Incidents =
VAR _Today = MAX ( FactIncidents[event_date] )
VAR _Daily = CALCULATE (
    [Total Incidents],
    FactIncidents[event_date] = _Today
)
RETURN
    _Daily
```

### Weekly Incidents
```dax
Weekly Incidents =
VAR _MaxDate = MAX ( FactIncidents[event_date] )
VAR _WeekStart = _MaxDate - WEEKDAY ( _MaxDate, 2 ) + 1
VAR _WeekEnd = _WeekStart + 6
VAR _Weekly = CALCULATE (
    [Total Incidents],
    FactIncidents[event_date] >= _WeekStart,
    FactIncidents[event_date] <= _WeekEnd
)
RETURN
    _Weekly
```

### Monthly Incidents
```dax
Monthly Incidents =
VAR _MaxDate = MAX ( FactIncidents[event_date] )
VAR _MonthStart = EOMONTH ( _MaxDate, -1 ) + 1
VAR _MonthEnd = EOMONTH ( _MaxDate, 0 )
VAR _Monthly = CALCULATE (
    [Total Incidents],
    FactIncidents[event_date] >= _MonthStart,
    FactIncidents[event_date] <= _MonthEnd
)
RETURN
    _Monthly
```

### Rolling 7 Days
```dax
Rolling 7 Days =
VAR _MaxDate = MAX ( FactIncidents[event_date] )
VAR _StartDate = _MaxDate - 6
VAR _Rolling = CALCULATE (
    [Total Incidents],
    FactIncidents[event_date] >= _StartDate,
    FactIncidents[event_date] <= _MaxDate
)
RETURN
    _Rolling
```

### Rolling 30 Days
```dax
Rolling 30 Days =
VAR _MaxDate = MAX ( FactIncidents[event_date] )
VAR _StartDate = _MaxDate - 29
VAR _Rolling = CALCULATE (
    [Total Incidents],
    FactIncidents[event_date] >= _StartDate,
    FactIncidents[event_date] <= _MaxDate
)
RETURN
    _Rolling
```

---

## 📁 Display Folder: **Availability**

### MTTR (Mean Time To Resolve - Hours)
```dax
MTTR =
VAR _CriticalIncidents = FILTER (
    FactIncidents,
    FactIncidents[severity] = "CRITICAL"
)
VAR _WithResolution = ADDCOLUMNS (
    _CriticalIncidents,
    "NextTimestamp",
    VAR _CurrentTime = [incident_timestamp]
    VAR _CurrentServer = [server_id]
    RETURN
        MINX (
            FILTER (
                FactIncidents,
                FactIncidents[server_id] = _CurrentServer
                    && FactIncidents[incident_timestamp] > _CurrentTime
                    && FactIncidents[severity] <> "CRITICAL"
            ),
            FactIncidents[incident_timestamp]
        ),
    "ResolutionHours",
    VAR _Next = [NextTimestamp]
    VAR _Current = [incident_timestamp]
    RETURN
        IF ( NOT ISBLANK ( _Next ), DATEDIFF ( _Current, _Next, HOUR ), BLANK () )
)
VAR _AvgHours = AVERAGEX ( _WithResolution, [ResolutionHours] )
RETURN
    _AvgHours
```

### Availability %
```dax
Availability % =
VAR _TotalHours = DIVIDE ( [Rolling 30 Days] * 24, 1, 1 )
VAR _DownHours = [MTTR] * [Critical Incidents]
VAR _UpHours = _TotalHours - _DownHours
VAR _Pct = DIVIDE ( _UpHours, _TotalHours, 1 )
RETURN
    _Pct
```

### SLA %
```dax
SLA % =
VAR _SLAThresholdHours = 4
VAR _CriticalIncidents = CALCULATE (
    [Total Incidents],
    FactIncidents[severity] = "CRITICAL"
)
VAR _WithinSLA = CALCULATE (
    COUNTROWS ( FactIncidents ),
    FactIncidents[severity] = "CRITICAL",
    FactIncidents[cpu_percent] <= 90,
    FactIncidents[memory_percent] <= 90,
    FactIncidents[api_latency_ms] <= 500
)
VAR _SLA = DIVIDE ( _WithinSLA, _CriticalIncidents, 1 )
RETURN
    _SLA
```

---

## 📁 Display Folder: **AI Insights**

### Health Score
```dax
Health Score =
VAR _CriticalWeight = 0.5
VAR _WarningWeight = 0.3
VAR _InfoWeight = 0.1
VAR _CPUWeight = 0.15
VAR _MemoryWeight = 0.15
VAR _LatencyWeight = 0.2

VAR _TotalInc = [Total Incidents]
VAR _CriticalInc = [Critical Incidents]
VAR _WarningInc = [Warning Incidents]
VAR _InfoInc = CALCULATE ( [Total Incidents], FactIncidents[severity] = "INFO" )
VAR _AvgCPU = [Avg CPU]
VAR _AvgMemory = [Avg Memory]
VAR _AvgLatency = [Avg API Latency]

VAR _SeverityScore = 100
    - ( DIVIDE ( _CriticalInc, _TotalInc, 0 ) * 100 * _CriticalWeight )
    - ( DIVIDE ( _WarningInc, _TotalInc, 0 ) * 100 * _WarningWeight )
    - ( DIVIDE ( _InfoInc, _TotalInc, 0 ) * 100 * _InfoWeight )

VAR _InfraScore = 100
    - ( DIVIDE ( _AvgCPU, 100 ) * 100 * _CPUWeight )
    - ( DIVIDE ( _AvgMemory, 100 ) * 100 * _MemoryWeight )
    - ( MIN ( DIVIDE ( _AvgLatency, 1000 ), 1 ) * 100 * _LatencyWeight )

VAR _HealthScore = ( _SeverityScore * 0.6 ) + ( _InfraScore * 0.4 )
RETURN
    MAX ( 0, MIN ( 100, _HealthScore ) )
```

### Failure Rate
```dax
Failure Rate =
VAR _TotalInc = [Total Incidents]
VAR _FailureInc = CALCULATE (
    [Total Incidents],
    FactIncidents[severity] IN { "CRITICAL", "WARNING" }
)
VAR _Rate = DIVIDE ( _FailureInc, _TotalInc, 0 )
RETURN
    _Rate
```

### Top Region
```dax
Top Region =
VAR _RegionCounts = ADDCOLUMNS (
    VALUES ( DimRegions[region_name] ),
    "IncidentCount", CALCULATE ( [Total Incidents] )
)
VAR _TopRegion = TOPN ( 1, _RegionCounts, [IncidentCount], DESC )
RETURN
    MAXX ( _TopRegion, DimRegions[region_name] )
```

### Top Server
```dax
Top Server =
VAR _ServerCounts = ADDCOLUMNS (
    VALUES ( DimServers[server_name] ),
    "IncidentCount", CALCULATE ( [Total Incidents] )
)
VAR _TopServer = TOPN ( 1, _ServerCounts, [IncidentCount], DESC )
RETURN
    MAXX ( _TopServer, DimServers[server_name] )
```

### Top Event Type
```dax
Top Event Type =
VAR _EventCounts = ADDCOLUMNS (
    VALUES ( FactIncidents[event_type] ),
    "IncidentCount", CALCULATE ( [Total Incidents] )
)
VAR _TopEvent = TOPN ( 1, _EventCounts, [IncidentCount], DESC )
RETURN
    MAXX ( _TopEvent, FactIncidents[event_type] )
```

### Peak Hour
```dax
Peak Hour =
VAR _HourlyCounts = ADDCOLUMNS (
    ADDCOLUMNS (
        VALUES ( FactIncidents[incident_timestamp] ),
        "Hour", HOUR ( FactIncidents[incident_timestamp] )
    ),
    "IncidentCount", CALCULATE ( [Total Incidents] )
)
VAR _HourlyAgg = SUMMARIZE (
    _HourlyCounts,
    [Hour],
    "TotalIncidents", SUMX ( _HourlyCounts, [IncidentCount] )
)
VAR _PeakHour = TOPN ( 1, _HourlyAgg, [TotalIncidents], DESC )
RETURN
    MAXX ( _PeakHour, [Hour] )
```

### Peak Day
```dax
Peak Day =
VAR _DailyCounts = ADDCOLUMNS (
    VALUES ( FactIncidents[event_date] ),
    "IncidentCount", CALCULATE ( [Total Incidents] ),
    "DayName", FORMAT ( FactIncidents[event_date], "DDDD" )
)
VAR _PeakDay = TOPN ( 1, _DailyCounts, [IncidentCount], DESC )
RETURN
    MAXX ( _PeakDay, [DayName] )
```

---

## 📁 Display Folder: **Incident KPIs** (Additional Severity Breakdowns)

### Info Incidents
```dax
Info Incidents =
CALCULATE ( [Total Incidents], FactIncidents[severity] = "INFO" )
```

### Critical %
```dax
Critical % =
DIVIDE ( [Critical Incidents], [Total Incidents], 0 )
```

### Warning %
```dax
Warning % =
DIVIDE ( [Warning Incidents], [Total Incidents], 0 )
```

---

## 📁 Display Folder: **Infrastructure** (Hourly Aggregations)

### Hourly Avg CPU
```dax
Hourly Avg CPU =
AVERAGE ( FactHourlyMetrics[avg_cpu_percent] )
```

### Hourly Avg Memory
```dax
Hourly Avg Memory =
AVERAGE ( FactHourlyMetrics[avg_memory_percent] )
```

### Hourly Avg API Latency
```dax
Hourly Avg API Latency =
AVERAGE ( FactHourlyMetrics[avg_api_latency_ms] )
```

### Hourly Event Count
```dax
Hourly Event Count =
SUM ( FactHourlyMetrics[event_count] )
```

---

## 📁 Display Folder: **Availability** (Server-Level)

### Server Uptime %
```dax
Server Uptime % =
VAR _Server = SELECTEDVALUE ( DimServers[server_id] )
VAR _TotalHours = CALCULATE (
    DATEDIFF (
        MIN ( FactHourlyMetrics[hour_bucket] ),
        MAX ( FactHourlyMetrics[hour_bucket] ),
        HOUR
    ),
    DimServers[server_id] = _Server
)
VAR _DownHours = CALCULATE (
    SUM ( FactHourlyMetrics[critical_count] ),
    DimServers[server_id] = _Server
)
VAR _UpHours = _TotalHours - _DownHours
VAR _Pct = DIVIDE ( _UpHours, _TotalHours, 1 )
RETURN
    _Pct
```

### Region Health Score
```dax
Region Health Score =
VAR _Region = SELECTEDVALUE ( DimRegions[region_name] )
VAR _TotalInc = CALCULATE ( [Total Incidents], DimRegions[region_name] = _Region )
VAR _CriticalInc = CALCULATE ( [Critical Incidents], DimRegions[region_name] = _Region )
VAR _WarningInc = CALCULATE ( [Warning Incidents], DimRegions[region_name] = _Region )
VAR _AvgCPU = CALCULATE ( [Avg CPU], DimRegions[region_name] = _Region )
VAR _AvgMemory = CALCULATE ( [Avg Memory], DimRegions[region_name] = _Region )
VAR _AvgLatency = CALCULATE ( [Avg API Latency], DimRegions[region_name] = _Region )

VAR _SeverityScore = 100 - ( DIVIDE ( _CriticalInc, _TotalInc, 0 ) * 50 ) - ( DIVIDE ( _WarningInc, _TotalInc, 0 ) * 30 )
VAR _InfraScore = 100 - ( DIVIDE ( _AvgCPU, 100 ) * 20 ) - ( DIVIDE ( _AvgMemory, 100 ) * 20 ) - ( MIN ( DIVIDE ( _AvgLatency, 1000 ), 1 ) * 10 )

VAR _HealthScore = ( _SeverityScore * 0.6 ) + ( _InfraScore * 0.4 )
RETURN
    MAX ( 0, MIN ( 100, _HealthScore ) )
```

---

## 📁 Display Folder: **AI Insights** (Trend Analysis)

### Incident Trend (7-Day Slope)
```dax
Incident Trend 7D =
VAR _Dates = TOPN ( 7, VALUES ( FactIncidents[event_date] ), FactIncidents[event_date], DESC )
VAR _DailyCounts = ADDCOLUMNS (
    _Dates,
    "Count", CALCULATE ( [Total Incidents] )
)
VAR _XValues = ADDCOLUMNS ( _DailyCounts, "X", RANKX ( _DailyCounts, [Count], , ASC, DENSE ) )
VAR _Slope = 
    DIVIDE (
        COUNTROWS ( _XValues ) * SUMX ( _XValues, [X] * [Count] ) - SUMX ( _XValues, [X] ) * SUMX ( _XValues, [Count] ),
        COUNTROWS ( _XValues ) * SUMX ( _XValues, [X] * [X] ) - SUMX ( _XValues, [X] ) * SUMX ( _XValues, [X] ),
        0
    )
RETURN
    _Slope
```

### Anomaly Score
```dax
Anomaly Score =
VAR _CurrentHour = HOUR ( MAX ( FactIncidents[incident_timestamp] ) )
VAR _AvgHourly = CALCULATE (
    AVERAGEX (
        VALUES ( FactIncidents[event_date] ),
        CALCULATE ( [Total Incidents], HOUR ( FactIncidents[incident_timestamp] ) = _CurrentHour )
    ),
    ALL ( FactIncidents )
)
VAR _CurrentCount = CALCULATE ( [Total Incidents], HOUR ( FactIncidents[incident_timestamp] ) = _CurrentHour )
VAR _StdDev = CALCULATE (
    STDEVX.P (
        VALUES ( FactIncidents[event_date] ),
        CALCULATE ( [Total Incidents], HOUR ( FactIncidents[incident_timestamp] ) = _CurrentHour )
    ),
    ALL ( FactIncidents )
)
VAR _ZScore = DIVIDE ( _CurrentCount - _AvgHourly, _StdDev, 0 )
VAR _Anomaly = IF ( ABS ( _ZScore ) > 2, 1, 0 )
RETURN
    _Anomaly
```

---

## 📁 Display Folder: **Incident KPIs** (Cardinality Helpers)

### Distinct Servers
```dax
Distinct Servers =
DISTINCTCOUNT ( FactIncidents[server_id] )
```

### Distinct Regions
```dax
Distinct Regions =
DISTINCTCOUNT ( FactIncidents[region_key] )
```

### Distinct Event Types
```dax
Distinct Event Types =
DISTINCTCOUNT ( FactIncidents[event_type] )
```

---

## Usage Notes

| Measure Category | Recommended Visual | Slicers |
|------------------|-------------------|---------|
| Incident KPIs | Card, KPI, Table | Region, Server, Event Type, Severity |
| Infrastructure | Line Chart, Area Chart | Time (Date/Hour), Region, Server |
| Availability | Gauge, Card | Region, Server |
| AI Insights | Table, Scatter Plot | None (computed) |

**Performance Tips**:
- All time-intelligence measures use `FactIncidents[event_date]` (DATE column) for optimal partitioning
- `Health Score` and `Anomaly Score` are compute-intensive — use in cards/tables only, not as slicers
- `MTTR` requires critical incidents followed by non-critical — ensure data quality for accurate results
- For large datasets (>2M rows), consider creating calculated tables for `Daily Incidents` / `Hourly Incidents` aggregations

**Formatting**:
- Incident counts: `#,##0`
- Percentages: `0.0%`
- Latency: `#,##0 ms`
- Health/Availability/SLA: `0.0%`
- MTTR: `#,##0.0 hrs`