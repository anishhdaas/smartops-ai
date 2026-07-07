# SmartOps AI — Visual Hierarchy Specification

> **Design Language**: Microsoft Fluent 2 + Executive Dashboard Best Practices  
> **Principle**: Clarity > Density — every pixel must earn its place

---

## 1. Hierarchy Layers (Z-Axis)

| Layer | Z-Index | Elevation | Purpose | Examples |
|-------|---------|-----------|---------|----------|
| **L0: Canvas** | `z-base` (0) | `elevation-0` | Page background | `neutral-50` / `neutral-0` |
| **L1: Content Cards** | `z-raised` (10) | `elevation-1` | Primary data containers | KPI cards, charts, tables |
| **L2: Interactive Cards (Hover)** | `z-raised` (10) | `elevation-2` | Hover/focus state | Card hover, row highlight |
| **L3: Sticky Headers** | `z-sticky` (100) | `elevation-2` | Persistent navigation | Nav bar, table sticky headers |
| **L4: Overlays** | `z-overlay` (200) | `elevation-3` | Tooltips, popovers, dropdowns | Chart tooltips, slicer dropdowns |
| **L5: Modals/Drawers** | `z-modal` (500) | `elevation-4` | Focused tasks | Drill-through, config dialogs |
| **L6: Notifications** | `z-toast` (1000) | `elevation-4` | System alerts | Error toasts, refresh notifications |
| **L7: Tooltips (Above Toasts)** | `z-tooltip` (1100) | `elevation-3` | Hover details | Data point tooltips |

---

## 2. Visual Weight (Y-Axis Priority)

### Priority 1: Critical Action / Alert (Immediate Attention)
- **KPI Cards** — Top row, largest type (`display-1`), boldest weight
- **Critical Alerts** — Red status badge + pulsing indicator
- **SLA Breach Indicators** — Prominent badge, fixed position

### Priority 2: Primary Metrics (Scan in <3 seconds)
- **Trend Charts** — Line/area charts with clear axis
- **Health Score Gauges** — Semi-circle gauges, color-coded
- **Top-N Tables** — Ranked lists with sparklines

### Priority 3: Contextual Detail (On Demand)
- **Drill-through Tables** — Expandable rows, pagination
- **Filter/Slicer Panels** — Collapsible, right-aligned
- **Annotations/Insights** — AI-generated callouts

### Priority 4: Metadata / Chrome (Peripheral)
- **Page Title/Breadcrumb** — `heading-2`, muted color
- **Last Refresh Timestamp** — `caption`, right-aligned
- **Export/Share Actions** — Icon buttons, low contrast

---

## 3. Layout Zones (X-Axis Grid)

