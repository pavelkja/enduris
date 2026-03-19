# enduris
App for longevity data analysis above Strava activities
Aplikace pro analýzu Strava aktivit zaměřená na longevity. Chci sportovat do 100 let, ne se honit za každým KOMem v okolí.

# Strava Health Analytics

Webová aplikace pro pokročilou analýzu sportovních aktivit synchronizovaných ze Stravy.

Projekt je zaměřený na **health / longevity analytiku**, interpretaci srdečního tepu a dlouhodobý vývoj kondice.

Strava slouží pouze jako zdroj dat. Veškerá analytika probíhá v této aplikaci.

---

# Hlavní funkce

## Health analytics

Analýza organismu na základě dat aktivit:

- cardiovascular efficiency
- HR drift
- cardio load
- dlouhodobý trend kondice

## Activity analytics

Statistiky aktivit:

- distance per year
- distance per month
- rolling 30 days
- elevation gain

## Segment analytics

Analýza opakovaných úseků (např. kopců):

- historie času
- vývoj srdečního tepu
- detekce odchylek výkonu

## Personal dashboard

Přehled:

- km this year
- elevation this year
- rides this year
- trend efektivity

---

# Technologie

## Backend

- Python
- FastAPI
- PostgreSQL

## Frontend

- Next.js
- React
- Chart.js / Recharts

---

# Architektura

Workflow aplikace:
Strava API
↓
Import activities
↓
Import streams
↓
Compute metrics
↓
Store results
↓
Dashboard & analytics


Strava slouží pouze pro synchronizaci dat.

Analytika probíhá nad lokální databází.

---

# Autentizace

Přihlášení probíhá přes Strava OAuth.

Workflow:

1. User clicks **Connect with Strava**
2. Strava OAuth login
3. Application receives:

- athlete_id
- access_token
- refresh_token

Tokeny se ukládají do databáze.

---

# Synchronizace dat

## První synchronizace
GET /athlete/activities


Pagination: 30 aktivit na request.

## Další synchronizace

GET /athlete/activities?after=timestamp


Timestamp je uložen v `users.last_sync`.

## Alternativa

Strava webhook:

- activity created
- activity updated

Server stáhne pouze nové aktivity.

---

# Datový model

## Project structure

backend/ – FastAPI backend (main application)

## Users

| field | type |
|------|------|
| id | uuid |
| strava_athlete_id | bigint |
| name | text |
| access_token | text |
| refresh_token | text |
| last_sync | timestamp |

## Activities

| field | type |
|------|------|
| id | bigint |
| user_id | uuid |
| sport_type | text |
| start_date | timestamp |
| distance | float |
| moving_time | int |
| elapsed_time | int |
| elevation_gain | float |
| avg_speed | float |
| max_speed | float |
| avg_hr | float |
| max_hr | float |

## Activity Streams

| field | type |
|------|------|
| activity_id | bigint |
| user_id | uuid |
| time | int |
| heartrate | int |
| speed | float |
| cadence | float |
| altitude | float |
| grade | float |
| lat | float |
| lon | float |

## Segments

| field | type |
|------|------|
| id | bigint |
| name | text |
| distance | float |
| avg_grade | float |

## Segment Efforts

| field | type |
|------|------|
| activity_id | bigint |
| user_id | uuid |
| segment_id | bigint |
| elapsed_time | int |
| avg_hr | float |
| max_hr | float |

## Activity Metrics

| field | type |
|------|------|
| activity_id | bigint |
| user_id | uuid |
| metric_name | text |
| value | float |

## Daily Metrics

| field | type |
|------|------|
| user_id | uuid |
| date | date |
| distance | float |
| elevation | float |
| load_score | float |

---

# Raw Data vs Derived Data

## Raw data

- activities
- activity_streams
- segment_efforts

Obsahují originální data ze Stravy.

## Derived data

- activity_metrics
- daily_metrics
- segment_metrics

Obsahují výsledky analytiky.

Výhoda:

- metriky lze kdykoliv přepočítat
- lze přidávat nové analytické algoritmy

---

# Metrics System

Metriky jsou implementovány jako pluginy.

Struktura:
metrics/
efficiency.py
hr_drift.py
load_score.py

Každá metrika implementuje funkci:

compute(activity, streams)


Výsledky se ukládají do tabulky `activity_metrics`.

---

# MVP Metriky

## Cardiovascular Efficiency
efficiency = avg_speed / avg_hr

## HR Drift
drift = (HR_second_half - HR_first_half) / HR_first_half

## Cardio Load
load = sum(time_in_zone * zone_weight)


---

# Dashboard

## Overview

- km this year
- elevation this year
- rides this year

## Seasonality

distance per month  
comparison between years

## Health

- efficiency trend
- HR drift trend

