# Implementation-ready research handoff
This is a research handoff, not another generic build prompt. Current v4 blueprint remains the acceptance contract.

## Frozen decisions
- Create only a separate SafeBuild repository; original UVAI remains untouched.
- Primary provisional pilot core: WGS84 bbox [76.335,10.015,76.355,10.030], Kakkanad.
- Fallback: Pune core [73.900,18.548,73.945,18.575].
- Start with resident-to-essential-destination distance/reachability.
- Real infrastructure context: KMRL Phase II. **No verified official closure or road-development graph delta supplied.**
- Initial public scenario label HYPOTHETICAL_CONSTRUCTION_ACCESS_REVIEW_ON_REAL_ROADS.
- Genuine AI only after engine tests: read-only selected hosted model, claim-object validation. No predictive infrastructure ML.

## Verified inputs supplied
1. Three authentic small OSM XML samples under evidence/ and counts in inspection JSON. These are sample audits, not full routable pilot snapshots.
2. Kochi AIIB project assessment PDF downloaded; source/date in report.
3. DATASET_INVENTORY.csv contains exact access routes and status.
4. Official source/evidence table in VERIFIED_RESEARCH_REPORT.md.
5. Independent acceptance-test design in VALIDATION_PROTOCOL.md.
6. Candidate strategy in PILOT_SITE_EVIDENCE.md and VALIDATION_PROTOCOL.md.

## First concrete work
A. Retrieve full buffered PBF using provided reproducible commands; archive URL, time, checksum, CRS and relation audit. Do not reuse regional “latest” URL as a fixed version without storing bytes/hash.
B. Assign a reviewer to critical movements and facility entrances. Record unknowns explicitly. Build separate pedestrian/vehicle profiles.
C. Freeze origins before seeing results, using verified public settlement/entrance locations. Population raster optional; report equal-origin weighting until a licensed raster is actually loaded.
D. Route tiny hand-computed graphs and independent real reviewed routes. Validate restricted turns and grade separation; do not equate crossing lines with junctions.
E. Implement G0, G0+C, G0+P, G0+P+C, G0+P+C+M. P must remain identity unless there is an explicitly sourced or explicitly hypothetical public-network delta.
F. Register externally specified interventions; permission UNKNOWN excludes “verified implementable” mode. Preserve no-option output. Do not invent road geometry.
G. Export exact data/provenance/uncertainty before adding AI.

## Required input contracts
Road: source_id, osm_way_id, edge_id, direction, geometry, length_m, mode, access_status, turn_state, grade/layer, snapshot_hash.
Restriction: source_document/page/span, edge_ids, start/end, mode, direction, authority_status, observed_or_hypothetical, reviewer.
Facility: operator_source, entrance geometry, modes, service_type, verified_on, reviewer.
Candidate: geometry/delta, phase, affected_modes, physical_status, owner_status, permission_status, cost_status/range/source, dependencies, incompatibilities, reviewer.
Run: immutable input hashes, config/version, graph deltas, origins/destinations, failed/unknown counts, completeness status and deterministic metrics.

## Stop conditions
No full graph or legal data route: stop metric claims.
Unsupported critical movement: uncertainty warning or refuse, never assume public access.
No real closure: label hypothesis, not actual restriction.
No development delta: no development-attributable change claim.
No lawful/physical intervention: NO_VERIFIED_OPTION.
Timeout: INCOMPLETE_ANALYSIS; no optimal recommendation.
AI unavailable/fails: deterministic core only.
No independent review/permission/partner: do not claim FIELD_PILOTED or PILOT_READY.

## Evidence outputs expected from implementation
Actual test commands/results, five-state per-origin CSVs, independent reviewed routes, candidate status ledger, buffer/sensitivity tests, worst-community and mode-conflict results, AI raw eval logs, performance measurements, disclosure audit and release gate status. Default tests to NOT_TESTED. Research counts are not routing accuracy results.

