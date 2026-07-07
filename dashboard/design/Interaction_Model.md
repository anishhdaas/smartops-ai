# SmartOps AI — Interaction Model Specification

> **Design Language**: Microsoft Fluent 2 + Power BI UX Patterns  
> **Principle**: Direct manipulation, progressive disclosure, keyboard-first

---

## 1. Interaction Principles

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **Direct Manipulation** | Click data → see detail | Drill-through on any visual element |
| **Progressive Disclosure** | Show summary → reveal detail | Expandable rows, accordions, tooltips |
| **Keyboard-First** | Every action accessible via keyboard | Tab order, arrow keys, shortcuts |
| **Immediate Feedback** | <100ms response | Optimistic UI, skeleton loaders |
| **Reversible Actions** | Undo/confirm destructive acts | Toast undo, confirmation modals |
| **Consistent Patterns** | Same interaction = same behavior | Standardized components |

---

## 2. Input Methods

### Mouse / Touch

| Gesture | Target | Action | Feedback |
|---------|--------|--------|----------|
| **Click** | Button, Link, Tab | Activate/Navigate | Ripple (150ms) |
| **Click** | Chart Data Point | Show Tooltip + Highlight Series | Tooltip (100ms), Series bold |
| **Click** | Table Row | Expand Detail Drawer | Slide down (200ms) |
| **Click** | KPI Card | Drill to Detail Page | Nav transition (300ms) |
| **Double-Click** | Table Cell (editable) | Inline Edit | Input focus |
| **Right-Click** | Any Data Element | Context Menu | Menu at cursor (z-overlay) |
| **Drag** | Column Header | Reorder Columns | Ghost column, drop zone |
| **Drag** | Slicer Handle | Resize Panel | Live resize |
| **Hover** | Interactive Element | Elevate + Cursor Change | elevation-2, pointer |
| **Hover** | Chart Legend Item | Highlight Series | Series opacity 1.0, others 0.3 |
| **Long Press** (Touch) | Table Row | Multi-Select Mode | Checkboxes appear |

### Keyboard

| Key / Chord | Context | Action |
|-------------|---------|--------|
| `Tab` / `Shift+Tab` | Global | Next/Previous focusable |
| `Enter` / `Space` | Button, Link, Checkbox | Activate / Toggle |
| `Escape` | Modal, Drawer, Tooltip, Menu | Close / Cancel |
| `Arrow Keys` | Menu, Tabs, Radio Group | Navigate options |
| `Home` / `End` | List, Table, Tabs | First / Last item |
| `Page Up` / `Page Down` | Table, Long List | Scroll by page |
| `Ctrl+F` / `Cmd+F` | Global | Global Search |
| `Ctrl+K` / `Cmd+K` | Global | Command Palette |
| `Ctrl+S` / `Cmd+S` | Edit Mode | Save |
| `Ctrl+Z` / `Cmd+Z` | Global | Undo Last Action |
| `/` | Global (non-input) | Focus Global Search |
| `?` | Global | Show Keyboard Shortcuts Help |

### Screen Reader (ARIA)

| Pattern | ARIA Attributes | Announcement |
|---------|-----------------|--------------|
| **KPI Card** | `role="region" aria-label="CPU Utilization, 87%, Critical"` | Full metric + status |
| **Chart** | `role="img" aria-roledescription="chart" aria-label="..."` | Summary + key insight |
| **Table** | `role="grid" aria-rowcount="47"` | Row/col position on navigate |
| **Slicer** | `role="listbox" aria-multiselectable="true"` | Selected count + options |
| **Toast** | `role="alert" aria-live="polite"` | Immediate announcement |
| **Loading** | `aria-busy="true" aria-live="polite"` | "Loading data..." |

---

## 3. Core Interaction Patterns

### 3.1 Drill-Through (Primary Navigation)

