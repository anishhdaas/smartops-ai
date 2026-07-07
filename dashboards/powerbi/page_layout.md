# dashboards/powerbi/page_layout.md

## Overview
All pages use a **16:9 (1920 × 1080 px) canvas** with a **12‑column grid**. The grid spacing is 16 px between columns and rows, top/bottom margin 24 px. The dark enterprise theme (`enterprise_theme.json`) provides background `#1B1B1B`, foreground `#F3F2F2`, and accent `#00B7C3`.

---

## 1. Executive Overview

### Canvas Grid
- **Columns:** 12 (each 140 px wide).
- **Rows:** 120 px height.
- **Gutters:** 16 px.
- **Margins:** 24 px on all sides.

### KPI Placement
| KPI | Grid (col‑start / col‑span, row‑start / row‑span) | Size |
|-----|-----------------------------------------------|------|
| Total Incidents | 1 / 2, 1 / 1 | 360 × 120 |
| Critical Incidents | 3 / 2, 1 / 1 | 360 × 120 |
| Health Score | 5 / 2, 1 / 1 | 360 × 120 |
| Incidents Today | 7 / 2, 1 / 1 | 360 × 120 |
| Last 24 h | 9 / 2, 1 / 1 | 360 × 120 |

### Chart Placement
| Visual | Grid | Size |
|--------|------|------|
| Incident Volume Trend (Line) | 1 / 8, 2 / 2 | 960 × 240 |
| Critical Incident % Donut | 9 / 4, 2 / 2 | 480 × 240 |
| Server Health Multi‑row Card | 1 / 12, 4 / 1 | 1440 × 120 |

### Slicers
- **Date Range** – column 10‑12, row 1, dropdown style.
- **Refresh Timestamp** – tiny text in top‑right (column 12).

### Tables
- No tables on this page; KPI tiles act as summary cards.

### Navigation
- Fixed **bottom navigation bar** (48 px height) with icons for the five pages. Active page highlighted with accent `#00B7C3`.

### Drill‑through Buttons
- Each KPI tile has a transparent overlay button titled **"Details"** that drills to a dedicated detail page filtered by the KPI.

### Spacing & Responsive Layout
- On screens < 1024 px the grid collapses to 6 columns; KPI tiles stack vertically (full width). Charts retain aspect ratio and re‑flow to a single column.
- Padding of 16 px between all visuals; minimum touch target 48 px.

---

## 2. Infrastructure Monitoring

### Canvas Grid
- **Columns:** 12 (140 px).
- **Rows:** 150 px (taller for column charts).
- **Gutters/Margins:** same as Overview.

### KPI Placement
| KPI | Grid | Size |
|-----|------|------|
| Total Servers (Card) | 5 / 3, 1 / 1 | 360 × 120 |

### Chart Placement
| Visual | Grid | Size |
|--------|------|------|
| Avg CPU % (Clustered Column) | 1 / 6, 2 / 3 | 960 × 360 |
| Avg Memory % (Clustered Column) | 7 / 6, 2 / 3 | 960 × 360 |
| API Latency (Line) | 1 / 12, 5 / 2 | 1920 × 240 |
| Top‑10 Servers (Table) | 1 / 12, 7 / 3 | 1920 × 360 |

### Slicers & Controls
- **Server Group** slicer – column 1‑4, row 1 (dropdown).
- **Region** dropdown – column 8, row 1.
- **Date Range** slicer – column 9‑12, row 1 (hidden on mobile).

### Tables
- **Top‑10 Servers by Health** – placed at rows 7‑9 spanning full width.

### Navigation
- Bottom bar identical to Overview.

### Drill‑through Buttons
- KPI card and each column chart include a **"Server Detail"** button that passes the selected server name.
- Table rows link to **Server Detail** page.

### Spacing & Responsive Layout
- On tablet (< 1280 px) the CPU and Memory column charts stack vertically.
- Table scrolls horizontally if required.
- Slicers collapse into a **slide‑out drawer** accessible via a funnel icon on the navigation bar.

---

## 3. AI Incident Intelligence

### Canvas Grid
- **Columns:** 12 (140 px).
- **Rows:** 120 px.

### KPI Placement
| KPI | Grid | Size |
|-----|------|------|
| Incident Growth % (Card) | 1 / 3, 4 / 1 | 360 × 120 |
| Summary Card (overall) | 4 / 9, 4 / 1 | 1440 × 120 |

### Chart Placement
| Visual | Grid | Size |
|--------|------|------|
| Severity Funnel | 1 / 5, 2 / 2 | 800 × 240 |
| Incidents vs CPU Scatter | 6 / 7, 2 / 2 | 1120 × 240 |
| Recent Critical Incidents (Table) | 1 / 12, 5 / 3 | 1920 × 360 |

