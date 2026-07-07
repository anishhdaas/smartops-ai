# SmartOps AI — Typography Specification

> **Design Language**: Microsoft Fluent 2 Type System  
> **Font Family**: `Segoe UI Variable` (primary), `Segoe UI` (fallback), system UI stack  
> **Scale**: Modular scale 1.25 (Major Third)  
> **Responsive**: Fluid clamping with `clamp()` for all sizes

---

## 1. Font Families

| Family | Stack | Usage |
|--------|-------|-------|
| `font-sans` | `"Segoe UI Variable", "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif` | All UI text, body, headings |
| `font-mono` | `"Cascadia Code", "Cascadia Mono", "SF Mono", "Fira Code", "Consolas", monospace` | Code, metrics, IDs, timestamps, JSON |
| `font-display` | `"Segoe UI Variable Display", "Segoe UI Variable", "Segoe UI", sans-serif` | Large headlines, hero numbers (KPI cards) |

**Font Feature Settings**:
```css
font-feature-settings: "cv02" 1, "cv03" 1, "cv04" 1, "cv11" 1, "ss01" 1;
/* cv02: Single-storey 'a', cv03: Single-storey 'g', cv04: Straight 'y', cv11: Slashed zero, ss01: Tabular figures */
```

---

## 2. Type Scale (Fluid)

> **Base**: 14px (0.875rem) at 320px viewport  
> **Max**: 16px (1rem) at 1920px viewport  
> **Ratio**: 1.25 (Major Third)  
> **Clamp**: `clamp(min, preferred, max)`

| Token | Mobile (320px) | Desktop (1920px) | Fluid CSS | Line Height | Weight | Usage |
|-------|----------------|------------------|-----------|-------------|--------|-------|
| `display-1` | 40px / 2.5rem | 56px / 3.5rem | `clamp(2.5rem, 5vw, 3.5rem)` | 1.1 | 700 | Hero KPI numbers, page titles |
| `display-2` | 32px / 2rem | 44px / 2.75rem | `clamp(2rem, 4vw, 2.75rem)` | 1.15 | 600 | Section titles, dashboard headers |
| `heading-1` | 28px / 1.75rem | 36px / 2.25rem | `clamp(1.75rem, 3vw, 2.25rem)` | 1.2 | 600 | Card titles, visual titles |
| `heading-2` | 24px / 1.5rem | 28px / 1.75rem | `clamp(1.5rem, 2.5vw, 1.75rem)` | 1.25 | 600 | Sub-section headers |
| `heading-3` | 20px / 1.25rem | 22px / 1.375rem | `clamp(1.25rem, 2vw, 1.375rem)` | 1.3 | 600 | Group labels, slicer headers |
| `heading-4` | 18px / 1.125rem | 18px / 1.125rem | `1.125rem` | 1.35 | 600 | Table headers, axis labels |
| `body-lg` | 16px / 1rem | 18px / 1.125rem | `clamp(1rem, 1.5vw, 1.125rem)` | 1.5 | 400 | Body text, tooltips, legends |
| `body` | 14px / 0.875rem | 16px / 1rem | `clamp(0.875rem, 1.25vw, 1rem)` | 1.5 | 400 | Default body, table cells |
| `body-sm` | 13px / 0.8125rem | 14px / 0.875rem | `clamp(0.8125rem, 1vw, 0.875rem)` | 1.5 | 400 | Secondary text, metadata |
| `caption` | 12px / 0.75rem | 12px / 0.75rem | `0.75rem` | 1.4 | 400 | Footnotes, timestamps, badges |
| `caption-sm` | 11px / 0.6875rem | 11px / 0.6875rem | `0.6875rem` | 1.4 | 400 | Dense tables, chart tick labels |
| `mono-lg` | 14px / 0.875rem | 16px / 1rem | `clamp(0.875rem, 1.25vw, 1rem)` | 1.5 | 400 | Code blocks, metric values |
| `mono` | 13px / 0.8125rem | 14px / 0.875rem | `clamp(0.8125rem, 1vw, 0.875rem)` | 1.5 | 400 | Inline code, IDs, JSON keys |
| `mono-sm` | 12px / 0.75rem | 12px / 0.75rem | `0.75rem` | 1.4 | 400 | Dense code, timestamps |

---

## 3. Weight Scale

| Token | Weight | Numeric | Usage |
|-------|--------|---------|-------|
| `weight-light` | Light | 300 | Reserved (large display only) |
| `weight-normal` | Regular | 400 | Body text, default |
| `weight-medium` | Medium | 500 | Emphasis, labels, button text |
| `weight-semibold` | SemiBold | 600 | Headings, KPI labels, important values |
| `weight-bold` | Bold | 700 | Display numbers, critical alerts |
| `weight-black` | Black | 800 | Reserved |