```
User Action          →  System Response                    →  Visual Feedback
─────────────────────────────────────────────────────────────────────────────
Click KPI Card       →  Navigate to Detail Page            →  Page transition (300ms)
Click Chart Point    →  Open Drill Modal (contextual)      →  Modal slide up (250ms)
Click Table Row      →  Expand Detail Drawer (inline)      →  Row expands (200ms)
Click "View All"     →  Navigate to Full List Page         →  Page transition
```

**Drill Modal Specification**:
- Size: 560px max-width, 80vh max-height
- Position: Centered, `z-modal`
- Content: Context-aware detail view (table, chart, or both)
- Header: Entity name + close button
- Actions: Primary (Export), Secondary (Close)
- Focus: Trap focus, return to trigger on close

**Detail Drawer Specification**:
- Position: Below expanded row, full width
- Height: Auto (max 400px), scrollable
- Animation: Slide down + fade in (200ms ease-out)
- Close: Click outside, `Escape`, or collapse icon
- Focus: First focusable element in drawer

### 3.2 Filtering & Slicing (Data Control)

```
User Action                    →  System Response              →  Visual Feedback
─────────────────────────────────────────────────────────────────────────────
Click Slicer Dropdown          →  Open Options Panel           →  Panel slide (150ms)
Select Checkbox                →  Apply Filter (debounced 300ms) →  Checkbox toggle + spinner
Type in Search                 →  Filter Options (debounced 150ms) →  Live filter
Click "Clear All"              →  Reset All Slicers            →  All unchecked + refresh
Change Time Range              →  Reload Data                  →  Global loading state
Click "Apply" (mobile)         →  Close Sheet + Apply          →  Sheet slide down (250ms)
```

**Debounce Rules**:
- Checkbox/Radio: 300ms (batch multiple selections)
- Search Input: 150ms (responsive feel)
- Date Picker: Immediate on confirm
- Range Slider: 300ms on release

**Loading States**:
- Skeleton cards for KPI row
- Shimmer on charts (preserve layout)
- Spinner overlay on tables (centered)
- Disable slicer interactions during fetch

### 3.3 Sorting & Pagination (Table Control)

```
User Action              →  System Response           →  Visual Feedback
─────────────────────────────────────────────────────────────────────────────
Click Column Header      →  Toggle Sort (ASC/DESC)    →  Sort icon rotate
Shift+Click Header       →  Multi-Column Sort         →  Badge "1", "2" on headers
Click Page Number        →  Navigate Page             →  Row fade out/in (150ms)
Click "Next/Prev"        →  Adjacent Page             →  Same
Change Page Size         →  Reload with New Size      →  Full table refresh
```

**Sort Indicators**:
- Unsorted: `↕` (neutral-400)
- ASC: `↑` (brand-primary)
- DESC: `↓` (brand-primary)
- Multi-sort: Numbered badges (1, 2, 3) next to icon

### 3.4 Time Range Selection (Global Context)

```
Control              →  Behavior                          →  Presets
─────────────────────────────────────────────────────────────────────────────
Dropdown             →  Click → Preset List               →  Last 1h, 6h, 24h, 7d, 30d
Custom Range         →  "Custom..." → Date Picker Modal   →  Start/End + Presets
Relative Input       →  "Last [N] [unit]" inputs          →  N=number, unit=min/hour/day
Auto-Refresh Toggle  →  On/Off (default: 30s)            →  10s, 30s, 1m, 5m, Off
```

**Time Range Persistence**: Saved per-user per-dashboard in localStorage

### 3.5 Export & Share (Data Portability)

```
Action          →  Flow                                    →  Output
─────────────────────────────────────────────────────────────────────────────
Export CSV      →  Click → Confirm → Download              →  Current view data
Export PNG      →  Click → Render → Download               →  Current visual
Export PDF      →  Click → Modal (options) → Generate      →  Full dashboard
Share Link      →  Click → Copy URL (with filters)         →  Deep link
Schedule Email  →  Click → Modal (recipients, cadence)     →  Background job
```

---

## 4. Component-Specific Interactions

### 4.1 KPI Card

