# SmartOps AI — Dashboard Validation Checklist

**Project:** SmartOps AI Microsoft Fabric Implementation  
**Version:** 1.0  
**Date:** 2026-07-07  
**Author:** Anishh Daas  
**Status:** Production Validation  

---

This checklist validates every layer of the SmartOps AI Power BI dashboard — from workspace configuration through to portfolio readiness. Each item is a binary pass/fail gate. **All items must pass** before the dashboard is considered interview-ready.

---

## 1. Workspace Checklist

- [ ] Workspace created in Microsoft Fabric with dedicated capacity (F64 or higher)
- [ ] Workspace named `SmartOps AI — Production` (or approved convention)
- [ ] Workspace description documents purpose, data sources, and refresh cadence
- [ ] Contributors assigned with least-privilege roles (Viewer / Contributor / Admin)
- [ ] Git integration enabled and connected to `smartops-ai` repository
- [ ] Deployment pipeline configured (Dev → Test → Prod) with auto-deploy on merge to `main`
- [ ] Workspace documentation (`README.md`, data dictionary) published in workspace OneLake
- [ ] Sensitivity labels applied (Confidential / Internal / Public) per org policy
- [ ] Workspace-level tenant settings reviewed (export, sharing, external access)
- [ ] Capacity metrics monitoring enabled (CPU, memory, query duration)

---

## 2. Snowflake Connection Checklist

- [ ] Snowflake warehouse `SMARTOPS_WH` provisioned with auto-suspend (60s) and auto-resume
- [ ] Role `SMARTOPS_READER` created with `SELECT` on `SMARTOPS_DB.ANALYTICS` schema only
- [ ] Network policy restricts access to Fabric IP ranges (CIDR allowlist)
- [ ] PrivateLink / Azure Private Endpoint configured (no public internet egress)
- [ ] Connection uses OAuth 2.0 client credentials (service principal), not username/password
- [ ] Secret stored in Azure Key Vault; Fabric linked service references Key Vault secret
- [ ] Query timeout set to 300 seconds; statement timeout 600 seconds
- [ ] Connection test succeeds from Fabric Data Pipeline (test query returns 1 row)
- [ ] Incremental refresh watermark column (`LOAD_TS`) indexed in Snowflake
- [ ] Row-level security policies in Snowflake align with Fabric RLS roles

---

## 3. Semantic Model Checklist

- [ ] Model uses **Import mode** for dimension tables, **DirectQuery** for fact tables > 10M rows
- [ ] All tables renamed to business-friendly names (no `DIM_`, `FACT_` prefixes in model)
- [ ] Columns hidden from report view: surrogate keys, technical columns, watermark columns
- [ ] Data types correct: `Date` for dates, `Decimal` for currency, `Whole Number` for counts
- [ ] Sort-by-column configured for all ordinal categories (e.g., `Month Name` sorted by `Month Number`)
- [ ] Hierarchies defined: `Date → Year → Quarter → Month → Day`, `Product → Category → Subcategory → SKU`
- [ ] Calculation groups created for time intelligence (YoY, YTD, Rolling 12M) — no duplicate measures
- [ ] No bidirectional relationships unless explicitly documented and performance-tested
- [ ] Model size < 1 GB (Import) or DirectQuery latency < 2s per visual (95th percentile)
- [ ] `MODEL.DOCUMENTATION` annotation on every table and measure (description, owner, last updated)

---

## 4. Relationship Validation

- [ ] All relationships are **One-to-Many** (dimension → fact) — no Many-to-Many without bridge table
- [ ] Cross-filter direction set to **Single** (dimension filters fact) unless bidirectional justified
- [ ] Referential integrity enforced: `Validate` button in Model view shows 0 orphaned keys
- [ ] Inactive relationships documented with `USERELATIONSHIP` usage in specific measures
- [ ] Composite keys not used; surrogate integer keys on all dimension tables
- [ ] Relationship cardinality matches Snowflake PK/FK constraints
- [ ] Ambiguity resolution: no multiple active paths between same table pair
- [ ] Date table marked as **Date Table** with contiguous date range (no gaps)
- [ ] Relationships tested with `CROSSFILTER` both directions in DAX Studio — results match expectations
- [ ] Performance: `RELATED()` and `RELATEDTABLE()` queries execute in < 50ms on sample data