### Desktop (≥1440px) — 12 Column Grid

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  NAV BAR (full width, sticky)                                               │
├──────────────┬──────────────────────────────────────────────────────────────┤
│              │  PAGE HEADER (title + breadcrumb + actions)                 │
│   SIDEBAR    ├──────────────┬──────────────┬──────────────┬────────────────┤
│  (collapsible│  KPI ROW     │  KPI ROW     │  KPI ROW     │  KPI ROW       │
│   280px)     │  (3-col ea)  │              │              │                │
│              ├──────────────┴──────────────┴──────────────┴────────────────┤
│              │  PRIMARY CHARTS ROW (2×2 or 1×3)                             │
│              │  ┌──────────────┬──────────────┬──────────────┐              │
│              │  │  CHART 1     │  CHART 2     │  CHART 3     │              │
│              │  │  (4-col)     │  (4-col)     │  (4-col)     │              │
│              │  └──────────────┴──────────────┴──────────────┘              │
│              ├──────────────┬──────────────┬──────────────┬────────────────┤
│              │  DETAIL TABLE│  AI INSIGHTS │  SLICER PANEL│                │
│              │  (6-col)     │  (3-col)     │  (3-col)     │                │
│              └──────────────┴──────────────┴──────────────┴────────────────┘
```

### Tablet (768-1023px) — 8 Column Grid

```
┌──────────────────────────────────────────────────────┐
│  NAV BAR (hamburger menu)                            │
├──────────────────────────────────────────────────────┤
│  PAGE HEADER                                         │
├──────────────┬──────────────┬──────────────┬─────────┤
│  KPI 1       │  KPI 2       │  KPI 3       │  KPI 4  │  (2-col each)
├──────────────┴──────────────┴──────────────┴─────────┤
│  CHART 1 (8-col)     │  CHART 2 (8-col)              │  (stacked)
├──────────────────────┴───────────────────────────────┤
│  TABLE (8-col)  │  INSIGHTS (8-col)  │  SLICERS (8)  │  (stacked)
└──────────────────────────────────────────────────────┘
```

### Mobile (≤767px) — 4 Column Grid (Single Column Stack)

```
┌────────────────────────────┐
│  NAV BAR (hamburger)       │
├────────────────────────────┤
│  PAGE HEADER               │
├────────────────────────────┤
│  KPI 1                     │
│  KPI 2                     │
│  KPI 3                     │
│  KPI 4                     │
├────────────────────────────┤
│  CHART 1                   │
│  CHART 2                   │
│  CHART 3                   │
├────────────────────────────┤
│  TABLE (collapsible rows)  │
├────────────────────────────┤
│  AI INSIGHTS (accordion)   │
├────────────────────────────┤
│  SLICERS (bottom sheet)    │
└────────────────────────────┘
```

---

## 4. Component Visual Hierarchy

### KPI Card (Executive Tier)

```
┌─────────────────────────────────────────┐
│  ┌───────────────────────────────────┐  │  ← Card (elevation-1, radius-lg)
│  │  LABEL          TREND ▲ +12%      │  │     heading-3 / weight-semibold
│  │  ─────────────────────────────    │  │     divider (neutral-100)
│  │                                   │  │
│  │        1,234,567                  │  │  ← VALUE: display-1 / weight-bold
│  │                                   │  │     font-display + tabular-nums
│  │  vs last week: +12.3%  📈         │  │  ← COMPARISON: body-sm / weight-medium
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Spacing**: `space-6` padding, `space-4` internal gap  
**Typography**: Label=`heading-3`, Value=`display-1`, Trend=`body-sm`  
**Color**: Value=`neutral-900`, Positive trend=`status-success`, Negative=`status-critical`

---

### Chart Card (Primary Metrics Tier)

```
┌─────────────────────────────────────────────────────────────┐
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Title                    [Filter ▼] [Export ▼]       │  │  ← Header: heading-3 + actions
│  │  ─────────────────────────────────────────────────    │  │
│  │                                                       │  │
│  │        ████████████████████████                       │  │  ← Chart area (min 300px height)
│  │      ████████████████████████████                     │  │
│  │    ████████████████████████████████                   │  │
│  │                                                       │  │
│  │  0    6    12    18    24    (hours)                 │  │  ← Axis: caption
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Legend:  ● CPU  ● Memory  ● Network  ● Disk         │  │  ← Footer: caption + viz colors
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Spacing**: `space-4` card padding, `space-3` header/footer  
**Chart Area**: Min-height 300px desktop, 250px tablet, 200px mobile  
**Responsive**: Legend stacks horizontally → vertically on tablet

---

### Data Table (Detail Tier)

```
┌──────────────────────────────────────────────────────────────────────┐
│  ┌────┬──────────────┬──────────┬──────────┬──────────┬────────────┐  │
│  │ ▼  │ Server       │ CPU %    │ Memory % │ Status   │ Trend      │  │  ← Header: heading-4
│  ├────┼──────────────┼──────────┼──────────┼──────────┼────────────┤  │
│  │ ▶  │ web-01-bang  │  87%     │  92%     │ ⬤ CRIT   │ ████▁▁▁    │  │  ← Row: body + mono
│  │    │ web-02-bang  │  45%     │  61%     │ ✓ HEALTHY│ ▁▁▁▁▁▁▁    │  │
│  │    │ api-01-sin   │  23%     │  34%     │ ✓ HEALTHY│ ▁▁██▁▁▁    │  │
│  │    │ db-01-tok    │  67%     │  78%     │ ▲ WARN   │ ▁▁▁▁██▁    │  │
│  └────┴──────────────┴──────────┴──────────┴──────────┴────────────┘  │
│  ◀ Prev  1  2  3  ...  12  Next ▶    Showing 1-4 of 47                │  │  ← Pagination: caption
└─────────────────────────────────────────────────────────────────────────┘
```

**Column Hierarchy**:
1. **Expand** (icon, 32px) — `z-overlay` on hover
2. **Entity Name** (primary key, 200px) — `body` weight-medium
3. **Primary Metric** (numeric, 100px) — `mono` tabular-nums
4. **Secondary Metric** (numeric, 100px) — `mono` tabular-nums
5. **Status** (badge, 80px) — `caption` weight-semibold + icon
6. **Sparkline** (trend, 120px) — inline SVG, `viz-1` color

**Hover**: Row `elevation-2`, background `neutral-50`  
**Expand**: Reveals detail drawer (L5), pushes content down

---

### AI Insight Card (Contextual Tier)

```
┌─────────────────────────────────────────────────────────────┐
│  ┌───────────────────────────────────────────────────────┐  │
│  │  💡 AI Insight                    [Dismiss] [▼]        │  │  ← heading-4 + actions
│  │  ─────────────────────────────────────────────────    │  │
│  │                                                       │  │
│  │  "CPU spike detected on web-01-bang at 14:32 UTC.   │  │  ← body text
│  │   Correlated with deploy v2.4.1. Recommend rollback."│  │
│  │                                                       │  │
│  │  ┌───────────────────────────────────────────────┐   │  │  ← Evidence chip group
│  │  │ [Deploy v2.4.1] [CPU +340%] [Error rate +12%] │   │  │
│  │  └───────────────────────────────────────────────┘   │  │
│  │                                                       │  │
│  │  [View Details]  [Auto-Remediate]  [Snooze 1h]      │  │  ← Actions: button group
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Elevation**: `elevation-1` with left accent border (3px `brand-accent`)  
**Spacing**: `space-4` padding, `space-3` internal gaps  
**Actions**: Primary=`brand-primary`, Secondary=`neutral-200`, Ghost=transparent

