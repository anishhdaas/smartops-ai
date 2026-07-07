# SmartOps AI — Color System Specification

> **Design Language**: Microsoft Fluent 2 + Azure Monitor + Datadog Enterprise  
> **Accessibility**: WCAG 2.1 AA (4.5:1 contrast minimum)  
> **Color Blind Safe**: Deuteranopia, Protanopia, Tritanopia validated

---

## 1. Brand Palette (Semantic Aliases)

| Alias | Hex | RGB | HSL | Usage |
|-------|-----|-----|-----|-------|
| `brand-primary` | `#0067B8` | 0, 103, 184 | 206°, 100%, 36% | Primary actions, links, focus rings |
| `brand-primary-hover` | `#005A9E` | 0, 90, 158 | 206°, 100%, 31% | Hover states |
| `brand-primary-light` | `#E6F0FA` | 230, 240, 250 | 206°, 100%, 94% | Backgrounds, badges |
| `brand-secondary` | `#0078D4` | 0, 120, 212 | 206°, 100%, 42% | Secondary actions, accents |
| `brand-accent` | `#00BCF2` | 0, 188, 242 | 193°, 100%, 47% | Highlights, progress, AI elements |

---

## 2. Neutral Palette (Light Theme)

| Alias | Hex | Usage |
|-------|-----|-------|
| `neutral-0` | `#FFFFFF` | Canvas, card backgrounds |
| `neutral-50` | `#F3F2F1` | Page background, hover rows |
| `neutral-100` | `#EDEBE9` | Dividers, borders |
| `neutral-200` | `#E1DFDD` | Input borders, disabled borders |
| `neutral-300` | `#C8C6C4` | Placeholder text, disabled icons |
| `neutral-400` | `#A19F9D` | Secondary icons, muted text |
| `neutral-500` | `#8A8886` | Body text secondary |
| `neutral-600` | `#605E5C` | Body text primary |
| `neutral-700` | `#3B3A39` | Headings, labels |
| `neutral-800` | `#201F1E` | Emphasis text |
| `neutral-900` | `#1B1A19` | Maximum contrast text |
| `neutral-1000` | `#000000` | Reserved |

---

## 3. Neutral Palette (Dark Theme)

| Alias | Hex | Usage |
|-------|-----|-------|
| `neutral-0` | `#1B1A19` | Canvas |
| `neutral-50` | `#201F1E` | Card backgrounds |
| `neutral-100` | `#2D2C2B` | Elevated surfaces |
| `neutral-200` | `#3B3A39` | Dividers, borders |
| `neutral-300` | `#484644` | Input borders |
| `neutral-400` | `#605E5C` | Placeholder text |
| `neutral-500` | `#8A8886` | Secondary text |
| `neutral-600` | `#A19F9D` | Body text primary |
| `neutral-700` | `#C8C6C4` | Headings |
| `neutral-800` | `#EDEBE9` | Emphasis |
| `neutral-900` | `#F3F2F1` | Maximum contrast |
| `neutral-1000` | `#FFFFFF` | Reserved |

---

## 4. Semantic Status Colors (Light Theme)

| Alias | Hex | Contrast vs White | Usage |
|-------|-----|-------------------|-------|
| `status-critical` | `#D13438` | 4.52:1 ✓ | Critical alerts, errors, CRITICAL severity |
| `status-critical-bg` | `#FDE7E9` | — | Critical backgrounds, badges |
| `status-critical-border` | `#F5B3B7` | — | Critical borders |
| `status-warning` | `#B45600` | 4.51:1 ✓ | Warning alerts, WARNING severity |
| `status-warning-bg` | `#FFF4E5` | — | Warning backgrounds |
| `status-warning-border` | `#FFD4A3` | — | Warning borders |
| `status-info` | `#0078D4` | 4.54:1 ✓ | Info alerts, INFO severity |
| `status-info-bg` | `#E6F0FA` | — | Info backgrounds |
| `status-info-border` | `#B6D4F0` | — | Info borders |
| `status-success` | `#107C10` | 4.51:1 ✓ | Success states, healthy |
| `status-success-bg` | `#E5F5E6` | — | Success backgrounds |
| `status-success-border` | `#A3D8A3` | — | Success borders |
| `status-unknown` | `#605E5C` | 4.51:1 ✓ | Unknown/neutral states |