---

## 5. DAX Validation

- [ ] All measures follow **measure naming convention**: `Measure Name` (Pascal Case, no prefixes)
- [ ] No calculated columns in fact tables — all logic in measures or Power Query
- [ ] Time intelligence uses `TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATESYTD` — no custom date math
- [ ] `CALCULATE` context transition tested: row context → filter context behavior verified
- [ ] `KEEPFILTERS` used where slicer selection must not be overridden
- [ ] `REMOVEFILTERS` / `ALL` used intentionally and documented (not as default)
- [ ] `VAR` / `RETURN` pattern used for all measures > 3 lines — single return point
- [ ] No `IFERROR` masking errors — root cause fixed in data or logic
- [ ] `DIVIDE` used instead of `/` for all ratio measures (handles divide-by-zero)
- [ ] Measure dependencies documented in `MEASURE_DEPENDENCIES.md` (generated via DAX Studio DMV)
- [ ] **Performance:** All measures execute in < 200ms on 1M-row fact (cold cache) in DAX Studio
- [ ] **No circular dependencies** — verified via `DMV_MEASURE_DEPENDENCIES` query
- [ ] **Formatting:** Currency measures use `$#,##0.00`; percentages use `0.0%`; counts use `#,##0`

---

## 6. KPI Validation

| KPI | Target | Source Measure | Visual Type | Status |
|-----|--------|----------------|-------------|--------|
| Revenue (MTD) | ≥ $2.5M | `[Revenue MTD]` | Card + Trend | [ ] |
| Revenue YoY Growth | ≥ 15% | `[Revenue YoY %]` | KPI Indicator | [ ] |
| Gross Margin | ≥ 42% | `[Gross Margin %]` | Gauge | [ ] |
| Active Customers | ≥ 1,200 | `[Active Customers]` | Card | [ ] |
| Churn Rate (Monthly) | ≤ 3.5% | `[Churn Rate %]` | KPI Indicator | [ ] |
| Avg Order Value | ≥ $185 | `[Avg Order Value]` | Card + Sparkline | [ ] |
| Order Fulfillment SLA | ≥ 98% | `[Fulfillment SLA %]` | Gauge | [ ] |
| Inventory Turns | ≥ 8.5x | `[Inventory Turns]` | Card | [ ] |

- [ ] Each KPI has **status threshold** (Good / Warning / Critical) with conditional formatting
- [ ] KPI trend sparklines show 12-month history with current month highlighted
- [ ] KPI tooltips show prior period, variance, and variance %
- [ ] KPI cards respond to all global slicers (Date, Region, Segment, Channel)
- [ ] KPI values reconcile to Snowflake source within 0.1% tolerance

---

## 7. Visual Validation

- [ ] **Color palette** matches `04_PowerBI_Theme.json` — no hardcoded hex values in visuals
- [ ] **Typography:** Title 16pt, Axis 11pt, Data labels 10pt, Tooltip 11pt — consistent across all pages
- [ ] **Chart types** appropriate: Line (trend), Bar (comparison), Scatter (correlation), Map (geo), Table (detail)
- [ ] **No pie charts** — replaced with donut (max 5 segments) or bar charts
- [ ] **Data labels** shown only where value adds clarity (not on dense line charts)
- [ ] **Gridlines** subtle (10% opacity); axis lines visible; zero baseline shown for bar charts
- [ ] **Legends** positioned bottom/right; hidden when single series
- [ ] **Conditional formatting** on tables: revenue green/red, margin traffic lights, variance arrows
- [ ] **Small multiples** used for segment/region breakdowns instead of stacked bars > 8 series
- [ ] **Visual headers** show drill icons, focus mode, export — consistent placement
- [ ] **Alt text** set on every visual (accessibility): describes insight, not chart type
- [ ] **Dynamic titles** reflect slicer selection (e.g., "Revenue by Region — APAC, Q3 2025")

