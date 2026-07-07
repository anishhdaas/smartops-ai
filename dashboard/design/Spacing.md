# SmartOps AI — Spacing & Layout Specification

> **Design Language**: Microsoft Fluent 2 Spacing System  
> **Base Unit**: 4px (0.25rem)  
> **Grid**: 12-column responsive grid (CSS Grid + Flexbox)  
> **Scale**: Exponential (4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 72, 80, 96)

---

## 1. Spacing Scale (Base-4)

| Token | Value | Rem | Px | Usage |
|-------|-------|-----|-----|-------|
| `space-0` | 0 | 0 | 0 | Reset, tight stacking |
| `space-1` | 1 | 0.25rem | 4px | Micro gaps, icon-text |
| `space-2` | 2 | 0.5rem | 8px | Default gap, inline spacing |
| `space-3` | 3 | 0.75rem | 12px | Component internal padding |
| `space-4` | 4 | 1rem | 16px | **Base unit** — card padding, section gap |
| `space-5` | 5 | 1.25rem | 20px | Form field gaps, list items |
| `space-6` | 6 | 1.5rem | 24px | Section spacing, card margins |
| `space-7` | 7 | 1.75rem | 28px | Large component gaps |
| `space-8` | 8 | 2rem | 32px | Page section breaks |
| `space-9` | 9 | 2.25rem | 36px | Major section breaks |
| `space-10` | 10 | 2.5rem | 40px | Page margins (desktop) |
| `space-11` | 11 | 2.75rem | 44px | Hero sections |
| `space-12` | 12 | 3rem | 48px | Full-page sections |
| `space-14` | 14 | 3.5rem | 56px | Extra large |
| `space-16` | 16 | 4rem | 64px | Maximum |
| `space-20` | 20 | 5rem | 80px | Reserved |
| `space-24` | 24 | 6rem | 96px | Reserved |

---

## 2. Responsive Spacing (Fluid)

> **Mobile-first**: Values scale up at breakpoints  
> **Clamp**: `clamp(mobile, preferred, desktop)`

| Token | Mobile (≤767px) | Tablet (768-1023px) | Desktop (≥1024px) | Fluid CSS |
|-------|-----------------|---------------------|-------------------|-----------|
| `space-section` | `space-6` (24px) | `space-8` (32px) | `space-10` (40px) | `clamp(1.5rem, 3vw, 2.5rem)` |
| `space-component` | `space-4` (16px) | `space-5` (20px) | `space-6` (24px) | `clamp(1rem, 1.5vw, 1.5rem)` |
| `space-card` | `space-3` (12px) | `space-4` (16px) | `space-4` (16px) | `clamp(0.75rem, 1vw, 1rem)` |
| `space-inline` | `space-2` (8px) | `space-2` (8px) | `space-3` (12px) | `clamp(0.5rem, 0.75vw, 0.75rem)` |
| `space-micro` | `space-1` (4px) | `space-1` (4px) | `space-1` (4px) | `0.25rem` |
| `space-page-x` | `space-4` (16px) | `space-6` (24px) | `space-8` (32px) | `clamp(1rem, 2vw, 2rem)` |
| `space-page-y` | `space-6` (24px) | `space-8` (32px) | `space-10` (40px) | `clamp(1.5rem, 3vw, 2.5rem)` |

---

## 3. Layout Grid (12-Column)

### Container Widths

| Breakpoint | Container Max | Columns | Gutter | Margin |
|------------|---------------|---------|--------|--------|
| Mobile (≤767px) | 100% | 4 | `space-3` (12px) | `space-4` (16px) |
| Tablet (768-1023px) | 720px | 8 | `space-4` (16px) | `space-6` (24px) |
| Laptop (1024-1439px) | 960px | 12 | `space-5` (20px) | `space-6` (24px) |
| Desktop (1440-1919px) | 1200px | 12 | `space-6` (24px) | `space-8` (32px) |
| Wide (≥1920px) | 1440px | 12 | `space-8` (32px) | `space-10` (40px) |

### Grid CSS