## Segments

- segment history
- HR stability

---

# Development Roadmap

## Phase 1 – Strava integration

- Strava OAuth
- import activities

## Phase 2 – Streams import

- import activity streams

## Phase 3 – Metrics engine

- efficiency
- HR drift
- cardio load

## Phase 4 – Dashboard

- overview
- seasonality
- health metrics

## Phase 5 – Segment analytics

- segment history
- HR deviation

## Phase 6 – Sync improvements

- incremental sync
- Strava webhook

## Phase 7 – Advanced analytics

- terrain efficiency
- fatigue detection
- recovery score

---

# Development Setup

## Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

## Frontend
cd frontend
npm install
npm run dev

---

# Environment Variables
DATABASE_URL=
STRAVA_CLIENT_ID=
STRAVA_CLIENT_SECRET=
STRAVA_REDIRECT_URI=


---

# Future Extensions

- Garmin integration
- Apple Health integration
- AI interpretation of training data
- training recommendations
- advanced performance analytics

---

# License

MIT

# Synchronization Architecture

Tato sekce popisuje strategii synchronizace dat ze Stravy.

Cílem je:

- minimalizovat počet API requestů
- zvládnout uživatele s tisíci aktivitami
- umožnit postupné rozšiřování analytiky
- oddělit raw data od analytických výpočtů

---

# Typy synchronizace

Aplikace používá dva typy synchronizace:

1. **Initial Sync** – první import všech aktivit
2. **Incremental Sync** – pravidelné importy nových aktivit

---

# Initial Sync (první synchronizace)

Při prvním připojení uživatele může mít Strava účet stovky až tisíce aktivit.

Strava API vrací:

- max 30 aktivit na request
- pagination přes `page`

Proto může první synchronizace vyžadovat desítky až stovky API volání.

Initial sync probíhá **asynchronně na pozadí**.

---

## Workflow

1. User klikne **Connect with Strava**
2. Proběhne **Strava OAuth**
3. Server získá:
athlete_id
access_token
refresh_token

4. Vytvoří se záznam v `users`
5. Spustí se background job `initial_sync`

---

## Initial Sync Worker

Worker provede:
GET /athlete/activities?page=X&per_page=30

Loop pokračuje dokud API nevrátí prázdnou odpověď.

Do databáze se uloží pouze **summary data aktivit**.

---

## Ukládaná data

Tabulka `activities` obsahuje:

- activity_id
- sport_type
- start_date
- distance
- moving_time
- elevation_gain
- avg_speed
- avg_hr
- max_hr

Tyto údaje jsou dostatečné pro základní statistiky:

- km per year
- elevation per year
- rides per year

---

# Streams Import Strategy

Streams obsahují detailní data aktivity:

- heart rate
- speed
- altitude
- cadence
- GPS

Endpoint:
GET /activities/{id}/streams

Streams jsou **nejdražší část API**.

Proto se nestahují během první synchronizace.

---

## Lazy Streams Import

Streams se importují později pomocí workeru.

Strategie:

1. Initial sync uloží pouze activities
2. Worker postupně importuje streams
3. Streams se importují pouze jednou

Streams se totiž **nikdy nemění**.

---

# Streams Worker

Worker hledá aktivity kde:
streams_imported = false

a postupně stahuje:
GET /activities/{id}/streams

Po úspěšném importu:
streams_imported = true

Poté může běžet výpočet metrik.

---

# Metrics Processing

Po importu streams se spustí:
compute_metrics(activity)

Výsledky se ukládají do:
activity_metrics
daily_metrics
segment_metrics

Po dokončení:
metrics_computed = true

---

# Incremental Sync

Po dokončení první synchronizace se uloží:
users.last_sync

Další synchronizace používá:
GET /athlete/activities?after=timestamp

Importují se pouze nové aktivity.

Workflow:
import activity
↓
import streams
↓
compute metrics

---

# Rate Limiting

Strava API limity:
200 requests / 15 minutes
2000 requests / day

Worker musí implementovat throttling.

Například:
sleep(0.2)

nebo queue systém.

---

# Sync Status

Pro UI je vhodné sledovat stav synchronizace.

Pole v `users`:
sync_status

Možné hodnoty:
pending
syncing
processing
ready
error

Frontend může zobrazit například:
Importing your activities...
Processing training data...

---

# Streams Data Model

Streams obsahují velké množství dat.

Například:

- 1 hodina jízdy = ~3600 datových bodů
- 1000 aktivit = miliony řádků

Proto není optimální ukládat každý bod jako samostatný řádek.

---

## Doporučená struktura

Streams se ukládají jako **JSON array per activity**.

Tabulka:
activity_streams