---

### Slicer/Filter Panel (Control Tier)

```
┌────────────────────────────────────────┐
│  ┌────────────────────────────────────┐ │  ← Panel (fixed 300px desktop)
│  │  TIME RANGE              [Clear]   │ │     heading-3
│  │  ────────────────────────────────  │ │
│  │  [Last 1h ▼]  [Custom...]          │ │  ← Select + custom
│  ├────────────────────────────────────┤ │
│  │  REGIONS                       [✓] │ │  ← Multi-select with search
│  │  ────────────────────────────────  │ │
│  │  ☑ Bangalore  (142)                │ │
│  │  ☑ Singapore  (98)                 │ │
│  │  ☐ Tokyo       (67)                │ │
│  ├────────────────────────────────────┤ │
│  │  SEVERITY                      [✓] │ │
│  │  ────────────────────────────────  │ │
│  │  ⬤ CRITICAL   (12)                 │ │  ← Color-coded checkboxes
│  │  ▲ WARNING    (45)                 │ │
│  │  ● INFO       (203)                │ │
│  │  ✓ HEALTHY    (512)                │ │
│  └────────────────────────────────────┘ │
```

**Desktop**: Fixed right panel (300px), `position: sticky`  
**Tablet/Mobile**: Bottom sheet (slide up), `z-modal`  
**Spacing**: `space-4` panel padding, `space-5` group gap, `space-2` option gap

---

## 5. Color as Hierarchy Signal

| Signal | Color Treatment | Hierarchy Level |
|--------|-----------------|-----------------|
| **Critical Value** | `status-critical` text + `status-critical-bg` badge | P1 |
| **Warning Value** | `status-warning` text + `status-warning-bg` badge | P1 |
| **Primary Metric** | `neutral-900` (dark) / `neutral-900` (light) | P2 |
| **Secondary Metric** | `neutral-600` (dark) / `neutral-600` (light) | P3 |
| **Metadata** | `neutral-500` / `neutral-500` | P4 |
| **Disabled** | `neutral-300` text, 40% opacity | — |
| **Interactive** | `brand-primary` text/underline on hover | — |
| **AI-Generated** | `brand-accent` left border (3px) + icon | P3 |

---

## 6. Typography as Hierarchy Signal

| Element | Token | Weight | Color | Hierarchy |
|---------|-------|--------|-------|-----------|
| KPI Value | `display-1` | 700 (bold) | `neutral-900` | P1 |
| Page Title | `display-2` | 600 | `neutral-900` | P1 |
| Card Title | `heading-3` | 600 | `neutral-700` | P2 |
| Chart Axis Title | `body-sm` | 500 | `neutral-600` | P3 |
| Table Header | `heading-4` | 600 | `neutral-700` | P2 |
| Table Cell (Primary) | `body` | 400 | `neutral-900` | P2 |
| Table Cell (Secondary) | `body` | 400 | `neutral-600` | P3 |
| Sparkline Label | `caption` | 400 | `neutral-500` | P4 |
| Timestamp | `caption-sm` | 400 | `neutral-400` | P4 |