### Slicers & Controls
- **Incident Type** slicer – column 1‑4, row 1.
- **Severity** dropdown – column 8, row 1.
- **Date Range** slicer – column 9‑12, row 1 (collapsed on mobile).

### Tables
- **Recent Critical Incidents** – full‑width table occupying rows 5‑7.

### Navigation
- Bottom navigation bar unchanged.

### Drill‑through Buttons
- Funnel slices drill to **Severity Detail** page.
- Scatter points drill to **Server Detail** (filtered by server).
- Table rows drill to **Incident Detail** page.

### Spacing & Responsive Layout
- On screens < 960 px the funnel and scatter charts stack vertically.
- KPI font size reduces to 80 %.
- Slicers move into a **floating panel** toggled by a filter icon.

---

## 4. Data Warehouse

### Canvas Grid
- **Columns:** 12 (140 px).
- **Rows:** 140 px.

### KPI Placement
| KPI | Grid | Size |
|-----|------|------|
| Number of Tables (Card) | 5 / 3, 1 / 1 | 360 × 120 |

### Chart Placement
| Visual | Grid | Size |
|--------|------|------|
| Load Size by Source (Stacked Column) | 1 / 8, 2 / 3 | 1280 × 420 |
| Refresh Duration (Line) | 9 / 4, 2 / 3 | 640 × 420 |
| Data Quality Issues (Donut) | 1 / 6, 5 / 2 | 960 × 240 |
| Row Count by Schema (Matrix) | 7 / 6, 5‑7, 5 / 3 | 960 × 420 |

### Slicers & Controls
- **Data Source** slicer – column 1‑4, row 1.
- **Issue Category** dropdown – column 8, row 1.
- **Date Range** slicer – column 9‑12, row 1 (collapses on small viewports).

### Tables
- No traditional table visual on this page; the matrix serves as a detailed table.

### Navigation
- Bottom navigation bar persists.

### Drill‑through Buttons
- Clicking a source segment in the stacked column opens **Source Detail** page filtered to that source.
- Matrix cells drill to **Table Detail** page.
- Donut segments drill to **Issue List** page for that category.

### Spacing & Responsive Layout
- For viewports < 1024 px the stacked column and line chart become a single column (stacked vertically).
- Matrix retains scrollbars; columns wrap when width exceeds the viewport.
- All slicers collapse into a **right‑hand slide‑out pane**.

---

## 5. Data Quality

### Canvas Grid
- **Columns:** 12 (140 px).
- **Rows:** 130 px.

### KPI Placement
| KPI | Grid | Size |
|-----|------|------|
| Total Issues (Card) | 1 / 3, 1 / 1 | 360 × 120 |
| Data Freshness (Card) | 7 / 3, 1 / 1 | 720 × 120 |

### Chart Placement
| Visual | Grid | Size |
|--------|------|------|
| Issues by Severity (Bar) | 1 / 6, 2 / 2 | 960 × 240 |
| Issue Trend 90 d (Line) | 7 / 6, 2 / 2 | 960 × 240 |
| Top 20 Tables (Issue Rate) (Table) | 1 / 12, 4‑6, 4 / 3 | 1920 × 360 |

### Slicers & Controls
- **Issue Type** slicer – column 4‑6, row 1.
- **Date Range** slicer – column 10‑12, row 1 (hidden on mobile).
- **Severity** filter dropdown integrated into the bar chart header.

### Tables
- **Top 20 Tables** – full‑width table with conditional formatting (red when issue rate > 5 %).

### Navigation
- Same bottom navigation bar.

### Drill‑through Buttons
- Bar segments drill to **Severity Detail** page.
- Table rows drill to **Table Issue Detail** page.
- Card “Total Issues” drills to **Issues List** page.

### Spacing & Responsive Layout
- On narrow screens (< 960 px) KPI cards stack, and the two main charts collapse into a single column.
- Slicer panel becomes a **hamburger menu**.
- Minimum 16 px padding between each visual; touch targets ≥ 48 px.

---

## Global Elements (All Pages)
- **Header:** Persistent across pages; contains report title, last‑refresh timestamp, and an **Export PDF** button.
- **Navigation Bar:** Fixed at the bottom, 48 px high, icons for the five pages, active icon accent `#00B7C3`.
- **Bookmarks:** Each page includes at least three bookmarks (Default view, Filtered view, Focused view) managed through Power BI’s Bookmarks pane.
- **Theme:** All pages use the `enterprise_theme.json` dark enterprise theme.
- **Responsive Settings:** Power BI *Responsive* option enabled on every visual; the 12‑column grid logic ensures graceful degradation.