| State | Trigger | Visual | Interaction |
|-------|---------|--------|-------------|
| **Default** | — | `elevation-1`, `neutral-0` bg | — |
| **Hover** | Mouse enter | `elevation-2`, `brand-primary` border-top (3px) | Cursor: pointer |
| **Focus** | Tab key | `elevation-2`, `brand-primary` focus ring (2px + 2px) | Outline: none |
| **Active** | Click/Enter | Scale 0.98 (50ms) | Ripple from center |
| **Loading** | Data fetch | Skeleton (shimmer `neutral-100`→`neutral-50`) | Pointer: wait |
| **Critical** | Value > threshold | `status-critical` left border (4px), pulsing badge | Pulse: 2s infinite |

### 4.2 Chart (Line, Area, Bar, Scatter)

| Interaction | Trigger | Behavior | Visual |
|-------------|---------|----------|--------|
| **Tooltip** | Hover/Focus data point | Show value + timestamp + series | `z-overlay`, follows cursor |
| **Series Toggle** | Click legend item | Show/hide series | Legend item strikethrough, opacity 0.3 |
| **Zoom** | Drag selection (brush) | Zoom to selection | Selection rect `brand-primary` 20% |
| **Pan** | Shift+Drag | Pan time range | Cursor: grab/grabbing |
| **Reset Zoom** | Double-click / Button | Reset to full range | Button in chart toolbar |
| **Crosshair** | Hover (line/area) | Vertical line + all series values | Line `neutral-300`, dots per series |
| **Drill** | Click data point | Open drill modal | Same as KPI drill |

**Touch Adaptations**:
- Tooltip: Tap to show, tap elsewhere to hide
- Zoom: Pinch gesture
- Pan: Two-finger drag
- Series toggle: Long-press legend → checkboxes

### 4.3 Data Table

| Interaction | Trigger | Behavior |
|-------------|---------|----------|
| **Row Select** | Click row / Checkbox | Toggle selection, highlight row |
| **Multi-Select** | Shift+Click / Ctrl+Click | Range / Toggle individual |
| **Select All** | Header checkbox | All visible / All pages (confirm) |
| **Row Expand** | Click expand icon / Enter | Open detail drawer below row |
| **Inline Edit** | Double-click editable cell | Replace with input, blur to save |
| **Column Resize** | Drag header divider | Live resize, persist width |
| **Column Reorder** | Drag header | Drop indicator, persist order |
| **Column Hide** | Header menu → Hide | Remove from view, show in menu |
| **Copy** | Ctrl+C (selected) | TSV to clipboard |
| **Context Menu** | Right-click row | Actions: Drill, Copy, Filter, Alert |

### 4.4 Slicer Panel

| Slicer Type | Interaction | Behavior |
|-------------|-------------|----------|
| **Single Select** | Radio / Dropdown | One active, click to change |
| **Multi-Select** | Checkboxes + Search | Multiple, "Select All" option |
| **Hierarchical** | Tree (expand/collapse) | Parent selects all children |
| **Date Range** | Dual Calendar / Presets | Start + End, relative presets |
| **Numeric Range** | Dual Input / Slider | Min/Max with step |
| **Text Search** | Input + Debounce | Filter options, highlight matches |

**Mobile Slicer**: Bottom sheet (slide up), full width, `z-modal`, swipe down to dismiss

### 4.5 AI Insight Card

| Interaction | Trigger | Behavior |
|-------------|---------|----------|
| **Expand** | Click card / Enter | Show full insight + evidence |
| **Dismiss** | Click ✕ / Swipe left | Remove from feed (undo toast 5s) |
| **Action** | Click button | Execute (remediate, snooze, link) |
| **Feedback** | Click 👍/👎 | Train model, show thanks toast |
| **Pin** | Click 📌 | Keep at top of feed |

---

## 5. Global States

### 5.1 Loading States