```css
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--grid-gutter);
  padding-inline: var(--grid-margin);
  max-width: var(--container-max);
  margin-inline: auto;
}

@media (max-width: 767px) {
  .grid { grid-template-columns: repeat(4, 1fr); }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .grid { grid-template-columns: repeat(8, 1fr); }
}

@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(12, 1fr); }
}

/* Column span utilities */
.col-1  { grid-column: span 1; }
.col-2  { grid-column: span 2; }
.col-3  { grid-column: span 3; }
.col-4  { grid-column: span 4; }
.col-5  { grid-column: span 5; }
.col-6  { grid-column: span 6; }
.col-7  { grid-column: span 7; }
.col-8  { grid-column: span 8; }
.col-9  { grid-column: span 9; }
.col-10 { grid-column: span 10; }
.col-11 { grid-column: span 11; }
.col-12 { grid-column: span 12; }

/* Responsive spans */
@media (max-width: 767px) {
  .col-mobile-12 { grid-column: span 4; }
  .col-mobile-6  { grid-column: span 2; }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .col-tablet-12 { grid-column: span 8; }
  .col-tablet-6  { grid-column: span 4; }
}
```

---

## 4. Component Spacing Patterns

### Card

```css
.card {
  padding: var(--space-card);           /* 12px/16px */
  gap: var(--space-component);          /* 16px/24px */
  border-radius: var(--radius-lg);      /* 12px */
}

.card-header {
  padding-bottom: var(--space-3);       /* 12px */
  border-bottom: 1px solid var(--neutral-100);
  margin-bottom: var(--space-3);        /* 12px */
}

.card-body {
  gap: var(--space-2);                  /* 8px */
}

.card-footer {
  padding-top: var(--space-3);          /* 12px */
  border-top: 1px solid var(--neutral-100);
  margin-top: var(--space-3);           /* 12px */
}
```

### KPI Card (Executive Dashboard)

```css
.kpi-card {
  padding: var(--space-6);              /* 24px/32px */
  gap: var(--space-4);                  /* 16px/20px */
  min-height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.kpi-value {
  line-height: var(--leading-tight);    /* 1.1 */
  margin: 0;
}

.kpi-label {
  margin-top: var(--space-1);           /* 4px */
}

.kpi-trend {
  margin-top: var(--space-2);           /* 8px */
  gap: var(--space-1);                  /* 4px */
}
```

### Section / Page

```css
.page {
  padding-block: var(--space-page-y);   /* 24px/40px */
  padding-inline: var(--space-page-x);  /* 16px/32px */
}

.section {
  margin-block: var(--space-section);   /* 24px/40px */
}

.section-header {
  margin-bottom: var(--space-component); /* 16px/24px */
}

.section-title {
  margin-bottom: var(--space-1);        /* 4px */
}

.section-subtitle {
  margin-top: 0;
}
```

### Form

```css
.form-group {
  margin-bottom: var(--space-5);        /* 20px */
  gap: var(--space-2);                  /* 8px */
}

.form-label {
  margin-bottom: var(--space-1);        /* 4px */
}

.form-input {
  padding: var(--space-3) var(--space-4); /* 12px 16px */
  gap: var(--space-2);                  /* 8px */
}

.form-error {
  margin-top: var(--space-1);           /* 4px */
}

.form-help {
  margin-top: var(--space-1);           /* 4px */
}
```

### Table

```css
.table {
  border-collapse: collapse;
  width: 100%;
}

.table th,
.table td {
  padding: var(--space-3) var(--space-4); /* 12px 16px */
  text-align: start;
}

.table th {
  border-bottom: 2px solid var(--neutral-200);
  padding-bottom: var(--space-3);       /* 12px */
}

.table td {
  border-bottom: 1px solid var(--neutral-100);
}

.table tbody tr:hover td {
  background: var(--neutral-50);
}

.table--compact th,
.table--compact td {
  padding: var(--space-2) var(--space-3); /* 8px 12px */
}
```

### List / Menu

```css
.list {
  gap: var(--space-2);                  /* 8px */
}

.list-item {
  padding: var(--space-2) var(--space-3); /* 8px 12px */
  gap: var(--space-3);                  /* 12px */
}

.list-item--dense {
  padding: var(--space-1) var(--space-2); /* 4px 8px */
}

.menu {
  padding: var(--space-2);              /* 8px */
  gap: var(--space-1);                  /* 4px */
}

.menu-item {
  padding: var(--space-2) var(--space-3); /* 8px 12px */
  gap: var(--space-2);                  /* 8px */
}
```

### Slicer / Filter Panel

```css
.slicer-panel {
  width: 300px;                         /* Fixed desktop */
  padding: var(--space-4);              /* 16px */
  gap: var(--space-5);                  /* 20px */
}

.slicer-group {
  gap: var(--space-2);                  /* 8px */
}

.slicer-label {
  margin-bottom: var(--space-1);        /* 4px */
}

.slicer-options {
  gap: var(--space-1);                  /* 4px */
  max-height: 200px;
  overflow-y: auto;
}

.slicer-option {
  padding: var(--space-2) var(--space-3); /* 8px 12px */
  gap: var(--space-2);                  /* 8px */
}
```