| field | type |
|------|------|
| activity_id | bigint |
| user_id | uuid |
| stream_type | text |
| data | jsonb |

---

## Příklad
activity_id: 123456
stream_type: heartrate
data:
[120,121,123,125,126,130,...]

Další stream:
stream_type: speed
data: [7.1,7.3,7.2,...]

---

## Výhody

- dramaticky méně řádků v databázi
- rychlejší import
- jednodušší cache
- lepší výkon při analýze

---

# Kompletní Sync Workflow
User login
↓
OAuth Strava
↓
Create user
↓
enqueue initial_sync
↓
download activities
↓
store activities
↓
enqueue streams worker
↓
download streams
↓
compute metrics
↓
dashboard ready

---

# Key Principles

Projekt používá několik důležitých principů:

### 1️⃣ Strava je pouze zdroj dat

Analytika probíhá **lokálně**.

---

### 2️⃣ Raw data vs derived data

Raw data:
activities
activity_streams
segment_efforts

Derived data:
activity_metrics
daily_metrics
segment_metrics

Derived data lze kdykoliv přepočítat.

---

### 3️⃣ Streams import only once

Streams:

- se nikdy nemění
- importují se pouze jednou
- výrazně šetří API limity

---

### 4️⃣ Background processing

Všechny náročné operace běží v workerech:

- initial sync
- streams import
- metrics computation

Frontend tak zůstává rychlý.

---

# Future Improvements

Možná budoucí rozšíření synchronizace:

- Strava Webhooks
- real-time activity import
- partial stream loading
- caching streams
- batch metrics computation

## Activity Filtering

Pro analytiku se používají pouze aktivity, které mají smysl pro vyhodnocení fyzického výkonu.

### Supported activity types

- Ride
- VirtualRide
- Run
- TrailRun
- VirtualRun

Tyto sporty mají relativně stabilní vztah mezi tepem a výkonem.

E-bike aktivity nejsou zahrnuty, protože elektrická asistence výrazně zkresluje výkonové metriky.

### Heart rate requirement

Aktivity bez srdečního tepu nejsou analyzovány.

Podmínka:

activity.has_heartrate == true

Pouze aktivity s HR daty jsou dále zpracovány a jsou pro ně stahovány streams.

# Backend Implementation Order

Tato sekce popisuje doporučené pořadí implementace backendu.

Cílem je:

- minimalizovat riziko slepých uliček při práci se Strava API
- rychle ověřit funkčnost celé pipeline
- mít co nejdříve funkční MVP
- umožnit postupné rozšiřování analytiky

Vývoj probíhá iterativně – každý krok by měl být samostatně otestovatelný.

---

# Step 1 – Basic Backend Setup

Inicializace backendu.

Technologie:

- FastAPI
- PostgreSQL
- SQLAlchemy / SQLModel

Základní struktura projektu:
backend/
app/
main.py
database.py
models/
services/
metrics/
workers/

Cíl:

- běžící API server
- funkční připojení k databázi

---

# Step 2 – Database Schema

Implementace základního databázového modelu.

Nejdůležitější tabulky:

- users
- activities
- activity_streams
- activity_metrics
- daily_metrics

Každá tabulka obsahuje `user_id`, aby bylo možné podporovat více uživatelů.

Důležité indexy:
CREATE INDEX idx_activities_user_date
ON activities(user_id, start_date);

---

# Step 3 – Strava OAuth

Implementace přihlášení přes Strava.

Workflow:

1. User klikne **Connect with Strava**
2. Redirect na Strava OAuth
3. Strava vrátí authorization code
4. Server získá:
access_token
refresh_token
athlete_id

Tyto údaje se uloží do tabulky `users`.

---

# Step 4 – Activities Import

Implementace endpointu pro import aktivit.

Strava endpoint:
GET /athlete/activities

Pagination:
page
per_page=30

Import probíhá v loopu, dokud API vrací data.

Ukládají se pouze **summary data aktivit**.

---

# Step 5 – Activity Filtering

Při importu aktivit se aplikují základní filtry.

### Supported activity types

- Ride
- VirtualRide
- Run
- TrailRun
- VirtualRun

### Heart rate requirement

Aktivity musí splňovat:
activity.has_heartrate == true

Aktivity bez HR se neanalyzují.

---

# Step 6 – Background Worker

Synchronizace aktivit nesmí blokovat API.

Implementuje se jednoduchý worker:

- FastAPI background tasks
- nebo RQ / Celery

Worker zpracovává:

- initial sync
- streams import
- výpočet metrik

---

# Step 7 – Streams Import

Streams obsahují detailní data aktivity.

Strava endpoint:
GET /activities/{id}/streams

Importují se pouze pro aktivity, které:

- prošly filtrem sportu
- obsahují HR data

Streams se importují pouze jednou.