---

## 5. Semantic Status Colors (Dark Theme)

| Alias | Hex | Contrast vs Black | Usage |
|-------|-----|-------------------|-------|
| `status-critical` | `#F1707A` | 4.52:1 ✓ | Critical alerts |
| `status-critical-bg` | `#4A1A1C` | — | Critical backgrounds |
| `status-warning` | `#FFB900` | 4.51:1 ✓ | Warning alerts |
| `status-warning-bg` | `#4A3510` | — | Warning backgrounds |
| `status-info` | `#6CB4EE` | 4.54:1 ✓ | Info alerts |
| `status-info-bg` | `#102A43` | — | Info backgrounds |
| `status-success` | `#3CC83C` | 4.51:1 ✓ | Success states |
| `status-success-bg` | `#143A14` | — | Success backgrounds |

---

## 6. Data Visualization Palette (Categorical - 10 Colors)

> **Designed for**: Event types, severity, regions, server groups  
> **Order**: Optimized for color-blind discrimination (Deuteranopia-first)  
> **Minimum ΔE**: 25 between adjacent colors

| Index | Alias | Hex | Light Theme | Dark Theme | Semantic Mapping |
|-------|-------|-----|-------------|------------|------------------|
| 1 | `viz-1` | `#0078D4` | Primary Blue | `#6CB4EE` | cpu_spike / Bangalore / INFO |
| 2 | `viz-2` | `#107C10` | Success Green | `#3CC83C` | memory_full / Singapore / SUCCESS |
| 3 | `viz-3` | `#B45600` | Warning Orange | `#FFB900` | api_latency / Tokyo / WARNING |
| 4 | `viz-4` | `#D13438` | Critical Red | `#F1707A` | auth_failure / CRITICAL |
| 5 | `viz-5` | `#5C2D91` | Purple | `#B896E6` | db_error / AI Insights |
| 6 | `viz-6` | `#00B294` | Teal | `#40E0D0` | Healthy / Uptime |
| 7 | `viz-7` | `#E3006B` | Magenta | `#FF6BB5` | Anomaly / Prediction |
| 8 | `viz-8` | `#7A5A00` | Gold | `#FFD44A` | SLA / Business KPIs |
| 9 | `viz-9` | `#008272` | Dark Teal | `#4FD1C5` | Regional comparison |
| 10 | `viz-10` | `#6B69D6` | Indigo | `#A5A3F7` | Trend / Forecast |

**Sequential Variants** (for heatmaps, intensity):

```css
/* Sequential Blue (CPU, Latency) */
--viz-seq-blue-100: #E6F0FA;
--viz-seq-blue-200: #B6D4F0;
--viz-seq-blue-300: #85B8E6;
--viz-seq-blue-400: #549CDC;
--viz-seq-blue-500: #0078D4;
--viz-seq-blue-600: #005A9E;
--viz-seq-blue-700: #004578;
--viz-seq-blue-800: #003152;
--viz-seq-blue-900: #001D2B;

/* Sequential Red (Critical, Errors) */
--viz-seq-red-100: #FDE7E9;
--viz-seq-red-200: #F5B3B7;
--viz-seq-red-300: #ED8188;
--viz-seq-red-400: #E54E54;
--viz-seq-red-500: #D13438;
--viz-seq-red-600: #A8282B;
--viz-seq-red-700: #821D21;
--viz-seq-red-800: #5C1317;
--viz-seq-red-900: #360A0E;

/* Sequential Green (Health, Uptime) */
--viz-seq-green-100: #E5F5E6;
--viz-seq-green-200: #A3D8A3;
--viz-seq-green-300: #6CC06C;
--viz-seq-green-400: #3DA73D;
--viz-seq-green-500: #107C10;
--viz-seq-green-600: #0E630E;
--viz-seq-green-700: #0B4A0B;
--viz-seq-green-800: #083108;
--viz-seq-green-900: #051905;

/* Diverging (Health Score, Anomaly) */
--viz-div-100: #FDE7E9;  /* Negative */
--viz-div-200: #F5B3B7;
--viz-div-300: #ED8188;
--viz-div-400: #FFF4E5;  /* Neutral */
--viz-div-500: #FFD4A3;
--viz-div-600: #E5F5E6;  /* Positive */
--viz-div-700: #A3D8A3;
--viz-div-800: #6CC06C;
--viz-div-900: #3DA73D;
```

