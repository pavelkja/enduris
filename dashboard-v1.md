# Dashboard v1.0 – Specification

## 🎯 Goal

Vytvořit jednoduchý, rychlý a rozšiřitelný dashboard pro přehled sportovních aktivit (Strava data), který:

* zobrazí základní statistiky (YTD + měsíce)
* umožní přepínání mezi sporty
* slouží jako základ pro další analytiku (efficiency, trendy, insighty)

---

## 🧭 UI Structure

### Sport Filter (top switch)

Možnosti:

* `cycling_overall`
* `ride`
* `run`
* další sport_type dle dostupných dat

Chování:

* všechny endpointy respektují parametr `sport`
* `cycling_overall` = subset cycling aktivit:

  * Ride
  * GravelRide
  * MountainBikeRide
  * VirtualRide

---

## 📊 Section 1: Year-to-Date Comparison

### Popis

Zobrazuje agregovaná data pro:

* aktuální rok (YTD)
* minulý rok
* předminulý rok

---

### Endpoint

GET `/api/dashboard/ytd?sport=ride`

---

### Response

```json
[
  {
    "year": 2026,
    "metrics": {
      "distance": 1234.5,
      "rides": 45,
      "elevation": 15000,
      "time": 36000,
      "avg_hr": 142
    }
  },
  {
    "year": 2025,
    "metrics": { ... }
  },
  {
    "year": 2024,
    "metrics": { ... }
  }
]
```

---

### Metrics Definition

* `distance` → km
* `rides` → počet aktivit
* `elevation` → metry
* `time` → sekundy (frontend formátuje na hh:mm)
* `avg_hr` → průměrná tepová frekvence (simple average pro MVP)

---

## 📅 Section 2: Monthly Comparison

### Popis

Zobrazuje data pro:

* aktuální měsíc
* stejný měsíc minulý rok
* stejný měsíc předminulý rok
* minulý měsíc
* měsíc předtím

---

### Endpoint

GET `/api/dashboard/months?sport=ride`

---

### Response

```json
[
  {
    "label": "current_month",
    "month": "2026-03",
    "metrics": {
      "distance": 320,
      "rides": 12,
      "elevation": 4200,
      "time": 9800,
      "avg_hr": 145
    }
  },
  {
    "label": "same_month_last_year",
    "month": "2025-03",
    "metrics": { ... }
  },
  {
    "label": "same_month_two_years",
    "month": "2024-03",
    "metrics": { ... }
  },
  {
    "label": "previous_month",
    "month": "2026-02",
    "metrics": { ... }
  },
  {
    "label": "previous_month_last_year",
    "month": "2025-02",
    "metrics": { ... }
  }
]
```

---

## 🧠 Metrics Structure (IMPORTANT)

Všechny endpointy používají jednotnou strukturu:

```json
"metrics": {
  "distance": number,
  "rides": number,
  "elevation": number,
  "time": number,
  "avg_hr": number
}
```

### Pravidla:

* struktura se NEMĚNÍ
* nové metriky se pouze PŘIDÁVAJÍ
* frontend se nesmí rozbít při rozšíření

---

## ⚙️ Backend Logic

### Data Source

Primárně:

* `activities` table

Agregace:

* SUM(distance)
* COUNT(*)
* SUM(elevation_gain)
* SUM(moving_time)
* AVG(avg_hr)

---

### Sport Filtering

Parametr:

* `sport=ride`
* `sport=run`
* `sport=cycling_overall`

Mapping:

* `cycling_overall` → více `sport_type`

---

## 🧱 Architecture Principles

### 1. Endpoint = UI block

Každá sekce dashboardu má vlastní endpoint:

* `/ytd`
* `/months`
* (future: `/efficiency`, `/trends`)

---

### 2. Backend returns ready-to-render data

* frontend nepočítá agregace
* frontend pouze renderuje

---

### 3. Stable data contract

* struktura response je stabilní
* změny probíhají pouze rozšířením

---

## 🚀 Future Extensions (NOT in v1)

### Planned endpoints:

* GET `/api/dashboard/efficiency`
* GET `/api/dashboard/trends`
* GET `/api/dashboard/load`

### Possible new metrics:

* efficiency
* HR drift
* load score
* aerobic decoupling

---

## ❌ Out of scope (v1)

* grafy
* segment analytics
* AI insighty
* kombinace více sportů najednou

---

## ✅ MVP Definition

Dashboard v1.0 je hotový, pokud:

* funguje sport filter
* funguje `/ytd` endpoint
* funguje `/months` endpoint
* data se zobrazují na frontendu (i bez stylování)

---

## 🧭 Notes

* cílem není perfektní přesnost (např. HR weighting)
* cílem je rychlé dodání funkčního dashboardu
* přesnost a pokročilé metriky přijdou v dalších verzích

---