**Variable Font Axis** (Segoe UI Variable):
```css
font-variation-settings: "wght" 400, "wdth" 100, "opsz" 14;
/* wght: 300-700, wdth: 75-125, opsz: 8-72 */
```

---

## 4. Line Height System

| Token | Value | Usage |
|-------|-------|-------|
| `leading-none` | 1 | Icons, inline elements |
| `leading-tight` | 1.1 | Display headlines |
| `leading-snug` | 1.2 | Heading-1, Heading-2 |
| `leading-normal` | 1.3 | Heading-3, Heading-4 |
| `leading-relaxed` | 1.5 | Body text, paragraphs |
| `leading-loose` | 1.6 | Long-form content |

---

## 5. Letter Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `tracking-tighter` | -0.02em | Display-1, Display-2 |
| `tracking-tight` | -0.01em | Heading-1, Heading-2 |
| `tracking-normal` | 0 | Body, headings |
| `tracking-wide` | 0.01em | Captions, uppercase labels |
| `tracking-wider` | 0.05em | All-caps, button text, badges |
| `tracking-widest` | 0.1em | Tabular figures, mono |

---

## 6. Responsive Breakpoints

| Breakpoint | Min Width | Max Width | Base Font Size |
|------------|-----------|-----------|----------------|
| Mobile | 320px | 767px | 14px |
| Tablet | 768px | 1023px | 15px |
| Laptop | 1024px | 1439px | 15px |
| Desktop | 1440px | 1919px | 16px |
| Wide | 1920px | — | 16px |

---

## 7. Semantic Text Styles (Component Mapping)

| Component | Title | Value | Metadata | Units |
|-----------|-------|-------|----------|-------|
| **KPI Card** | `display-1` / `weight-bold` | `body-sm` / `weight-medium` | `caption` / `weight-normal` | `mono` |
| **Card Header** | `heading-3` / `weight-semibold` | — | — | — |
| **Visual Title** | `heading-4` / `weight-semibold` | — | — | — |
| **Axis Title** | `body-sm` / `weight-medium` | — | — | — |
| **Axis Labels** | `caption` / `weight-normal` | — | — | — |
| **Legend** | `body-sm` / `weight-normal` | — | — | — |
| **Tooltip** | `body` / `weight-normal` | `mono` / `weight-normal` | `caption` / `weight-normal` | — |
| **Table Header** | `heading-4` / `weight-semibold` | — | — | — |
| **Table Cell** | `body` / `weight-normal` | `mono` (numbers) | — | — |
| **Slicer Label** | `body-sm` / `weight-medium` | — | — | — |
| **Slicer Value** | `body` / `weight-normal` | — | — | — |
| **Navigation** | `body-sm` / `weight-medium` | — | — | — |
| **Breadcrumb** | `caption` / `weight-normal` | — | — | — |
| **Alert/Banner** | `body` / `weight-medium` | — | — | — |
| **Status Badge** | `caption` / `weight-semibold` | `tracking-wider` | — | — |

---

## 8. Number Formatting (Tabular Figures)

```css
.tabular-nums {
  font-variant-numeric: tabular-nums lining-nums;
  font-family: var(--font-mono);
}

/* Usage per-value formatting tokens */
--format-integer: "#,##0";
--format-decimal: "#,##0.0";
--format-percent: "0.0%";
--format-currency: "$#,##0";
--format-latency: "#,##0 ms";
--format-timestamp: "YYYY-MM-DD HH:mm:ss";
--format-date: "MMM DD, YYYY";
--format-time: "HH:mm:ss";
```

---

## 9. CSS Custom Properties