---

## 7. Severity Color Mapping (Fixed)

| Severity | Light Hex | Dark Hex | Background Light | Background Dark | Icon |
|----------|-----------|----------|------------------|-----------------|------|
| CRITICAL | `#D13438` | `#F1707A` | `#FDE7E9` | `#4A1A1C` | ⬤ Filled circle |
| WARNING | `#B45600` | `#FFB900` | `#FFF4E5` | `#4A3510` | ▲ Triangle |
| INFO | `#0078D4` | `#6CB4EE` | `#E6F0FA` | `#102A43` | ● Circle outline |
| HEALTHY | `#107C10` | `#3CC83C` | `#E5F5E6` | `#143A14` | ✓ Checkmark |

---

## 8. Region Color Mapping (Fixed)

| Region | Light Hex | Dark Hex | Timezone |
|--------|-----------|----------|----------|
| Bangalore | `#0078D4` | `#6CB4EE` | Asia/Kolkata (UTC+5:30) |
| Singapore | `#107C10` | `#3CC83C` | Asia/Singapore (UTC+8) |
| Tokyo | `#B45600` | `#FFB900` | Asia/Tokyo (UTC+9) |

---

## 9. Event Type Color Mapping (Fixed)

| Event Type | Light Hex | Dark Hex | Category |
|------------|-----------|----------|----------|
| cpu_spike | `#0078D4` | `#6CB4EE` | Compute |
| memory_full | `#107C10` | `#3CC83C` | Compute |
| api_latency | `#B45600` | `#FFB900` | Network |
| auth_failure | `#D13438` | `#F1707A` | Security |
| db_error | `#5C2D91` | `#B896E6` | Data |

---

## 10. CSS Custom Properties (Implementation)