### Tooltip

```css
.tooltip {
  padding: var(--space-3) var(--space-4); /* 12px 16px */
  gap: var(--space-2);                  /* 8px */
  max-width: 320px;
}

.tooltip-row {
  gap: var(--space-3);                  /* 12px */
  align-items: baseline;
}

.tooltip-label {
  flex: 0 0 120px;
}

.tooltip-value {
  flex: 1;
  text-align: end;
  font-family: var(--font-mono);
}
```

### Modal / Dialog

```css
.modal-overlay {
  padding: var(--space-6);              /* 24px/32px */
}

.modal {
  max-width: 560px;
  padding: var(--space-6);              /* 24px/32px */
  gap: var(--space-5);                  /* 20px */
  border-radius: var(--radius-xl);      /* 16px */
}

.modal-header {
  padding-bottom: var(--space-4);       /* 16px */
  border-bottom: 1px solid var(--neutral-100);
  margin-bottom: var(--space-4);        /* 16px */
}

.modal-body {
  gap: var(--space-4);                  /* 16px/20px */
}

.modal-footer {
  padding-top: var(--space-4);          /* 16px */
  border-top: 1px solid var(--neutral-100);
  margin-top: var(--space-4);           /* 16px */
  justify-content: flex-end;
  gap: var(--space-3);                  /* 12px */
}
```

### Navigation Bar

```css
.nav-bar {
  height: 56px;
  padding-inline: var(--space-6);       /* 24px/32px */
  gap: var(--space-6);                  /* 24px */
  border-bottom: 1px solid var(--neutral-100);
}

.nav-brand {
  gap: var(--space-3);                  /* 12px */
}

.nav-items {
  gap: var(--space-1);                  /* 4px */
}

.nav-item {
  padding: var(--space-2) var(--space-4); /* 8px 16px */
  gap: var(--space-2);                  /* 8px */
  border-radius: var(--radius-md);      /* 8px */
}

.nav-item--active {
  background: var(--brand-primary-light);
  color: var(--brand-primary);
}
```

---

## 5. Border Radius Scale

| Token | Value | Usage |
|-------|-------|-------|
| `radius-none` | 0 | Sharp corners, tables |
| `radius-sm` | 4px | Badges, tags, chips |
| `radius-md` | 8px | Buttons, inputs, cards (mobile) |
| `radius-lg` | 12px | Cards (desktop), modals, dropdowns |
| `radius-xl` | 16px | Modals, drawers, large containers |
| `radius-full` | 9999px | Pills, avatars, progress rings |
| `radius-card` | `clamp(8px, 1vw, 12px)` | Responsive card radius |

---

## 6. Shadow / Elevation Scale

| Token | Value | Usage |
|-------|-------|-------|
| `elevation-0` | none | Flat, inline |
| `elevation-1` | `0 1px 2px rgba(0,0,0,0.05)` | Cards (rest), table rows |
| `elevation-2` | `0 2px 4px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)` | Cards (hover), dropdowns |
| `elevation-3` | `0 4px 8px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.05)` | Modals, drawers, tooltips |
| `elevation-4` | `0 8px 16px rgba(0,0,0,0.1), 0 4px 8px rgba(0,0,0,0.06)` | Dialogs, popovers |
| `elevation-5` | `0 16px 32px rgba(0,0,0,0.12), 0 8px 16px rgba(0,0,0,0.08)` | Full-screen overlays |

**Dark Theme Shadows** (use colored shadows):
```css
[data-theme="dark"] {
  --elevation-1: 0 1px 2px rgba(0,0,0,0.3);
  --elevation-2: 0 2px 4px rgba(0,0,0,0.35), 0 1px 2px rgba(0,0,0,0.25);
  --elevation-3: 0 4px 8px rgba(0,0,0,0.4), 0 2px 4px rgba(0,0,0,0.3);
  --elevation-4: 0 8px 16px rgba(0,0,0,0.45), 0 4px 8px rgba(0,0,0,0.35);
  --elevation-5: 0 16px 32px rgba(0,0,0,0.5), 0 8px 16px rgba(0,0,0,0.4);
}
```

---

## 7. Z-Index Scale