| Scope | Indicator | Duration | Behavior |
|-------|-----------|----------|----------|
| **Initial Load** | Full-page skeleton | — | Staggered reveal (KPIs → Charts → Tables) |
| **Refresh** | Top progress bar (2px `brand-primary`) | <30s | Non-blocking, current data visible |
| **Filter Change** | Component skeletons | <10s | Per-component, preserve layout |
| **Drill/Expand** | Inline spinner (16px) | <5s | Centered in container |
| **Export** | Modal progress (steps) | <60s | Cancelable, background download |

**Skeleton Patterns**:
- KPI: Gray blocks (label → value → trend)
- Chart: Gray chart area + axis placeholders
- Table: Row shimmer (neutral-100 → neutral-50)
- Slicer: Disabled inputs, loading text

### 5.2 Error States

| Scope | Display | Recovery |
|-------|---------|----------|
| **Global** | Toast (top-right) + Banner (below nav) | Retry button, auto-retry (30s) |
| **Component** | Inline error (replace content) | Refresh button, error details |
| **Network** | Offline banner (persistent) | Queue actions, sync on reconnect |
| **Auth** | Modal (session expired) | Re-login, preserve state |
| **Validation** | Inline (form fields) | Real-time, clear on fix |

**Error Toast**:
- Duration: 8s (dismissible)
- Actions: Retry, Dismiss, Details
- Max concurrent: 3 (queue excess)

### 5.3 Empty States

| Context | Illustration | Message | Action |
|---------|--------------|---------|--------|
| **No Data** | Chart outline icon | "No data for selected filters" | Clear filters button |
| **No Results** | Search icon | "No servers match 'web-01'" | Adjust search |
| **First Visit** | Dashboard icon | "Welcome! Connect a data source" | Setup CTA |
| **Error** | Alert triangle | "Unable to load data" | Retry / Support |

---

## 6. Animation & Motion

### 6.1 Timing Scale

| Duration | Use Case | Easing |
|----------|----------|--------|
| **50ms** | Micro-feedback (ripple, press) | ease-out |
| **100ms** | Tooltip show, hover lift | ease-out |
| **150ms** | Card hover, dropdown, tab switch | ease-out |
| **200ms** | Drawer expand, modal, row expand | ease-in-out |
| **250ms** | Panel slide, page transition | ease-in-out |
| **300ms** | Full page navigation | ease-in-out |
| **500ms** | KPI count-up, complex transitions | ease-out |

### 6.2 Motion Tokens

```css
:root {
  --duration-50: 50ms;
  --duration-100: 100ms;
  --duration-150: 150ms;
  --duration-200: 200ms;
  --duration-250: 250ms;
  --duration-300: 300ms;
  --duration-500: 500ms;
  
  --ease-out: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### 6.3 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  
  /* Keep essential feedback */
  .ripple { animation: none; }
  .skeleton { animation: none; background: var(--neutral-100); }
}
```

---

## 7. Keyboard Navigation Map

### Global Tab Order

```
1. Skip Link ("Skip to main content")
2. Nav Bar: Logo → Navigation Items → User Menu → Search → Refresh
3. Page Header: Title → Breadcrumb → Actions (Export, Share)
4. KPI Row: Card 1 → Card 2 → Card 3 → Card 4
5. Primary Charts: Chart 1 → Chart 2 → Chart 3 (each: Title → Toolbar → Data)
6. Detail Table: Toolbar → Headers → Rows (each cell) → Pagination
7. AI Insights: Card 1 → Card 2 → ...
8. Slicer Panel: Group 1 → Group 2 → ... (each: Label → Input → Options)
9. Footer: Status → Version → Links
```

### Roving Tabindex (Composite Widgets)

| Widget | Pattern | Keys |
|--------|---------|------|
| **Navigation Tabs** | `role="tablist"` | ←/→ navigate, Home/End, Enter/Space activate |
| **Chart Toolbar** | `role="toolbar"` | ←/→ navigate, Enter activate |
| **Table Header** | `role="rowheader"` | ←/→ navigate, Enter sort, Space multi-sort |
| **Slicer Options** | `role="listbox"` | ↑/↓ navigate, Space toggle, Home/End |
| **Context Menu** | `role="menu"` | ↑/↓ navigate, Enter activate, Escape close |
| **Pagination** | `role="navigation"` | ←/→ prev/next, number keys direct |

