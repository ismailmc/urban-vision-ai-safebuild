# Competitors, prior art and falsifiable differentiation
Research 2026-10-12. This is documentation review, not hands-on product benchmarking. Sources and dates are in VERIFIED_RESEARCH_REPORT.md.

| System | Existing capability supported by inspected material | SafeBuild overlap | Implication |
|---|---|---|---|
| Autodesk Forma Site Design | Site/proposal comparison and environmental analysis | Alternative development evaluation, explainable maps | Do not describe Forma as merely a visualizer or infer absence of network analysis across its ecosystem |
| ArcGIS Urban | Scenario-based land-use/zoning and suitability analysis | Before/after planning comparisons | Scenario comparison itself is not innovation |
| ArcGIS Network Analyst | Routing, barriers/restrictions, location allocation | Accessibility and constrained decisions | Major direct overlap; optimization is already established |
| QGIS | Direction-aware shortest paths/service-area processing | Low-cost GIS reference workflow | A motivated GIS user can assemble much of the core analysis |
| UrbanSim | Land-use modeling integrated with network accessibility | Infrastructure/policy scenario indicators | Accessibility-aware planning is prior art |
| PTV Visum / broader PTV tools | Transportation modeling and construction/intervention scenario management | Closures, diversion comparisons | Do not claim existing tools lack mitigation workflows; realistic traffic modeling requires calibrated inputs |
| Bentley OpenCities Planner / digital twin ecosystem | Interactive infrastructure/city information and stakeholder communication | Maps, evidence communication and planning integration | Analytics may be added through an ecosystem; no blanket feature-absence claim |
| Eclipse SUMO | Road-permission changes and rerouting in traffic simulation | Construction scenarios | Useful optional reference; uncalibrated flow simulation is not a field measurement |
| Road vulnerability research (2014 publisher abstract) | Urban critical-link serviceability/vulnerability analysis | Critical connections, access impacts | Basic vulnerability detection is not original; full paper access/comparison remains incomplete |
| Recent critical safety link research (2025 publisher result) | Scenario-specific link importance | Hazard/criticality scoring | Further review needed; no novelty conclusion from abstract alone |

Primary links:
- https://blogs.autodesk.com/forma/2026/08/28/forma-site-design-tools-overview/
- https://doc.esri.com/en/arcgis-urban/latest/help/help-scenarios.html
- https://doc.esri.com/en/arcgis-urban/latest/help/help-suitability.html
- https://doc.esri.com/en/arcgis-pro/latest/arcpy/network-analyst/locationallocation.html
- https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/networkanalysis.html
- https://cloud.urbansim.com/docs/general/documentation/travel%20model%20integration.html
- https://www.ptvgroup.com/en/products/ptv-visum
- https://help.opencitiesplanner.bentley.com/index.html%40p%3D8662.html
- https://eclipse.dev/sumo/docs/Simulation/Routing.html
- https://www.sciencedirect.com/science/article/pii/S0966692314001392
- https://doi.org/10.1016/j.jnlssr.2025.100275

## Strongest defensible hypothesis
SafeBuild packages **source-linked change attribution, surrounding-resident impact distribution, common-cause access failures and permission-gated alternative comparison** into one small review workflow for construction planning.
This is a proposed integration/usability advantage. It is not proven unique, a patented invention, or a new shortest-path algorithm.

Smallest meaningful improvement: every candidate result exposes (a) exact affected origins, (b) source-backed edge changes, (c) access/permission status, (d) mode conflicts, (e) whether its ranking survives missing-road-attribute assumptions. The report must allow “no verified option” and a tied/unchanged result.

## Decision benchmark to run
Same frozen road snapshot, origin/facility entrances, restrictions and intervention registry for all methods:
1. Manual GIS analyst with QGIS and a prepared evidence spreadsheet.
2. Deterministic SafeBuild report without LLM.
3. Same engine plus AI analyst.
4. Simple heuristic: preserve the highest-centrality candidate connection; compare against exact finite enumeration.

Predeclare task: identify development vs construction impact, select or reject an alternative, and explain worst affected community under the same constraints.
Collect task completion time, factual/causal errors, missed infeasible options, correctly identified worst origins and reproducibility. Use counterbalanced tasks if multiple reviewers are available; a single reviewer is formative feedback, not statistically representative usability proof.
Proposed success: equal mathematical correctness, no additional material errors, and at least 20% lower median review time in the small task study. The 20% is a practical target, not measured evidence or literature benchmark. Report all task times and failures, not a claim of general municipal efficiency.

## Disproof
If the manual workflow is equally convenient, AI contributes no detectable benefit, or recommendations fail permission/uncertainty checks, narrow the claim to reproducible scenario reporting. Do not compensate by adding more features.

