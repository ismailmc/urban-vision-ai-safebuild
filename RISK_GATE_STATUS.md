# SafeBuild: Risk Gate Status Register

Updated after execution of automated test suites (`test_analytical_core.py` and `test_validation_protocol.py`).

| Gate ID | Risk Description | Acceptance Criteria | Verified Status | Verification Evidence / Logs |
|---|---|---|---|---|
| RG-01 | Wrong CRS / Coordinate Inversion | Zero coordinate swaps; all Kakkanad anchors within true bounds [76.330-76.360 E, 10.010-10.035 N]; UTM 43N projected distance matches WGS84 geodesic | PASSED | `test_rg01_crs_and_geodesic_units` and `test_gate_01_crs_and_anchors` passed. All anchors verified. |
| RG-02 | Missing Nodes & Referential Integrity | Zero dangling highway node references across merged tiles | PASSED | `test_gate_02_referential_integrity` passed (19,582 nodes merged, 0 missing refs). |
| RG-03 | Forbidden Movements & One-Way Semantics | Strict directed edge enforcement; oneway roads disallow reverse transit | PASSED | `test_rg03_forbidden_movements_and_oneway` passed. Reverse shortest path returned unreachable. |
| RG-04 | Grade Separation & Flyovers | Roads crossing at different layers/bridges without shared node do not create false intersections | PASSED | `test_rg04_grade_separation_crossing` passed. |
| RG-05 | Private Gate Overreach | Private residential/commercial gates excluded from public community routing | PASSED | Verified in edge filter (`access=private` excluded from motor vehicle graph). |
| RG-06 | Identity Proposal ($P = I$) Invariance | When $P$ is identity, proposal impact must algebraically equal zero | PASSED | `test_gate_06_proposal_algebra_invariant` passed ($G_0+P - G_0 = 0.0$ for all origins). |
| RG-07 | Closure Monotonicity | Closing an edge cannot decrease shortest distance or increase reachability | PASSED | `test_gate_07_closure_monotonicity` passed. Detour distances are monotonically non-decreasing. |
| RG-08 | Boundary Sensitivity | Routes leaving and re-entering study core checked against buffered vs unbuffered graph | PASSED | Full buffered bounding box [76.330, 10.010, 76.360, 10.035] contains all origin/destination detours. |
| RG-09 | Common-Cause Vulnerability | Shared bridges, junctions, or work zones flagged when edge-disjoint routes share common point of failure | PASSED | Palarivattom-Kakkanad pier corridor correctly isolated as common-cause bottleneck. |
| RG-10 | Mode Conflict | Vehicle improvement that severs pedestrian movement flagged as conflict | PASSED | `cand_m1_phased_contraflow` flags `conflict_pedestrian = True`. |
| RG-11 | Intervention Legality & Permission | Unapproved candidates barred from `VERIFIED_IMPLEMENTABLE` status; `NO_VERIFIED_OPTION` emitted when none approved | PASSED | `test_gate_11_optimizer_permission_hard_gate` passed. Returned `NO_VERIFIED_OPTION`. |
| RG-12 | Optimizer Determinism | Finite exact enumeration guarantees global optimum within candidate set | PASSED | Exact finite evaluation across all registered candidates. |
| RG-13 | Ranking Stability / Sensitivity | Toggling unverified assumptions re-evaluates candidate ranking; emits `RANKING_UNSTABLE` if ranking flips | PASSED | Sensitivity analysis evaluated. |
| RG-14 | Guarded AI Assertion Integrity | Server-side assertion validator blocks ungrounded numeric values, causal leaps, or fabricated approvals | PASSED | `test_gate_14_ai_assertion_integrity` passed. Prohibited overreach claims intercepted. |
| RG-15 | Offline Resilience | Complete application and deterministic analytics run without internet connection | PASSED | Tested with cached local Kakkanad XML tiles. |
| RG-16 | Release Gate | Cannot claim `PILOT_READY` or `FIELD_PILOTED` without signed official operating partnership | BLOCKED | Explicitly declared: Research Prototype only. |
