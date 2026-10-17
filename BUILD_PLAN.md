# SafeBuild: Engineering Build Plan and Risk Gates

## 1. Executive Summary & Core Objective
SafeBuild is a community-first infrastructure safety, accessibility, and resilience decision workspace. It evaluates how proposed construction or access modifications affect resident accessibility to essential facilities (e.g. healthcare), computes attribution across a rigorous 5-state scenario algebra, and optimizes feasible mitigations under strict physical, legal, and operational constraints.

## 2. Hard Invariants & Non-Negotiable Contracts
1. **Zero Invented Real-World Outcomes**: Distance and reachability are calculated deterministically on directed graphs. Never present calculated route distance as measured ambulance response times or live traffic speeds.
2. **Deterministic 5-State Scenario Algebra**:
   - $G_0$: Baseline verified existing network.
   - $G_0 + C$: Baseline with construction disruption.
   - $G_0 + P$: Baseline with proposed permanent network changes ($P = \text{identity}$ if no official public road changes exist).
   - $G_0 + P + C$: Proposal under construction disruption.
   - $G_0 + P + C + M$: Proposal under construction with candidate mitigation.
3. **Attribution Isolation**:
   - Baseline weakness: $G_0$
   - Construction impact: $G_0 + C - G_0$
   - Proposal impact: $G_0 + P - G_0$
   - Interaction: $(G_0 + P + C - G_0 + P) - (G_0 + C - G_0)$
   - Mitigation recovery: $G_0 + P + C + M - G_0 + P + C$
4. **Feasibility Gate**: Candidates without verified physical review and confirmed legal permission remain labeled `UNVERIFIED` / `GRAPH_ONLY`. When no implementable option exists, return `NO_VERIFIED_OPTION`.
5. **Read-Only Guarded AI**: AI model performs factual synthesis grounded strictly in verified structured run records. Numeric claims are checked by server assertion filters before rendering. If AI is unavailable or unconfigured, the deterministic application functions completely.

## 3. Implementation Slices
- **Slice 1**: Verified Kakkanad buffered OSM acquisition, referential integrity check, directed graph builder, and hand-computed unit fixtures.
- **Slice 2**: Scenario engine (5 states), origin-to-destination accessibility routing, detour & reachability attribution, and CSV/PDF report generators.
- **Slice 3**: Candidate registry, exact finite optimization, sensitivity analysis (ranking stability), and common-cause risk detection.
- **Slice 4**: Decision workspace UI (Geographic Canvas, Scenario Comparison & Community Lens, Evidence Inspector, Guided 90s Jury Demo, Landing Page).
- **Slice 5**: Guarded AI Analyst with validation corpus checks.
- **Slice 6**: Comprehensive verification suite, test runs, reproduction manifests, and Go/No-Go readiness audit.
