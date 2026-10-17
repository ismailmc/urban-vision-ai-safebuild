# Proposed engineering protocol and acceptance tests
All thresholds below are proposed targets to freeze **before** evaluation; none is an achieved result. They are engineering acceptance choices, not empirical standards. Keep actual failures.

## Five-state controlled attribution
Freeze base directed mode-specific graph G0, resident origins O, essential facility entrances D, lengths, costs, phase, snapping policy and source snapshot.
C = explicit restriction transform; P = public-network proposal transform; M = reviewed candidate transform.
Evaluate G0, G0+C, G0+P, G0+P+C, G0+P+C+M.
Per origin: route distance to same designated destination and nearest eligible destination, reachability, detour where finite, destination switches, worst-case supported disruption.
- Existing weakness: G0 state.
- Closure effect: metric(G0+C) minus metric(G0).
- Proposal effect: metric(G0+P) minus metric(G0).
- Proposal under closure: metric(G0+P+C) minus metric(G0+C).
- Closure in proposal: metric(G0+P+C) minus metric(G0+P).
- Interaction: difference of the two closure effects, only when comparable finite metrics exist.
- Mitigation: metric(G0+P+C+M) minus metric(G0+P+C).
Reachability transitions are categorical. Do not subtract infinities or calculate percentage detours for a zero/unreachable denominator. Missing topology/access is UNKNOWN, distinct from proven modeled unreachability.

An unchanged road graph with changed development massing cannot establish changed road reachability. If P identity, proposal effects must be zero. Static distance without demand/speeds cannot establish congestion or emergency response time.
One source may corroborate a project, not the causality of a calculated outcome.

## Network correctness
Use OSM topology and grade information, retain turn relations or implement edge-based transition restrictions. Keep parallel directed edges. A shortest-path engine without turn semantics is insufficient for a turn-constrained safety claim. QGIS simple line-network routing is an independent reference only for equivalent simpler profiles:
https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/networkanalysis.html
A route-aware secondary engine can help identify disagreements, but differences must be reconciled by profile and source-date, not majority vote:
https://project-osrm.org/docs/v5.22.0/api/?language=Python

No arbitrary nearest-node snapping across walls/rivers/private gates; store entrance connectors and review them. Lengths measured geodesically or in locally appropriate metric CRS (candidate UTM 43N for Kochi, verify CRS transformation).
Expand routing buffer and include relevant destinations beyond the study core; calculate metrics only for frozen core origins. No universal fixed buffer size.

## Interventions to investigate — all unapproved
| Candidate | Geometry/effect | Geographic/physical requirements | Permission/ownership unknown | Complexity and cost inputs | Community check/status |
|---|---|---|---|---|---|
| Preserve a current permitted connection during a work phase | Keep reviewed existing movement open | Work-zone separation, width, sight lines, pedestrian protection | Road owner and works/traffic approval | Temporary barrier/signage/traffic staffing BOQ | Existing-road-based; GRAPH CANDIDATE ONLY |
| Sequence supplied restrictions instead of simultaneous closure | Change closure time/order, not geography | Construction dependencies and access continuity | Contractor/KMRL/traffic authorization | Phase durations, safety/staffing quantities | Examine who bears longer exposure; UNVERIFIED |
| Supplied diversion on existing allowed roads | Change permitted movement only | Width, loads, gates, turns, condition and conflict audit | Not assumed from OSM public-looking geometry | Signs/control/reinstatement; unknown rates | Check residential burden and pedestrians; UNVERIFIED |
| Retain publicly permitted internal/external access | Preserve source-backed connector | Surveyed existing connection and work conflict | Public rights/easement must be demonstrated | Design/temporary works quantities unknown | Private gate must not count as public access; UNVERIFIED |

No candidate is physically/legal implementable merely because it is graph-feasible. Road name presence in sample is not permission proof.
Use statuses REJECTED, GRAPH_ONLY, PHYSICAL_REVIEWED, PERMISSION_CONFIRMED, VERIFIED_FOR_SPECIFIED_PHASE. Only last status qualifies for implementable recommendation. Return NO_VERIFIED_OPTION when absent.
For small finite candidates enumerate every permitted combination with conflicts/dependencies. Lexicographic objective: avoid new unreachable origins; minimize worst supported detour; then distribution/cost if reliable. Display tradeoffs and uncertainty, not universal “safer” claims. Unknown costs cannot become zero.
Common cause: group segments sharing bridges, junctions or work zones; edge-disjoint routes sharing one group are not independent corridors.

## Acceptance test register
Proposed sample sizes reflect deadline feasibility and do not certify field reliability. Record input, reference, metrics, outcome, reviewer, evidence hash and failure handling for every row.