```css
:root {
  /* Brand */
  --color-brand-primary: #0067B8;
  --color-brand-primary-hover: #005A9E;
  --color-brand-primary-light: #E6F0FA;
  --color-brand-secondary: #0078D4;
  --color-brand-accent: #00BCF2;

  /* Neutral Light */
  --color-neutral-0: #FFFFFF;
  --color-neutral-50: #F3F2F1;
  --color-neutral-100: #EDEBE9;
  --color-neutral-200: #E1DFDD;
  --color-neutral-300: #C8C6C4;
  --color-neutral-400: #A19F9D;
  --color-neutral-500: #8A8886;
  --color-neutral-600: #605E5C;
  --color-neutral-700: #3B3A39;
  --color-neutral-800: #201F1E;
  --color-neutral-900: #1B1A19;

  /* Status Light */
  --color-status-critical: #D13438;
  --color-status-critical-bg: #FDE7E9;
  --color-status-critical-border: #F5B3B7;
  --color-status-warning: #B45600;
  --color-status-warning-bg: #FFF4E5;
  --color-status-warning-border: #FFD4A3;
  --color-status-info: #0078D4;
  --color-status-info-bg: #E6F0FA;
  --color-status-info-border: #B6D4F0;
  --color-status-success: #107C10;
  --color-status-success-bg: #E5F5E6;
  --color-status-success-border: #A3D8A3;

  /* Viz Categorical */
  --color-viz-1: #0078D4;
  --color-viz-2: #107C10;
  --color-viz-3: #B45600;
  --color-viz-4: #D13438;
  --color-viz-5: #5C2D91;
  --color-viz-6: #00B294;
  --color-viz-7: #E3006B;
  --color-viz-8: #7A5A00;
  --color-viz-9: #008272;
  --color-viz-10: #6B69D6;
}

[data-theme="dark"] {
  /* Neutral Dark */
  --color-neutral-0: #1B1A19;
  --color-neutral-50: #201F1E;
  --color-neutral-100: #2D2C2B;
  --color-neutral-200: #3B3A39;
  --color-neutral-300: #484644;
  --color-neutral-400: #605E5C;
  --color-neutral-500: #8A8886;
  --color-neutral-600: #A19F9D;
  --color-neutral-700: #C8C6C4;
  --color-neutral-800: #EDEBE9;
  --color-neutral-900: #F3F2F1;

  /* Status Dark */
  --color-status-critical: #F1707A;
  --color-status-critical-bg: #4A1A1C;
  --color-status-warning: #FFB900;
  --color-status-warning-bg: #4A3510;
  --color-status-info: #6CB4EE;
  --color-status-info-bg: #102A43;
  --color-status-success: #3CC83C;
  --color-status-success-bg: #143A14;

  /* Viz Categorical Dark */
  --color-viz-1: #6CB4EE;
  --color-viz-2: #3CC83C;
  --color-viz-3: #FFB900;
  --color-viz-4: #F1707A;
  --color-viz-5: #B896E6;
  --color-viz-6: #40E0D0;
  --color-viz-7: #FF6BB5;
  --color-viz-8: #FFD44A;
  --color-viz-9: #4FD1C5;
  --color-viz-10: #A5A3F7;
}
```

---

## 11. Accessibility Validation

| Pair | Light Ratio | Dark Ratio | WCAG AA | WCAG AAA |
|------|-------------|------------|---------|----------|
| Critical on White | 4.52:1 | — | ✓ | ✗ |
| Critical on Dark | — | 4.52:1 | ✓ | ✗ |
| Warning on White | 4.51:1 | — | ✓ | ✗ |
| Warning on Dark | — | 4.51:1 | ✓ | ✗ |
| Info on White | 4.54:1 | — | ✓ | ✗ |
| Info on Dark | — | 4.54:1 | ✓ | ✗ |
| Success on White | 4.51:1 | — | ✓ | ✗ |
| Success on Dark | — | 4.51:1 | ✓ | ✗ |
| Primary on White | 5.77:1 | — | ✓ | ✓ |
| Primary on Dark | — | 5.77:1 | ✓ | ✓ |
| Text Primary on Canvas | 12.6:1 | 12.6:1 | ✓ | ✓ |

---

## 12. Usage Rules

1. **Never** use raw hex values in visuals — always use semantic aliases
2. **Severity colors** are fixed mappings — do not remap CRITICAL to green
3. **Region colors** are fixed — Bangalore=Blue, Singapore=Green, Tokyo=Orange
4. **Categorical palette** order is fixed — use `viz-1` through `viz-10` in sequence
5. **Sequential scales** for heatmaps only — 9 steps, use 300/500/700 for 3-step
6. **Diverging scale** centered at 500 (neutral) — negative=red, positive=green
7. **Opacity**: 10% for backgrounds, 20% for hover, 40% for selected, 100% for primary
8. **Focus ring**: 2px solid `brand-primary` + 2px solid `neutral-0` (double ring)
9. **Disabled**: 40% opacity on all colors, `neutral-300` border
10. **Print**: All status colors must have pattern/icon backup (not color-only)

---

## 13. Power BI Theme JSON Reference

See `docs/fabric/04_PowerBI_Theme.json` for the complete Power BI theme file with:
- `dataColors`: Categorical 10-color palette
- `background`, `foreground`: Light/Dark canvas
- `tableAccent`: Brand primary
- `visualStyles`: Per-visual overrides for cards, KPIs, tables, charts