```css
:root {
  /* Font Families */
  --font-sans: "Segoe UI Variable", "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
  --font-mono: "Cascadia Code", "Cascadia Mono", "SF Mono", "Fira Code", "Consolas", monospace;
  --font-display: "Segoe UI Variable Display", "Segoe UI Variable", "Segoe UI", sans-serif;

  /* Weights */
  --weight-light: 300;
  --weight-normal: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;
  --weight-black: 800;

  /* Line Heights */
  --leading-none: 1;
  --leading-tight: 1.1;
  --leading-snug: 1.2;
  --leading-normal: 1.3;
  --leading-relaxed: 1.5;
  --leading-loose: 1.6;

  /* Letter Spacing */
  --tracking-tighter: -0.02em;
  --tracking-tight: -0.01em;
  --tracking-normal: 0;
  --tracking-wide: 0.01em;
  --tracking-wider: 0.05em;
  --tracking-widest: 0.1em;

  /* Fluid Type Scale */
  --text-display-1: clamp(2.5rem, 5vw, 3.5rem);
  --text-display-1-line: 1.1;
  --text-display-2: clamp(2rem, 4vw, 2.75rem);
  --text-display-2-line: 1.15;
  --text-heading-1: clamp(1.75rem, 3vw, 2.25rem);
  --text-heading-1-line: 1.2;
  --text-heading-2: clamp(1.5rem, 2.5vw, 1.75rem);
  --text-heading-2-line: 1.25;
  --text-heading-3: clamp(1.25rem, 2vw, 1.375rem);
  --text-heading-3-line: 1.3;
  --text-heading-4: 1.125rem;
  --text-heading-4-line: 1.35;
  --text-body-lg: clamp(1rem, 1.5vw, 1.125rem);
  --text-body-lg-line: 1.5;
  --text-body: clamp(0.875rem, 1.25vw, 1rem);
  --text-body-line: 1.5;
  --text-body-sm: clamp(0.8125rem, 1vw, 0.875rem);
  --text-body-sm-line: 1.5;
  --text-caption: 0.75rem;
  --text-caption-line: 1.4;
  --text-caption-sm: 0.6875rem;
  --text-caption-sm-line: 1.4;

  /* Mono Scale */
  --text-mono-lg: clamp(0.875rem, 1.25vw, 1rem);
  --text-mono: clamp(0.8125rem, 1vw, 0.875rem);
  --text-mono-sm: 0.75rem;
}
```

---

## 10. Power BI Text Formatting Reference

| Visual | Title Font | Label Font | Value Font | Detail Font |
|--------|------------|------------|------------|-------------|
| Card | Segoe UI Variable, 14pt, SemiBold | Segoe UI Variable, 11pt, Regular | Segoe UI Variable Display, 32pt, Bold | Segoe UI Variable, 10pt, Regular |
| KPI | Segoe UI Variable, 12pt, SemiBold | Segoe UI Variable, 10pt, Regular | Segoe UI Variable Display, 28pt, Bold | Segoe UI Variable, 10pt, Regular |
| Table | Segoe UI Variable, 11pt, SemiBold | Segoe UI Variable, 10pt, Regular | Segoe UI Variable, 10pt, Regular | — |
| Matrix | Segoe UI Variable, 11pt, SemiBold | Segoe UI Variable, 10pt, Regular | Segoe UI Variable, 10pt, Regular | — |
| Line/Area/Bar Chart | Segoe UI Variable, 12pt, SemiBold | Segoe UI Variable, 10pt, Regular | Segoe UI Variable, 10pt, Regular | Segoe UI Variable, 9pt, Regular |
| Gauge | Segoe UI Variable, 12pt, SemiBold | Segoe UI Variable, 10pt, Regular | Segoe UI Variable Display, 24pt, Bold | — |
| Donut/Pie | Segoe UI Variable, 12pt, SemiBold | Segoe UI Variable, 10pt, Regular | Segoe UI Variable, 10pt, Regular | — |
| Scatter | Segoe UI Variable, 12pt, SemiBold | Segoe UI Variable, 10pt, Regular | Segoe UI Variable, 10pt, Regular | — |
| Slicer | Segoe UI Variable, 11pt, Medium | Segoe UI Variable, 10pt, Regular | — | — |

---

## 11. Accessibility

- **Minimum font size**: 12px (0.75rem) for all readable text
- **Contrast**: All text meets WCAG 2.1 AA (4.5:1) against background
- **Resize**: Text supports 200% zoom without loss of function
- **Line height**: Minimum 1.5 for body text (1.4 for captions)
- **Letter spacing**: No negative tracking on body text
- **Font loading**: `font-display: swap` for web fonts; system fallback immediate

---

## 12. Dark Theme Adjustments

```css
[data-theme="dark"] {
  /* Increase weight slightly for better readability on dark */
  --weight-normal: 400;      /* stays */
  --weight-medium: 500;      /* stays */
  --weight-semibold: 600;    /* stays */
  
  /* Slightly larger line height for dark mode */
  --text-body-line: 1.55;
  --text-body-sm-line: 1.55;
  
  /* Reduce contrast slightly for comfort */
  /* Text color uses neutral-900 (#F3F2F1) not neutral-1000 (#FFFFFF) */
}
```

---

## 13. Usage Rules

1. **Never** hardcode pixel values — use semantic tokens
2. **Headings** always use `weight-semibold` (600) minimum
3. **Numbers** in data contexts always use `font-mono` + `tabular-nums`
4. **KPI values** use `font-display` + `weight-bold` + `tabular-nums`
5. **All caps** only for badges, buttons, slicer headers — max 12 chars
6. **Truncation**: Use CSS `text-overflow: ellipsis` with `max-width`, not fixed width
7. **RTL ready**: Logical properties (`margin-inline-start`, `padding-inline-end`)
8. **Print**: Serif fallback for body (`Georgia, serif`) at 12pt