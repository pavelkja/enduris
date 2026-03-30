# Technical Visual Style Specification: Enduris.app (v1.0)

This document serves as a guideline for the frontend implementation of the Enduris.app application. The goal is to achieve a clean, analytical, and calm interface with a strong focus on Dark Mode and data accuracy.

---

## 1. Design Tokens (Core Variables)

### 1.1 Color Palette (Solid Colors Only)
No gradients, shadows, or transparency unless explicitly stated otherwise.

| Token | HEX | Usage in UI |
|------|-----|-------------|
| --color-bg-base | #0A0C10 | Main application background (Deep Obsidian) |
| --color-bg-card | #1F2329 | Background for modules and cards (Slate Gray) |
| --color-text-primary | #E0E6ED | Primary text and values (Pure Ash) |
| --color-text-secondary | #A1B1C1 | Muted text, labels, chart axes |
| --color-primary | #34D399 | Brand color, positive trends (Bio-Green) |
| --color-accent-data | #60A5FA | Comparative data, neutral lines (Data Blue) |
| --color-accent-alert | #FBBF24 | Introspection, warnings (Amber Glow) |
| --color-border | #2D343C | Grid lines, separators |

---

### 1.2 Typography

- **Primary font:** Inter (Google Fonts)

- **Headings (H1, H2):**  
  Inter, Weight: 700 (Bold) / 600 (SemiBold)

- **Body Text:**  
  Inter, Weight: 400 (Regular), Line-height: 1.5

- **Data / Numbers:**  
  Inter, Weight: 700 (Bold), `font-variant-numeric: tabular-nums`

- **Labels / Mono:**  
  Inter, Weight: 400, Size: 12px (for axis labels and tooltips)

---

### 1.3 Layout & Spacing

- **Base Unit:** 8px

- **Cards:**  
  Border-radius: 8px  
  Padding: 24px

- **Gap (Spacing):**  
  Between cards: 24px or 32px

- **Grid:**  
  12-column system or CSS Grid for dashboard modules

---

## 2. Components & UI Elements

### 2.1 Logo (SVG)

- **Appearance:**  
  A closed circle with a rising curve (uniform stroke width)

- **Color:**  
  `--color-primary`

- **Text:**  
  `ENDURIS.APP` (All caps, Inter SemiBold)

---

### 2.2 Data Cards (DataCard)

- **Background:**  
  `--color-bg-card`

- **Internal Structure:**
  - Title (Small Caps or SemiBold, `--color-text-secondary`)
  - Main value (Large, Bold, `--color-text-primary`)
  - Trend indicator (Small, `--color-primary` for growth)

---

### 2.3 Charts (TrendGraph)

- **Line Style:**  
  Smooth spline curve (interpolation), thickness 2.5px

- **Visual Style:**  
  No fill (no area fill). Clean line only.

- **Grid:**  
  Horizontal lines only, color `--color-border`, thickness 1px

- **Interaction:**  
  On hover: thin vertical line across the entire chart  
  Tooltip: background `--color-bg-card` with white border

---

### 2.4 Navigation (Sidebar)

- **Background:**  
  `--color-bg-base` (or a slightly darker variation)

- **Icons:**  
  Linear (outline), stroke width 2px

- **Active State:**  
  Color `--color-primary` + 3px vertical indicator on the left edge

---

### 2.5 Buttons and CTA

- **Primary:**  
  Background `--color-primary`  
  Text `#0A0C10` (high contrast)

- **Secondary:**  
  Outline `--color-border`  
  Text `--color-text-primary`

- **Border Radius:**  
  4px

---

## 3. Behavior & Interaction

- **Hover States:**  
  Subtle background lightening of cards (approx. +5%)

- **Transitions:**  
  Smooth transitions for colors and hover states (0.2s ease-in-out)

- **Responsiveness:**  
  On mobile devices, cards stack vertically  
  Padding reduces to 16px

---

## Developer Note

The style should feel like a blend of Linear and Garmin Connect, with an emphasis on a calm, "laboratory-like" aesthetic inspired by mountains and health.

Avoid unnecessary animations — prioritize speed and data readability.