| Test | Input/reference | Proposed metric and threshold | Why / failure handling | Required evidence |
|---|---|---|---|---|
| Geographic identity/units | Real extract, bbox, known coordinate anchors; manual GIS inspection | Zero CRS swaps; all anchors in correct neighborhood; valid lengths | Location mistakes invalidate all findings; reject | GIS overlay, CRS/hash manifest |
| Completeness/connectivity | Full nodes/ways/relations; OSM referential audit | Zero unresolved road node references; critical turn gaps explicitly flagged | Referential integrity necessary, not completeness proof | Parser log and gap ledger |
| Directed routing | Hand-computed fixtures: one-way, gate, parallel edge, prohibited turn, grade separation | 100% fixture paths/reachability correct | Safety-critical semantics require exact agreement; block | Expected results written before run |
| Real route audit | At least 20 critical origin/entrance pairs independently reviewed on frozen sources | Zero forbidden movements; all reachability decisions reconciled; distance agreement within 1% against equivalent independent calculation | 1% allows geodesic/numerical variation, not missing streets; review disagreements | Route polylines, reviewer/source notes |
| Scenario causality | Identity P, closure-only, private entrance, identical proposals | Exactly zero changes for identity; no false public benefit; ties preserved | Algebraic invariants; block incorrect attribution | Graph deltas + per-origin five-state CSV |
| Closure monotonicity | Remove edges with fixed nonnegative lengths/origins/destinations | Reachability cannot improve; shortest distance cannot decrease | Fixed-graph mathematical invariant; block | Before/after traces |
| Boundary truncation | Same core origins with expanding buffers | Reachability stable; distance within 1% for audited routes between last two expansions | Stability diagnostic, not guarantee; expand or mark boundary-sensitive | Buffer manifests and comparison |
| Common-cause failures | Two edge-disjoint routes through one bridge/junction/work-zone group | Group removal removes both as expected; zero false independence labels | Prevents topological redundancy overclaim | Group-to-edge manifest and failures |
| Mode conflict | Vehicle-helping candidate that blocks pedestrian link | Conflict always visible; never label universally safer | Must preserve mode-specific harm; reject or expose tradeoff | Both mode result distributions |
| Intervention validity | Unknown permit, nonexistent road, conflicting sequence, no candidate | 100% invalid candidates excluded from implementable mode; no-option preserved | Permission/geometry hard gate; block | Candidate ledger + exclusion reason |
| Community distribution | Frozen origins; connected/disconnected and worst-affected examples | 100% origins accounted for, including unknown/unreachable; worst case retained | Avoid favorable-only averages; fail incomplete report | Origin sampling rationale and full results |
| Uncertainty ranking | Toggle each material unknown access/turn state | Same winner under admissible assumptions, or RANKING_UNSTABLE | Confidence needs robustness; withhold confident ranking | Scenario grid and ranking flips |
| Optimizer correctness | Small candidate sets with hand/exhaustive oracle | Feasible set and optimum match exactly; equal options tie | Exact finite search benchmark; block incorrect optimum | Enumeration and constraint logs |
| Optimizer scale | Proposed upper workload: 1,000 origins, 10 facilities, <=8 binary candidates, 10 disruption groups | Measured p50/p95; proposed p95 <=30 s, peak RAM <=2 GB on named machine | Explicit practical envelope; reduce scope if failed, never hide timeout | Hardware/config/run logs; NOT_TESTED |
| AI grounding/hallucination | Frozen 40-case corpus from AI plan | Zero material false released claims; 100% ID/scope/unit validation | Release safety gate; disable AI on failure | Raw inference/tool/assertion logs |
| App reliability | 20 complete local runs, forced failure/cancel | 20/20 accurate completion or explicit failure; no stale run mixing | Small smoke target; investigate all failures | Run IDs/error traces |
| Offline demo | Disconnect network with cached licensed data and no model | Entire deterministic workflow/report works; AI honestly unavailable/replay labeled | Reproducible deadline demo; fail dependency surprises | Offline execution log |
| Upload/access security | Oversize/invalid files, zip traversal, unauthorized edits, injected notices | All supplied attacks rejected; no client key/private-plan disclosure | Bounded security suite, not penetration certification | Request/result logs and disclosure audit |
| Report reproducibility | Same bytes/config/version rerun by independent reviewer | Exact deterministic metric equality after defined rounding; matching input hashes | Requires repeatability; investigate platform differences | Commands, manifests, report-to-API diff |

## Disproof experiments
1. P identity produces no community benefit: accept the null result.
2. Proposed development does not change the tested road network: retract development-impact claim.
3. Route improvement disappears when an uncertain private road is excluded: reject robust-benefit claim.
4. Mitigation worsens a pedestrian community or shifts detours to another origin: show the tradeoff.
5. Expanded boundary removes apparent isolation: initial result was truncation artifact.
6. Common bridge fails both supposed alternatives: retract physical-independence claim.
7. No approved candidate beats baseline: output no verified improvement.
8. AI performs worse than deterministic template: disable it.
9. Independent reviewer cannot reproduce a result: gate stays failed.
10. No local practitioner finds the workflow useful: adoption hypothesis remains unsupported.

## Ground truth hierarchy
Synthetic fixtures establish algorithm semantics only. Authentic snapshots establish recorded geography only. Independently reviewed movements/entrances establish limited geographic plausibility. Authority plans establish documented restrictions, not compliance on the ground. Field observations can validate current conditions, not future safety outcomes. Do not combine these into a single invented accuracy percentage.