Po importu:
streams_imported = true

---

# Step 8 – Metrics Engine

Implementace systému metrik.

Struktura:
metrics/
efficiency.py
hr_drift.py
load_score.py

Každá metrika implementuje:
compute(activity, streams)

Výsledky se ukládají do:
activity_metrics

---

# Step 9 – Daily Aggregation

Výpočet denních statistik.

Tabulka:
daily_metrics

Obsahuje například:

- distance
- elevation
- load_score

Tyto agregace výrazně zrychlují dashboard.

---

# Step 10 – Dashboard API

API endpointy pro frontend.

Například:
GET /api/dashboard/overview
GET /api/dashboard/seasonality
GET /api/dashboard/health

Vrací agregovaná data pro grafy.

---

# MVP Completion Criteria

MVP je hotové, pokud aplikace zvládá:

- Strava OAuth login
- import aktivit
- import streams
- výpočet základních metrik
- dashboard s grafy

---

# Post-MVP Extensions

Po ověření MVP lze postupně přidávat:

- steady effort detection
- terrain efficiency
- fatigue detection
- recovery score
- segment analytics
- Strava webhooks
- real-time activity updates

Architektura aplikace je navržena tak, aby tyto funkce bylo možné přidávat bez zásahu do existujících dat.



Tohle je shrnutí ze dne 17.3.2026, kde už jsme vytvořili celou řadu náležitostí:
# Enduris.app – Backend & Analytics Overview

## 🎯 Vision

Enduris.app je webová aplikace zaměřená na analýzu sportovních aktivit (Strava) s cílem poskytovat smysluplné insighty o výkonnosti, konzistenci a dlouhodobém vývoji kondice.

Cílem není zobrazovat pouze data, ale interpretovat je:
→ co se děje s výkonností a proč.

---

## 🧱 Technologie

- Backend: FastAPI (Python)
- Databáze: PostgreSQL (Neon)
- ORM: SQLAlchemy
- Data source: Strava API

---

## 📊 Datový model

### Tables

- `users`
- `activities`
- `activity_streams`
- `activity_metrics`
- `daily_metrics`

---

## ⚙️ Metrics Engine

- metriky implementovány jako pluginy (`app/metrics/`)
- ukládání do `activity_metrics`
- UNIQUE (activity_id, metric_name)
- UPSERT (idempotentní výpočty)

### Implementované metriky:

- efficiency
- hr_drift
- avg_hr_percent
- aerobic_decoupling

---

## 📈 Trend Analytics

### 1) Time-based (daily_metrics)

- agregace po dnech
- rolling averages:
  - 7 dní
  - 14 dní

Použití:
- dlouhodobý přehled
- sezónní trendy

---

### 2) Activity-based (hlavní přístup)

- výpočty přes SQL window functions
- rolling:
  - last 5 aktivit
  - last 10 aktivit

Důvod:
→ přesnější než časové okno (uživatel trénuje nepravidelně)

---

## 🧩 Segmentace

Používá se `sport_type` ze Strava API:

- Ride
- MountainBikeRide
- GravelRide
- VirtualRide
- Run
- TrailRun

👉 žádná heuristika (speed apod.)  
→ vyhnutí se chybné klasifikaci

---

## 🧠 Interpretace dat (Insight Engine – v základu)

### Trend

- improving
- declining
- stable

→ založeno na rozdílu last_5 vs last_10  
→ s thresholdem (eliminace šumu)

---

### Confidence

- low (<5 aktivit)
- medium (5–9 aktivit)
- high (10+ aktivit)

→ určuje spolehlivost trendu

---

### Variability

- very_stable
- stable
- volatile

→ založeno na standard deviation (efficiency)

---

## 🔌 API Endpoints

### `/dashboard/health`
- time-based trend (daily_metrics)

### `/dashboard/efficiency-trend`
- activity-based trend
- vrací:
  - trend
  - confidence
  - variability
  - data

### `/dashboard/sport-types`
- seznam dostupných sportů pro uživatele

---

## 🧠 Klíčové principy návrhu

- nemíchat různé sporty → segmentace
- raději méně dat, ale kvalitních
- activity-based analýza > time-based
- oddělení:
  - data (DB)
  - výpočty (services)
  - API (routers)

---

## 🚧 Další kroky

- Insight layer (lidské interpretace)
- fatigue detection
- kombinace metrik (HR drift + efficiency)
- UI dashboard
- personalizace

---

## 🔥 Aktuální stav

Projekt obsahuje funkční analytický backend, který:

- zpracovává Strava data
- počítá pokročilé metriky
- analyzuje trendy výkonnosti
- rozlišuje kvalitu signálu (confidence, variability)

→ připraveno pro další vrstvu: interpretace a UI