---

## 7. Spacing as Hierarchy Signal

| Relationship | Gap Token | Visual Effect |
|--------------|-----------|---------------|
| Page Sections | `space-section` (clamp 24-40px) | Major visual break |
| Card Groups | `space-component` (clamp 16-24px) | Related cards |
| Card Internal | `space-card` (clamp 12-16px) | Content breathing |
| Inline Elements | `space-inline` (clamp 8-12px) | Tight association |
| Micro (Icon-Text) | `space-micro` (4px) | Atomic unit |

---

## 8. Motion as Hierarchy Signal

| Transition | Duration | Easing | Trigger |
|------------|----------|--------|---------|
| Card Hover | 150ms | ease-out | Mouse enter |
| Row Expand | 200ms | ease-in-out | Click expand icon |
| Slicer Panel | 250ms | ease-out | Button click |
| Modal/Drawer | 300ms | ease-in-out | Action click |
| Toast In/Out | 200ms / 300ms | ease-out / ease-in | System event |
| Tooltip | 100ms / 150ms | ease-out | Hover/focus |
| KPI Value Change | 500ms | ease-out | Data refresh (count-up) |

**Reduced Motion**: All transitions → 0ms (respect `prefers-reduced-motion`)

---

## 9. Responsive Hierarchy Collapse

| Breakpoint | P1 (Always Visible) | P2 (Condensed) | P3 (Collapsed) | P4 (Hidden) |
|------------|---------------------|----------------|----------------|-------------|
| **Desktop** | KPI row, Primary charts | Detail tables, Insights | Slicer panel | Metadata |
| **Tablet** | KPI row (2×2), Primary chart (1) | Table (scrollable), Insights (accordion) | Slicer (bottom sheet) | Metadata |
| **Mobile** | KPI stack (4 cards), Primary chart | Table (cards), Insights (accordion) | Slicer (bottom sheet) | Metadata |

---

## 10. Print Hierarchy

```
@media print {
  /* Hide: Nav, slicers, actions, toasts, modals */
  .nav-bar, .slicer-panel, .actions, .toast, .modal { display: none; }
  
  /* Flatten: Cards → borders only, no shadows */
  .card { box-shadow: none; border: 1px solid var(--neutral-200); }
  
  /* Collapse: Spacing → space-2 */
  .section { margin-block: var(--space-2); }
  .card { padding: var(--space-2); }
  
  /* Typography: Serif body, smaller headings */
  .body { font-family: Georgia, serif; font-size: 12pt; }
  .heading-3 { font-size: 14pt; }
  
  /* Colors: High contrast only, no backgrounds */
  .status-badge { border: 1px solid currentColor; background: transparent; }
  
  /* Page breaks: Avoid breaking cards/tables */
  .card, .table { break-inside: avoid; }
}
```

---

## 11. Accessibility Hierarchy

| Requirement | Implementation |
|-------------|----------------|
| **Focus Order** | Matches visual hierarchy (top→bottom, left→right) |
| **Skip Links** | "Skip to main content" → first KPI card |
| **Landmarks** | `<nav>`, `<main>`, `<aside>` (slicers), `<footer>` |
| **Heading Structure** | h1=Page, h2=Section, h3=Card, h4=Sub-section |
| **Color-Independent** | Status = icon + text + color (never color-only) |
| **Contrast** | All text ≥4.5:1, UI elements ≥3:1 |
| **Zoom** | 200% zoom — no horizontal scroll, hierarchy preserved |

---

## 12. Implementation Checklist

- [ ] Z-index scale enforced via CSS custom properties
- [ ] Elevation tokens used (no arbitrary box-shadow)
- [ ] Typography tokens map to hierarchy levels
- [ ] Color aliases used (no raw hex in components)
- [ ] Spacing tokens responsive (clamp)
- [ ] Grid system implemented (12-col desktop, 8 tablet, 4 mobile)
- [ ] Focus order tested with keyboard
- [ ] Screen reader landmarks present
- [ ] Print stylesheet validated
- [ ] Reduced motion respected