---

## 8. Navigation Validation

- [ ] **Page Navigator** (custom button bar) on every page — Home, Executive, Operations, Finance, Customer, Settings
- [ ] **Bookmark navigation** for drill-through return buttons (Back to Summary)
- [ ] **Page tooltips** configured as report page tooltips (not visual tooltips) for KPI cards
- [ ] **Tab order** logical: slicers → KPIs → charts → tables (tested with Tab key)
- [ ] **Hidden pages** (Data Dictionary, Admin, Appendix) excluded from navigator, accessible via bookmark
- [ ] **Mobile navigator** collapses to hamburger menu on < 600px width
- [ ] **Deep linking** works: `?page=Executive&slicer_Region=EMEA` opens correct state
- [ ] **Page load time** < 3s (cold) / < 1s (warm) measured in Performance Analyzer

---

## 9. Drill-Through Validation

| Drill-Through Target | Source Fields | Destination Page | Back Button |
|----------------------|---------------|------------------|-------------|
| Customer Detail | `Customer Key` | Customer 360 | [ ] |
| Product Detail | `Product Key` | Product Performance | [ ] |
| Order Detail | `Order Key` | Order Explorer | [ ] |
| Region Detail | `Region` | Regional Deep Dive | [ ] |

- [ ] Drill-through filters **propagate correctly** — destination page filtered to shows only shows selected entity
- [ ] **Keep all filters** toggle tested: On = global filters persist; Off = only drill field filters
- [ ] **Cross-report drill-through** configured if targeting separate report (not required for single report)
- [ ] **Drill-through visual** (table/matrix) has "Drill Through" header icon visible
- [ ] **Return button** on destination page uses bookmark to return to exact prior page + filter state
- [ ] Drill-through works in **Power BI Mobile** app (tested on iOS/Android)

---

## 10. Tooltip Validation

- [ ] **Report page tooltips** used for all KPI cards (rich context: sparkline, variance, prior period)
- [ ] **Visual tooltips** on charts show: category, value, % of total, variance vs prior period
- [ ] **Tooltip page size** set to 400×320px (tooltip canvas) — content fits without scroll
- [ ] **Tooltip fields** include only relevant measures — no technical columns
- [ ] **Conditional formatting** in tooltips (red/green variance, up/down arrows)
- [ ] **Tooltip delay** default (0.5s) — no custom delay overriding user expectation
- [ ] Tooltips render correctly in **Power BI Service**, **Mobile**, and **Publish to Web**

---

## 11. Filter & Slicer Validation

- [ ] **Slicer panel** (vertical) on left: Date (hierarchy), Region, Segment, Channel, Product Category
- [ ] **Date slicer** uses **Relative Time** (Last 12 Months default) + **Between** for custom range
- [ ] **Sync slicers** across all report pages — verified in "Sync Slicers" pane
- [ ] **Slicer search** enabled for lists > 20 items (Region, Product Category)
- [ ] **Multi-select** with Ctrl+Click; **Select All** / **Clear** buttons visible
- [ ] **Visual-level filters** documented: e.g., "Top 10 Customers by Revenue" on Customer table
- [ ] **Page-level filters** applied: `Is Active = TRUE`, `Fiscal Year ≥ 2023`
- [ ] **Report-level filters** applied: `Tenant = SmartOps`, `Data Quality = Validated`
- [ ] **Slicer state persists** on drill-through and bookmark navigation
- [ ] **Performance:** Slicer dropdown loads in < 1s (cached) / < 3s (cold)

---

## 12. Mobile Layout Validation

- [ ] **Mobile layout** configured per page in Power BI Desktop (Phone view)
- [ ] **Stack order:** KPI cards (2×2 grid) → Primary chart → Secondary chart → Table (collapsed)
- [ ] **Font sizes** minimum 12pt on mobile — no horizontal scrolling
- [ ] **Touch targets** minimum 44×44px (slicer dropdowns, buttons, drill icons)
- [ ] **Landscape mode** tested — layout reflows without clipping
- [ ] **Offline caching** enabled for published app (last 30 days)
- [ ] **QR code** generated for mobile app deep link — tested on device
- [ ] **Push notifications** configured for data refresh completion (optional)