| Token | Value | Usage |
|-------|-------|-------|
| `z-base` | 0 | Page content |
| `z-raised` | 10 | Cards, dropdowns (hover) |
| `z-sticky` | 100 | Sticky headers, nav bars |
| `z-overlay` | 200 | Tooltips, popovers |
| `z-modal` | 500 | Modals, dialogs, drawers |
| `z-toast` | 1000 | Toasts, notifications |
| `z-tooltip` | 1100 | Tooltips (above toasts) |

---

## 8. CSS Custom Properties

```css
:root {
  /* Base Spacing */
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-7: 1.75rem;   /* 28px */
  --space-8: 2rem;      /* 32px */
  --space-9: 2.25rem;   /* 36px */
  --space-10: 2.5rem;   /* 40px */
  --space-11: 2.75rem;  /* 44px */
  --space-12: 3rem;     /* 48px */
  --space-14: 3.5rem;   /* 56px */
  --space-16: 4rem;     /* 64px */

  /* Responsive Spacing */
  --space-micro: var(--space-1);
  --space-inline: clamp(0.5rem, 0.75vw, 0.75rem);
  --space-card: clamp(0.75rem, 1vw, 1rem);
  --space-component: clamp(1rem, 1.5vw, 1.5rem);
  --space-section: clamp(1.5rem, 3vw, 2.5rem);
  --space-page-x: clamp(1rem, 2vw, 2rem);
  --space-page-y: clamp(1.5rem, 3vw, 2.5rem);

  /* Grid */
  --grid-gutter-mobile: var(--space-3);
  --grid-gutter-tablet: var(--space-4);
  --grid-gutter-desktop: var(--space-6);
  --grid-gutter-wide: var(--space-8);
  --grid-margin-mobile: var(--space-4);
  --grid-margin-tablet: var(--space-6);
  --grid-margin-desktop: var(--space-6);
  --grid-margin-wide: var(--space-10);
  --container-max-mobile: 100%;
  --container-max-tablet: 720px;
  --container-max-laptop: 960px;
  --container-max-desktop: 1200px;
  --container-max-wide: 1440px;

  /* Border Radius */
  --radius-none: 0;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
  --radius-card: clamp(8px, 1vw, 12px);

  /* Shadows */
  --elevation-0: none;
  --elevation-1: 0 1px 2px rgba(0,0,0,0.05);
  --elevation-2: 0 2px 4px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --elevation-3: 0 4px 8px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.05);
  --elevation-4: 0 8px 16px rgba(0,0,0,0.1), 0 4px 8px rgba(0,0,0,0.06);
  --elevation-5: 0 16px 32px rgba(0,0,0,0.12), 0 8px 16px rgba(0,0,0,0.08);

  /* Z-Index */
  --z-base: 0;
  --z-raised: 10;
  --z-sticky: 100;
  --z-overlay: 200;
  --z-modal: 500;
  --z-toast: 1000;
  --z-tooltip: 1100;
}
```

---

## 9. Power BI Layout Reference

### Canvas Settings
- **Page Size**: 16:9 (1920 × 1080) — Fixed for desktop
- **Page Alignment**: Center
- **Wallpaper**: `neutral-50` (light) / `neutral-0` (dark)

### Visual Margins (Default)
- **Visual Padding**: 12px (card) / 16px (KPI)
- **Visual Gap**: 16px (between visuals)
- **Page Margin**: 24px (all sides)

### Responsive Behavior (Power BI Service)
| Viewport | Layout Adjustment |
|----------|-------------------|
| ≥1920px | Full 12-col, all visuals at design size |
| 1366-1919px | KPI cards 2×2 grid, charts scale to 90%, side slicers collapse |
| 1024-1365px | Single column stack, slicers in hamburger menu |
| 768-1023px | Phone layout (separate design) |

---

## 10. Usage Rules

1. **Always** use spacing tokens — never hardcode px/rem values
2. **Base unit** is 4px — all values are multiples of 4px
3. **Responsive spacing** uses fluid clamp — no media queries for spacing
4. **Grid gutters** and **margins** are separate tokens — don't conflate
5. **Component padding** scales independently from page margins
6. **Card radius** is responsive — 8px mobile, 12px desktop
7. **Shadows** use elevation tokens — match component elevation to purpose
8. **Z-index** only from defined scale — no arbitrary values
9. **Print**: Remove shadows, set elevation-0, collapse margins to `space-2`
10. **Animation**: Spacing transitions use `transition: margin 150ms ease, padding 150ms ease, gap 150ms ease`