---

## 8. Touch & Mobile Adaptations

| Desktop Interaction | Mobile Adaptation |
|---------------------|-------------------|
| Hover tooltip | Tap to show, tap elsewhere to hide |
| Right-click menu | Long press (500ms) |
| Drag column reorder | Long press header → drag handle |
| Hover row highlight | Tap row → highlight + action bar |
| Multi-select (Ctrl+Click) | Checkbox column always visible |
| Slicer panel (side) | Bottom sheet (slide up) |
| Drill modal (center) | Full-screen modal |
| Keyboard shortcuts | Floating action button (FAB) → Command Palette |

### Touch Targets

| Element | Minimum Size | Spacing |
|---------|--------------|---------|
| Button | 44×44px | 8px |
| Checkbox/Radio | 24×24px | 12px |
| Tab | 44×44px | 4px |
| Menu Item | 44×44px | 0px |
| Chart Data Point | 16×16px (hit area) | — |

---

## 9. Accessibility Checklist

- [ ] All interactive elements reachable by keyboard
- [ ] Focus visible (2px `brand-primary` + 2px `neutral-0` ring)
- [ ] Focus order matches visual hierarchy
- [ ] ARIA labels on icon-only buttons
- [ ] Live regions for dynamic updates (toasts, loading)
- [ ] Color not sole indicator (icon + text + color)
- [ ] Contrast ≥4.5:1 text, ≥3:1 UI elements
- [ ] Touch targets ≥44×44px
- [ ] Reduced motion respected
- [ ] Screen reader tested (NVDA, JAWS, VoiceOver)
- [ ] Zoom 200% — no horizontal scroll, no content loss
- [ ] Language declared (`lang="en"`)
- [ ] Skip links present
- [ ] Landmarks: nav, main, aside, footer
- [ ] Heading hierarchy (h1→h2→h3→h4)

---

## 10. Performance Budgets

| Interaction | Target | Measurement |
|-------------|--------|-------------|
| **Click → Visual Feedback** | <50ms | Ripple, hover state |
| **Click → Tooltip** | <100ms | Tooltip render |
| **Click → Modal/Drawer** | <200ms | Animation start |
| **Filter → Data Update** | <300ms (debounce) + API | Skeleton shown immediately |
| **Page Navigation** | <500ms | First contentful paint |
| **Search → Results** | <150ms (debounce) | Debounced input |
| **Export Generate** | <30s | Progress indicator |

---

## 11. Implementation Notes

### Event Handling Pattern

```javascript
// Standard interaction handler
function handleInteraction(event, { 
  action,           // 'click' | 'keydown' | 'hover'
  target,           // Component reference
  analytics,        // Event data for telemetry
  accessibility     // ARIA updates needed
}) {
  // 1. Immediate visual feedback (<50ms)
  requestAnimationFrame(() => target.setState({ pressed: true }));
  
  // 2. Accessibility updates
  if (accessibility?.announce) {
    announceToScreenReader(accessibility.announce);
  }
  
  // 3. Business logic (async)
  const result = await executeAction(action, analytics);
  
  // 4. State update
  target.setState({ pressed: false, ...result });
  
  // 5. Telemetry
  telemetry.track('interaction', { action, ...analytics });
}
```

### Focus Management

```javascript
// Modal focus trap
function trapFocus(modal) {
  const focusable = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  
  first.focus();
  
  modal.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault(); last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); first.focus();
      }
    }
    if (e.key === 'Escape') closeModal(modal);
  });
}
```

---

## 12. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-07 | Initial specification |

---

*This specification defines the complete interaction model for SmartOps AI dashboards. All implementations must conform to these patterns for consistency across the platform.*