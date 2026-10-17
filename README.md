# URBAN VISION AI — SAFEBUILD
**Community-First Infrastructure Safety & Resilience Decision System**
*Seva First Innovation Challenge (SFIC) 2026 — Track A (Product & Technology / Undergraduate)*

---

## 1. System Overview
SafeBuild evaluates how proposed infrastructure construction arrangements and access modifications disrupt resident connectivity to essential facilities (e.g. healthcare), computes attribution across a 5-state scenario algebra, and optimizes feasible mitigations under strict physical, legal, and operational constraints.

### Core Hard Invariants
1. **Zero Invented Real-World Outcomes**: Detour distances are calculated deterministically on directed graphs. Never present calculated route distance as measured ambulance response times or live traffic speeds.
2. **Deterministic 5-State Scenario Algebra**:
   - $G_0$: Baseline verified existing network.
   - $G_0 + C$: Baseline with construction disruption.
   - $G_0 + P$: Baseline with proposed permanent network changes ($P = \text{identity}$ if no official public road changes exist).
   - $G_0 + P + C$: Proposal under construction disruption.
   - $G_0 + P + C + M$: Proposal under construction with candidate mitigation.
3. **Attribution Isolation**: Proposal effect $(G_0+P - G_0) = 0.0\text{ m}$ is preserved as an invariant when $P$ is identity.
4. **Feasibility Hard Gate**: Candidates without verified physical review and confirmed statutory police permission remain labeled `UNVERIFIED` / `GRAPH_ONLY`. When no implementable option exists, the optimizer strictly emits `NO_VERIFIED_OPTION`.
5. **Guarded Read-Only AI**: Server assertion filters intercept ungrounded numbers, causal leaps, or fabricated approvals prior to display.

---

## 2. Quickstart & Local Setup

### Prerequisites
- Python 3.12+
- Node.js 20+ / npm

### Step 1: Backend Setup
```bash
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install fastapi uvicorn pydantic networkx shapely reportlab requests google-genai
```

### Step 2: Run Tests
```bash
./venv/bin/python -m unittest backend/tests/test_analytical_core.py
./venv/bin/python -m unittest backend/tests/test_validation_protocol.py
```

### Step 3: Launch Backend Server
```bash
./venv/bin/uvicorn backend.api.server:app --host 0.0.0.0 --port 8000
```

### Step 4: Frontend Setup & Run
```bash
cd frontend
npm install
npm run build
npm run start -- -p 3000
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 3. Architecture & API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | System health, dataset node count, edge count, and AI status |
| `/api/metadata` | GET | Study area metadata, facility anchors, and OSM provenance |
| `/api/analysis` | GET | 5-state route attribution, origin metrics, and GeoJSON paths |
| `/api/optimizer` | GET | Exact finite evaluation of all registered candidate mitigations |
| `/api/report/csv` | GET | RFC 4180 compliant CSV export of the 5-state per-origin matrix |
| `/api/report/pdf` | GET | Multi-page decision document generated via ReportLab |
| `/api/ai/ask` | POST | Guarded geospatial AI analyst with server-side assertion filters |

---

## 4. Primary Provisional Pilot: Kakkanad, Kochi
- **Core Bounding Box**: `[76.335, 10.015, 76.355, 10.030]`
- **Full Routing Buffer**: `[76.330, 10.010, 76.360, 10.035]`
- **Nodes Parsed**: 19,582 nodes with 0 missing highway references
- **Directed Road Edges**: 11,675 motor vehicle edges; 11,733 pedestrian edges
- **Project Context**: Kochi Metro Rail Phase II (JLN Stadium to Infopark via Kakkanad)
- **Primary Facility Anchor**: Sunrise Hospital, Seaport-Airport Road (`fac_sunrise`)

---

## 5. Risk Gate & Release Status
See [RISK_GATE_STATUS.md](file:///home/ismail/Documents/SEWA%20URBAN/RISK_GATE_STATUS.md) for individual verification logs across all 16 risk gates (RG-01 to RG-16).
- **Current Operational Status**: Validated Research Prototype.
- **Field Pilot Status**: `NOT_FIELD_PILOTED` (requires official signed municipal partnership).