---

## 13. Accessibility Checklist

- [ ] **Color contrast** ≥ 4.5:1 (text) / 3:1 (UI elements) — verified with Colour Contrast Analyser
- [ ] **Color-blind safe palette** — no red/green solely for status; use icons + text
- [ ] **Alt text** on every visual (meaningful description, not "Bar chart")
- [ ] **Tab navigation** reaches all interactive elements in logical order
- [ ] **Focus indicators** visible (2px outline, theme accent color)
- [ ] **Screen reader** tested with NVDA / JAWS — all measures, slicers, buttons announced
- [ ] **Keyboard shortcuts** documented: Ctrl+Shift+F (filter pane), Ctrl+Shift+S (slicer pane)
- [ ] **Language** set to English (en-US) in report settings
- [ ] **Reduce motion** respected — no auto-animating carousels or transitions
- [ ] **High contrast mode** (Windows) tested — all visuals readable

---

## 14. Performance Checklist

- [ ] **Performance Analyzer** run on each page — no visual > 2s DAX query (warm cache)
- [ ] **DirectQuery** visuals show "DirectQuery" badge; fallback to Import for < 10M rows
- [ ] **Aggregations** configured for high-cardinality fact tables (pre-aggregated tables in model)
- [ ] **Query reduction** enabled: "Limit rows" on tables, "Top N" on visuals
- [ ] **VertiPaq Analyzer** run — no columns > 1M distinct values unoptimized
- [ ] **Memory usage** < 80% capacity at peak refresh
- [ ] **Refresh duration** < 15 minutes (full) / < 3 minutes (incremental)
- [ ] **Concurrent user test** — 20 users, all visuals render < 3s (load test script in repo)
- [ ] **DAX Studio** query plan shows no `CallbackDataID` (storage engine only)
- [ ] **No `FILTER` over fact table** in measures — use `CALCULATE` with column filters

---

## 15. Security Checklist

- [ ] **RLS roles** defined: `Region Manager` (filters `Region`), `Segment Lead` (filters `Segment`)
- [ ] **RLS tested** with "View as Role" — each role sees only authorized data
- [ ] **RLS on Snowflake** aligned — same predicates pushed via DirectQuery
- [ ] **Object-level security (OLS)** hides `Customer PII` table from non-Admin roles
- [ ] **Sensitivity labels** on report: Confidential (internal), Highly Confidential (finance page)
- [ ] **Export restrictions:** Viewers cannot export data / summarize / copy visual data
- [ ] **Embed tokens** (if embedded) use `EmbedTokenType.Report` with RLS effective identity
- [ ] **Audit logging** enabled in Fabric Admin Portal — query, export, share events captured
- [ ] **Service principal** for automated refresh has `Dataset.ReadWrite` only
- [ ] **No hardcoded secrets** in PBIX — all connections use parameterized data source credentials

---

## 16. Refresh Validation

- [ ] **Incremental refresh** configured: `LOAD_TS` watermark, 2-year rolling window, 1-day overlap
- [ ] **Refresh schedule:** Daily 02:00 UTC (incremental), Sunday 01:00 UTC (full)
- [ ] **Refresh history** (last 30 days): 0 failures, 0 data latency > 4 hours
- [ ] **Failure alerting:** Power Automate flow → Teams channel + email on refresh failure
- [ ] **Data validation post-refresh:** Row counts match Snowflake within 0.5%
- [ ] **KPI reconciliation** post-refresh: Revenue variance < 0.1% vs Snowflake
- [ ] **Schema drift detection:** Power Query `Table.Schema` comparison step fails refresh on mismatch
- [ ] **Long-running query** cancellation: 4-hour timeout with graceful rollback
- [ ] **Parallel partition refresh** enabled (max 4 partitions concurrent)
- [ ] **Refresh dependency** on Snowflake warehouse auto-resume verified

