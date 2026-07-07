# Microsoft Fabric Build Guide for macOS
## SmartOps AI — End-to-End Implementation

> **Prerequisites**: macOS 12+, Microsoft Fabric enabled tenant, Snowflake account with `SMARTOPS` schema access, Power BI Desktop (via Parallels/VM) or Power BI Service

---

## 1. Creating a Fabric Workspace

### 1.1 Via Fabric Portal (Recommended)
1. Open [app.fabric.microsoft.com](https://app.fabric.microsoft.com) in Safari/Chrome
2. Sign in with your organizational account (Fabric-enabled tenant)
3. Navigate to **Workspaces** → **New workspace**
4. Configure:
   - **Name**: `SmartOps AI`
   - **Description**: `Operational intelligence dashboards for SmartOps AI`
   - **Contact list**: Add workspace admins
   - **Storage**: Use default (OneLake)
5. Click **Apply**

### 1.2 Via Fabric CLI (Alternative)
```bash
# Install Fabric CLI
pip install microsoft-fabric-cli

# Authenticate
fab auth login

# Create workspace
fab workspace create --name "SmartOps AI" --description "Operational intelligence dashboards"
```

### 1.3 Verify Workspace
- Note the **Workspace ID** from URL: `https://app.fabric.microsoft.com/workspaces/<WORKSPACE_ID>`
- This ID is needed for deployment scripts and API calls

---

## 2. Connecting to Snowflake

### 2.1 Create Snowflake Connection in Fabric
1. In Fabric workspace → **Data** → **New item** → **Dataflow Gen2**
2. Name: `Snowflake_SmartOps_Connection`
3. In Power Query Online editor:
   - **Get Data** → **Snowflake**
   - **Server**: `<account>.snowflakecomputing.com`
   - **Warehouse**: `SMARTOPS_WH` (or your compute warehouse)
   - **Database**: `SMARTOPS_DB`
   - **Schema**: `SMARTOPS`
   - **Authentication**: `OAuth` (recommended) or `Basic` with key-pair auth
4. Test connection → **OK**

### 2.2 Configure OAuth (Production)
1. In Snowflake: Create security integration
   ```sql
   CREATE SECURITY INTEGRATION FABRIC_OAUTH
     TYPE = OAUTH
     ENABLED = TRUE
     OAUTH_CLIENT = 'MICROSOFT_FABRIC'
     OAUTH_REDIRECT_URL = 'https://app.fabric.microsoft.com/'
     OAUTH_ISSUE_REFRESH_TOKENS = TRUE;
   ```
2. Grant to role: `GRANT USAGE ON INTEGRATION FABRIC_OAUTH TO ROLE SMARTOPS_READER;`

### 2.3 Save Connection as Shared Dataset
- In Dataflow → **Home** → **Manage connections** → **Convert to shared connection**
- Name: `Snowflake_SmartOps_Shared`
- Enables reuse across Dataflows, Notebooks, and Semantic Models

---

## 3. Importing the Semantic Model

### 3.1 Option A: Power BI Desktop (Full Fidelity)
1. Launch Power BI Desktop (via Parallels Desktop / UTM / VMware Fusion on macOS)
2. **Get Data** → **Snowflake** → Use shared connection from §2.3
3. Select tables from `SMARTOPS` schema per `01_Snowflake_SQL.sql`:
   - `DIM_DATE`
   - `DIM_CUSTOMER`
   - `DIM_PRODUCT`
   - `DIM_REGION`
   - `DIM_CHANNEL`
   - `FACT_SALES`
   - `FACT_INVENTORY`
   - `FACT_OPERATIONS`
4. **Transform Data** → Apply steps from `01_Snowflake_SQL.sql` (CTE logic)
5. **Close & Apply**

### 3.2 Option B: Fabric Semantic Model (Direct Lake)
1. In Fabric workspace → **New item** → **Semantic model**
2. Name: `SmartOps_SemanticModel`
3. **Get Data** → **Snowflake** → Use shared connection
4. Enable **Direct Lake** mode (requires Fabric F64+ capacity)
5. Select same tables as Option A
6. Model will remain in OneLake with live Snowflake connection

### 3.3 Verify Import
- Check **Model view** → All 8 tables present
- Row counts match Snowflake:
  ```sql
  SELECT 'DIM_DATE' t, COUNT(*) c FROM SMARTOPS.DIM_DATE
  UNION ALL SELECT 'DIM_CUSTOMER', COUNT(*) FROM SMARTOPS.DIM_CUSTOMER
  -- ... repeat for all tables
  ```

---

## 4. Creating Relationships

### 4.1 Relationship Map (from `02_Data_Model.md`)

| From Table | From Column | To Table | To Column | Cardinality | Cross-filter |
|------------|-------------|----------|-----------|-------------|--------------|
| `FACT_SALES` | `DATE_KEY` | `DIM_DATE` | `DATE_KEY` | Many-to-One | Single |
| `FACT_SALES` | `CUSTOMER_KEY` | `DIM_CUSTOMER` | `CUSTOMER_KEY` | Many-to-One | Single |
| `FACT_SALES` | `PRODUCT_KEY` | `DIM_PRODUCT` | `PRODUCT_KEY` | Many-to-One | Single |
| `FACT_SALES` | `REGION_KEY` | `DIM_REGION` | `REGION_KEY` | Many-to-One | Single |
| `FACT_SALES` | `CHANNEL_KEY` | `DIM_CHANNEL` | `CHANNEL_KEY` | Many-to-One | Single |
| `FACT_INVENTORY` | `DATE_KEY` | `DIM_DATE` | `DATE_KEY` | Many-to-One | Single |
| `FACT_INVENTORY` | `PRODUCT_KEY` | `DIM_PRODUCT` | `PRODUCT_KEY` | Many-to-One | Single |
| `FACT_INVENTORY` | `REGION_KEY` | `DIM_REGION` | `REGION_KEY` | Many-to-One | Single |
| `FACT_OPERATIONS` | `DATE_KEY` | `DIM_DATE` | `DATE_KEY` | Many-to-One | Single |
| `FACT_OPERATIONS` | `REGION_KEY` | `DIM_REGION` | `REGION_KEY` | Many-to-One | Single |
| `FACT_OPERATIONS` | `CHANNEL_KEY` | `DIM_CHANNEL` | `CHANNEL_KEY` | Many-to-One | Single |

### 4.2 Create in Power BI / Fabric
1. Switch to **Model view**
2. Drag `DATE_KEY` from `DIM_DATE` to `DATE_KEY` in each fact table
3. Repeat for all keys above
4. **Verify**: Each relationship shows `1:*` with single cross-filter direction
5. **Mark `DIM_DATE` as Date Table**: Right-click `DIM_DATE` → **Mark as date table** → `DATE_KEY`

### 4.3 Set Relationship Properties
- **Security**: Restrict to `Single` (not `Both`) for performance
- **Rely on referential integrity**: Enable if Snowflake enforces FKs

---

## 5. Importing the Power BI Theme

### 5.1 Theme File
Source: `docs/fabric/04_PowerBI_Theme.json`

### 5.2 Import Steps
1. In Power BI Desktop: **View** → **Themes** → **Switch theme** → **Import theme**
2. Browse to `04_PowerBI_Theme.json` → **Open**
3. Theme applies: Colors, fonts, visual defaults

### 5.3 Verify Theme Application
- **Data colors**: Should show SmartOps palette (blues, teal, amber, semantic red/green)
- **Text classes**: Header/Title/Body fonts set to Inter/IBM Plex Sans
- **Visual defaults**: Card backgrounds, border radius, hover states configured

### 5.4 For Fabric Service (Power BI Service)
1. In Fabric workspace → **Semantic model** → **Settings** → **Theme**
2. Upload `04_PowerBI_Theme.json`
3. All reports connected to this model inherit theme

---

## 6. Creating All Five Dashboard Pages

> Reference: `docs/fabric/05_Dashboard_Wireframes.md` for layout specs

### 6.1 Page 1: Executive Overview
**Page name**: `Executive Overview`
**Canvas size**: 16:9 (1280 × 720)

| Visual | Type | Position | Key Measures |
|--------|------|----------|--------------|
| KPI Cards (4) | Card | Top row, 4-col | Total Revenue, YoY Growth, Gross Margin, Active Customers |
| Revenue Trend | Line chart | Middle-left (60%) | `[Revenue]` by Month |
| Top 10 Products | Bar chart | Middle-right (40%) | `[Revenue]` by Product |
| Regional Map | Filled map | Bottom (full) | `[Revenue]` by Region |
| Period Slicer | Slicer | Top-right | `DIM_DATE[Fiscal_Year]`, `DIM_DATE[Fiscal_Quarter]` |

**Build steps**:
1. Insert 4 **Card** visuals → Set fields to measures from §7
2. Insert **Line chart** → Axis: `DIM_DATE[Year_Month]`, Values: `[Revenue]`
3. Insert **Clustered bar chart** → Axis: `DIM_PRODUCT[Product_Name]`, Values: `[Revenue]`, Top N = 10
4. Insert **Filled map** → Location: `DIM_REGION[Region_Name]`, Values: `[Revenue]`
5. Insert **Slicer** → Field: `DIM_DATE[Fiscal_Year]` → Format as **Dropdown**
6. Insert **Slicer** → Field: `DIM_DATE[Fiscal_Quarter]` → Format as **Tiles**

### 6.2 Page 2: Sales Performance
**Page name**: `Sales Performance`
**Canvas size**: 16:9

| Visual | Type | Position | Key Measures |
|--------|------|----------|--------------|
| Sales by Channel | Donut chart | Top-left | `[Revenue]` by `DIM_CHANNEL[Channel_Name]` |
| Sales by Customer Tier | Stacked bar | Top-right | `[Revenue]` by `DIM_CUSTOMER[Tier]` |
| Monthly Comparison | Combo chart | Middle | `[Revenue]`, `[Prior_Year_Revenue]`, `[YoY_%]` |
| Customer Table | Table | Bottom | Customer, Revenue, Orders, Avg Order Value, YoY% |

**Build steps**:
1. **Donut**: Category = `Channel_Name`, Values = `[Revenue]`
2. **Stacked bar**: Axis = `Tier`, Values = `[Revenue]`, Legend = `Fiscal_Quarter`
3. **Combo chart**: Line = `[Revenue]` & `[Prior_Year_Revenue]`, Column = `[YoY_%]`
4. **Table**: Values = Customer_Name, `[Revenue]`, `[Order_Count]`, `[Avg_Order_Value]`, `[YoY_%]`
5. Add **Drillthrough** on Customer → Target: Page 4 (Customer Detail)

### 6.3 Page 3: Inventory & Operations
**Page name**: `Inventory & Operations`
**Canvas size**: 16:9

| Visual | Type | Position | Key Measures |
|--------|------|----------|--------------|
| Inventory Turnover | Gauge | Top-left | `[Inventory_Turnover]` |
| Stockout Rate | Gauge | Top-right | `[Stockout_Rate]` |
| Inventory Aging | Stacked column | Middle-left | `[Inventory_Value]` by `Aging_Bucket` |
| Operations Efficiency | Line chart | Middle-right | `[Ops_Efficiency_%]` by Week |
| Warehouse Table | Table | Bottom | Warehouse, Inventory Value, Turnover, Stockouts |

**Build steps**:
1. **Gauges**: Set min/max/target per `03_DAX_Measures.md` definitions
2. **Stacked column**: Axis = `Aging_Bucket` (0-30, 31-60, 61-90, 90+), Values = `[Inventory_Value]`
3. **Line chart**: Axis = `DIM_DATE[Year_Week]`, Values = `[Ops_Efficiency_%]`
4. **Table**: From `DIM_REGION` (warehouse level) with measures

### 6.4 Page 4: Customer Detail (Drillthrough Target)
**Page name**: `Customer Detail`
**Canvas size**: 16:9
**Drillthrough filter**: `DIM_CUSTOMER[Customer_Key]`

| Visual | Type | Position | Key Measures |
|--------|------|----------|--------------|
| Customer Header | Card | Top | Customer Name, Tier, Region |
| Revenue Trend | Line chart | Left | `[Revenue]` by Month |
| Product Mix | Donut | Right | `[Revenue]` by Product Category |
| Order History | Table | Bottom | Date, Product, Quantity, Revenue, Margin |

### 6.5 Page 5: Product Analytics
**Page name**: `Product Analytics`
**Canvas size**: 16:9

| Visual | Type | Position | Key Measures |
|--------|------|----------|--------------|
| Product Performance | Scatter chart | Top | X: `[Revenue]`, Y: `[Margin_%]`, Size: `[Units_Sold]` |
| Category Breakdown | Treemap | Middle-left | `[Revenue]` by Category/Subcategory |
| New vs Returning | Stacked area | Middle-right | `[New_Customer_Revenue]`, `[Returning_Customer_Revenue]` |
| SKU Table | Table | Bottom | SKU, Revenue, Margin, Units, Velocity |

---

## 7. Adding All DAX Measures

> Source: `docs/fabric/03_DAX_Measures.md`

### 7.1 Create Measure Table (Best Practice)
1. **Model view** → Right-click white space → **New measure table**
2. Name: `_Measures`
3. All measures below go in this table

### 7.2 Core Revenue Measures
```dax
// Base Revenue
Revenue = SUM(FACT_SALES[Revenue_Amount])

// Prior Year Revenue
Prior_Year_Revenue = 
CALCULATE(
    [Revenue],
    SAMEPERIODLASTYEAR(DIM_DATE[Date])
)

// Year-over-Year Growth %
YoY_% = 
DIVIDE(
    [Revenue] - [Prior_Year_Revenue],
    [Prior_Year_Revenue],
    0
)

// Gross Margin
Gross_Margin = 
DIVIDE(
    [Revenue] - SUM(FACT_SALES[COGS_Amount]),
    [Revenue],
    0
)

// Average Order Value
Avg_Order_Value = 
DIVIDE(
    [Revenue],
    DISTINCTCOUNT(FACT_SALES[Order_Key]),
    0
)
```

### 7.3 Customer Measures
```dax
Active_Customers = 
CALCULATE(
    DISTINCTCOUNT(FACT_SALES[Customer_Key]),
    FACT_SALES[Revenue_Amount] > 0
)

New_Customers = 
CALCULATE(
    DISTINCTCOUNT(FACT_SALES[Customer_Key]),
    FILTER(
        DIM_CUSTOMER,
        DIM_CUSTOMER[First_Order_Date] = MAX(DIM_DATE[Date])
    )
)

Returning_Customers = [Active_Customers] - [New_Customers]

Customer_Lifetime_Value = 
DIVIDE(
    [Revenue],
    [Active_Customers],
    0
)
```

### 7.4 Inventory Measures
```dax
Inventory_Value = SUM(FACT_INVENTORY[Inventory_Value])

Inventory_Turnover = 
DIVIDE(
    SUM(FACT_SALES[COGS_Amount]),
    AVERAGE(FACT_INVENTORY[Inventory_Value]),
    0
)

Stockout_Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(FACT_INVENTORY), FACT_INVENTORY[On_Hand_Qty] = 0),
    COUNTROWS(FACT_INVENTORY),
    0
)

Days_of_Supply = 
DIVIDE(
    SUM(FACT_INVENTORY[On_Hand_Qty]),
    DIVIDE(SUM(FACT_SALES[Units_Sold]), DISTINCTCOUNT(DIM_DATE[Date])),
    0
)
```

### 7.5 Operations Measures
```dax
Ops_Efficiency_% = 
DIVIDE(
    SUM(FACT_OPERATIONS[Actual_Output]),
    SUM(FACT_OPERATIONS[Planned_Output]),
    0
)

On_Time_Delivery_% = 
DIVIDE(
    CALCULATE(COUNTROWS(FACT_OPERATIONS), FACT_OPERATIONS[Delivered_On_Time] = TRUE),
    COUNTROWS(FACT_OPERATIONS),
    0
)

Order_Cycle_Time_Days = 
AVERAGE(FACT_OPERATIONS[Cycle_Time_Days])
```

### 7.6 Time Intelligence Measures
```dax
// MTD, QTD, YTD
Revenue_MTD = TOTALMTD([Revenue], DIM_DATE[Date])
Revenue_QTD = TOTALQTD([Revenue], DIM_DATE[Date])
Revenue_YTD = TOTALYTD([Revenue], DIM_DATE[Date])

// Rolling 12 Months
Revenue_R12M = 
CALCULATE(
    [Revenue],
    DATESINPERIOD(DIM_DATE[Date], MAX(DIM_DATE[Date]), -12, MONTH)
)

// Prior Period Comparisons
Revenue_Prior_Month = 
CALCULATE(
    [Revenue],
    PARALLELPERIOD(DIM_DATE[Date], -1, MONTH)
)
```

### 7.7 Formatting Measures
- Set **Format** for each measure in **Measure tools**:
  - Currency: `$#,##0` (Revenue, Margin, Inventory Value)
  - Percentage: `0.0%` (YoY%, Margins, Rates)
  - Whole number: `#,##0` (Customers, Orders, Units)
  - Decimal: `#,##0.0` (Turnover, Days of Supply)

---

## 8. Configuring Slicers

### 8.1 Global Slicers (Sync Across Pages)
1. Insert slicer on **Executive Overview** page
2. **Format** → **Sync slicers** → Check all 5 pages
3. Configure each:

| Slicer | Field | Type | Default | Sync |
|--------|-------|------|---------|------|
| Date Range | `DIM_DATE[Date]` | Between | Last 12 months | All pages |
| Fiscal Year | `DIM_DATE[Fiscal_Year]` | Dropdown | Current FY | All pages |
| Fiscal Quarter | `DIM_DATE[Fiscal_Quarter]` | Tiles | Current Q | All pages |
| Region | `DIM_REGION[Region_Name]` | List | All selected | Pages 1,2,3,5 |
| Channel | `DIM_CHANNEL[Channel_Name]` | Checkbox | All | Pages 1,2,5 |
| Customer Tier | `DIM_CUSTOMER[Tier]` | Dropdown | All | Pages 2,4 |

### 8.2 Slicer Formatting
- **Selection controls**: Show "Select all" + Search box
- **Layout**: Horizontal for ≤4 items, Vertical for >4
- **Title**: Show field name, font size 12pt, bold
- **Background**: Theme card background, border radius 4px

### 8.3 Page-Level Slicers
- **Page 3 (Inventory)**: Add `DIM_PRODUCT[Category]` slicer (not synced)
- **Page 4 (Customer Detail)**: Drillthrough filter replaces Customer slicer
- **Page 5 (Product)**: Add `DIM_PRODUCT[Brand]` slicer (not synced)

---

## 9. Publishing the Report

### 9.1 From Power BI Desktop
1. **File** → **Publish** → **Publish to Power BI**
2. Select workspace: `SmartOps AI`
3. Name: `SmartOps AI Dashboard`
4. Wait for upload → **Open in browser**

### 9.2 From Fabric Portal (Semantic Model + Report)
1. In workspace → **New item** → **Report**
2. Connect to `SmartOps_SemanticModel`
3. Build pages per §6 using web authoring
4. **Save** → Name: `SmartOps AI Dashboard`

### 9.3 Configure Dataset Settings
1. Workspace → **SmartOps_SemanticModel** → **Settings**
2. **Scheduled refresh** → Add schedule (see §10)
3. **Parameters** → Set Snowflake warehouse parameter if using parameterized connection
4. **Row-level security** → Define roles if needed (see below)

### 9.4 Row-Level Security (Optional)
```dax
// Role: Regional_Manager
// Table: DIM_REGION
// DAX: [Region_Key] = LOOKUPVALUE(DIM_REGION[Region_Key], DIM_REGION[Manager_UPN], USERPRINCIPALNAME())
```
1. **Modeling** → **Manage roles** → Create roles
2. Assign users in **Security** tab after publish

---

## 10. Scheduling Refresh

### 10.1 Refresh Requirements
- **Direct Lake** (§3.2): No refresh needed (live connection)
- **Import mode** (§3.1): Scheduled refresh required

### 10.2 Configure Schedule (Import Mode)
1. Workspace → `SmartOps_SemanticModel` → **Settings** → **Scheduled refresh**
2. **Keep data up to date**: On
3. **Frequency**: Daily
4. **Time zone**: `America/Los_Angeles` (or your local)
5. **Times**: `02:00`, `06:00`, `10:00`, `14:00`, `18:00`, `22:00` (6x/day)
6. **Notify on failure**: Add admin emails
7. **Apply**

### 10.3 Incremental Refresh (Large Datasets)
1. In Power BI Desktop: **Transform Data** → Right-click `FACT_SALES` → **Incremental refresh**
2. Configure:
   - **Archive data**: 3 years
   - **Refresh data**: 2 days
   - **Detect data changes**: `DIM_DATE[Date]`
3. Republish — Fabric respects incremental policy

### 10.4 XMLA Endpoint (Advanced)
- Enable in **Capacity settings** → **XMLA endpoint** → **Read/Write**
- Allows Tabular Editor, ALM Toolkit, programmatic refresh via TMSL

---

## 11. Performance Optimization

### 11.1 Model Optimization
| Technique | Implementation |
|-----------|----------------|
| **Star schema** | Already implemented per §4 |
| **Remove unused columns** | In Power Query: Remove `ETL_Load_Date`, `Source_System` from all tables |
| **Data types** | Use `Decimal` for currency, `Int` for keys, `Date` for dates |
| **Hierarchies** | Create: `Date → Year → Quarter → Month → Day`; `Region → Country → State → City` |
| **Sort by column** | `Month_Name` sort by `Month_Number`; `Fiscal_Quarter` sort by `Quarter_Number` |

### 11.2 DAX Optimization
- **Use variables**: All measures in §7 use `VAR`/`RETURN` pattern
- **Avoid `FILTER`CALCULATE` in iterators**: Use `SUMX`/`AVERAGEX` with simple expressions
- **Leverage storage engine**: Prefer `SUM`/`COUNT` over `SUMX` where possible
- **Time intelligence**: Use `TOTALYTD`/`SAMEPERIODLASTYEAR` not custom `FILTER`

### 11.3 Visual Optimization
| Visual | Optimization |
|--------|--------------|
| Tables | Limit rows: Top N = 50, enable **Pagination** |
| Maps | Use **Azure Maps** visual (better performance than Filled Map) |
| High-cardinality slicers | Use **Search-enabled dropdown**, not List |
| Tooltips | Disable on dense visuals; use **Report page tooltips** instead |

### 11.4 Capacity Sizing
| Workload | Recommended SKU |
|----------|-----------------|
| Dev/Test | F2 / P1 |
| Production (<10M rows) | F8 / P2 |
| Production (10M-100M rows) | F16 / P3 |
| Production (100M+ rows, Direct Lake) | F64 / P4 |

### 11.5 Monitoring
- **Fabric Monitor app**: Track refresh duration, query latency, memory
- **DAX Query View**: Analyze slow queries (`>1s`)
- **VertiPaq Analyzer** (Tabular Editor): Check cardinality, encoding hints

---

## 12. Validation Checklist

### 12.1 Data Validation
- [ ] Row counts match Snowflake source for all 8 tables
- [ ] Revenue totals match Snowflake: `SELECT SUM(Revenue_Amount) FROM SMARTOPS.FACT_SALES`
- [ ] Distinct customer count matches: `SELECT COUNT(DISTINCT Customer_Key) FROM SMARTOPS.FACT_SALES`
- [ ] Date range covers expected period (no gaps in `DIM_DATE`)
- [ ] No duplicate keys in dimension tables

### 12.2 Model Validation
- [ ] All 11 relationships created with correct cardinality
- [ ] `DIM_DATE` marked as date table
- [ ] No ambiguous relationships (single active path between tables)
- [ ] All measures in `_Measures` table (no implicit measures)
- [ ] Format strings set on all measures

### 12.3 Report Validation
- [ ] All 5 pages render without errors
- [ ] Slicers sync correctly across pages 1-3,5
- [ ] Drillthrough from Page 2 → Page 4 works
- [ ] Bookmarks/buttons (if any) navigate correctly
- [ ] Theme colors applied consistently
- [ ] Mobile layout configured (View → Mobile layout)

### 12.4 Functional Validation
- [ ] Scheduled refresh runs successfully (check history)
- [ ] Incremental refresh partitions created (if enabled)
- [ ] RLS roles filter data correctly (test as user)
- [ ] Export to PDF/PowerPoint works
- [ ] Embed token generation works (if embedding)

### 12.5 Performance Validation
- [ ] Page load < 3s on F8+ capacity
- [ ] DAX queries < 500ms for standard visuals
- [ ] No visual shows "Too many values" warning
- [ ] Memory per query < 500MB

---

## 13. Troubleshooting

### 13.1 Connection Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| "Cannot connect to Snowflake" | Network/Firewall | Allow Fabric IP ranges in Snowflake network policy |
| "Authentication failed" | OAuth config | Verify security integration `FABRIC_OAUTH` exists and granted |
| "Warehouse not found" | Wrong warehouse name | Use `SHOW WAREHOUSES` in Snowflake; match exactly |
| "Permission denied" | Role grants | `GRANT USAGE ON DATABASE SMARTOPS_DB TO ROLE SMARTOPS_READER` |

### 13.2 Refresh Failures

| Error | Fix |
|-------|-----|
| "Timeout" | Reduce partition size; enable incremental refresh |
| "Memory limit exceeded" | Upgrade capacity; optimize DAX; remove high-cardinality columns |
| "Data source credentials invalid" | Update credentials in **Settings** → **Data source credentials** |
| "Partition not found" | Rebuild incremental refresh policy; republish |

### 13.3 Visual Errors

| Issue | Fix |
|-------|-----|
| Blank visual | Check field wells; verify measure returns data |
| "Can't display visual" | Reduce data points; add filters; check for circular dependency |
| Map not rendering | Use Azure Maps visual; verify `Region_Name` matches Azure geography |
| Slicer not syncing | Verify **Sync slicers** pane; check page names match exactly |

### 13.4 DAX Errors

| Error | Fix |
|-------|-----|
| "Circular dependency" | Use `CALCULATE` with explicit filter; avoid bidirectional relationships |
| "Column not found" | Verify column name in **Data view**; check for typos |
| "Function not supported in DirectQuery" | Rewrite using supported functions; or switch to Import mode |
| "Memory error in `SUMX`" | Replace with `SUM` + `CALCULATE`; reduce iterator cardinality |

### 13.5 Performance Degradation

1. **Run Performance Analyzer** (Power BI Desktop: **View** → **Performance Analyzer**)
2. Identify slowest visual → Optimize its DAX or reduce granularity
3. Check **VertiPaq Analyzer** for:
   - High cardinality columns → Remove or bucket
   - Poor encoding → Apply encoding hints (`Value` vs `Hash`)
   - Large dictionaries → Use surrogate keys (already done)

### 13.6 macOS-Specific Issues

| Issue | Workaround |
|-------|------------|
| Power BI Desktop not native | Use Parallels Desktop (best), UTM (free), or VMware Fusion |
| Keyboard shortcuts differ | Map `Cmd` → `Ctrl` in VM settings |
| File paths for PBIX | Use shared folder `/Users/ishaan/Projects/smartops-ai` mounted in VM |
| Browser authentication | Use Safari/Chrome in macOS; copy token to VM browser if needed |

---

## Appendix: Quick Reference Commands

```bash
# Fabric CLI workspace operations
fab workspace list
fab workspace get --name "SmartOps AI"
fab item list --workspace "SmartOps AI"

# Semantic model refresh via CLI
fab item invoke --workspace "SmartOps AI" --item "SmartOps_SemanticModel" --operation refresh

# Check refresh status
fab item get --workspace "SmartOps AI" --item "SmartOps_SemanticModel" --details
```

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-07 | SmartOps AI Team | Initial build guide |

---

**Next Steps**: After validation, configure **Deployment Pipelines** (Dev → Test → Prod) and **Audience-specific apps** for executive vs operational users.