---

## 17. Demo Readiness Checklist

- [ ] **Demo script** documented (`DEMO_SCRIPT.md`) — 10-min narrative with talking points
- [ ] **Demo data snapshot** captured — static PBIX backup for offline demo
- [ ] **Bookmarks** created for each demo scene: Executive Overview → Customer Deep Dive → Ops Alert
- [ ] **Narrative tooltips** on demo bookmarks explain "why this matters"
- [ ] **Screen recording** (4K, 30fps) of full demo uploaded to portfolio artifacts
- [ ] **PowerPoint appendix** with architecture diagram, data flow, DAX samples
- [ ] **Q&A prep doc** with 10 anticipated questions + answers (performance, RLS, refresh, scale)
- [ ] **Offline mode** tested: PBIX opens and navigates without Fabric connection
- [ ] **Mobile demo** recorded on phone — portrait + landscape
- [ ] **Portfolio write-up** (Markdown) in repo: problem, solution, impact, tech stack, lessons learned

---

## 18. Final Pre-GitHub Checklist

- [ ] **Repository structure** matches `docs/fabric/` conventions — all 7 docs present
- [ ] **No local file paths** in PBIX (use relative / parameterized paths)
- [ ] **No sample data** in repo — PBIX published to Fabric, not committed
- [ ] **`.gitignore`** excludes `.pbix`, `.pbip`, `*.tmp`, `.cache/`
- [ ] **README.md** at repo root links to Fabric docs folder and live report URL
- [ ] **License** file present (MIT or org-standard)
- [ ] **Contributing guide** documents branch strategy, PR template, review requirements
- [ ] **Changelog** (`CHANGELOG.md`) follows Keep a Changelog format
- [ ] **Dependabot** / Renovate configured for GitHub Actions, Python, Power BI REST API
- [ ] **GitHub Actions** workflow: lint (Power BI Lint), validate (Tabular Editor), deploy (Fabric CLI)
- [ ] **Documentation** rendered via GitHub Pages or MkDocs — verified live
- [ ] **Portfolio tag** `v1.0-portfolio` created on `main` branch

---

## Portfolio Acceptance Criteria

The dashboard is **interview-ready** only when **ALL** criteria below are **PASS**:

| # | Criterion | Pass Condition | Evidence Required |
|---|-----------|----------------|-------------------|
| 1 | **End-to-end data flow** | Snowflake → Fabric → Power BI → Mobile verified | Refresh history + mobile recording |
| 2 | **KPI accuracy** | All 8 KPIs reconcile to Snowflake within 0.1% | Reconciliation workbook (Excel/CSV) |
| 3 | **Performance** | All pages < 2s DAX (warm), < 3s (cold) | Performance Analyzer export (JSON) |
| 4 | **RLS enforcement** | Each role sees only authorized rows | "View as Role" screenshots (4 roles) |
| 5 | **Accessibility** | WCAG 2.1 AA compliant | Colour Contrast Analyser report + NVDA test log |
| 6 | **DAX quality** | No circular deps, all measures < 200ms, VAR/RETURN pattern | DAX Studio DMV exports |
| 7 | **Incremental refresh** | 30-day history: 0 failures, < 3 min avg | Refresh history CSV export |
| 8 | **Mobile parity** | All desktop insights accessible on phone | Mobile recording (portrait + landscape) |
| 9 | **Documentation complete** | All 7 fabric docs + README + CHANGELOG + DEMO_SCRIPT | Repo file tree screenshot |
| 10 | **Demo artifact** | 10-min recorded walkthrough + Q&A doc | Video link + PDF in repo |
| 11 | **Git hygiene** | Clean `main`, tagged release, CI passing | GitHub Actions badge green |
| 12 | **Architecture diagram** | Current, accurate, in repo (draw.io / Mermaid) | `docs/architecture.mmd` rendered |

---

**Sign-off:**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Data Engineer | | | |
| Analytics Lead | | | |
| Engineering Manager | | | |

---

*Generated for SmartOps AI Portfolio — Confidential*