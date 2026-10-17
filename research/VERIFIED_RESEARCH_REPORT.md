# SafeBuild: verified research and readiness decision
Research date: 12 October 2026. Decision: **CONDITIONAL GO for a narrow research prototype; NO-GO for claims of a validated municipal pilot today.**

## What was actually done
Official web pages, planning documents, data catalogs and model documentation were inspected. Small OSM XML extracts for Kochi, Bengaluru and Pune were downloaded and parsed. An AIIB project assessment PDF was downloaded. No routing experiments, AI inference, field inspection, intervention approval, practitioner interview or software deployment occurred.

The current v4 blueprint and development prompt were read for compatibility. This research supplements their evidence requirements; it does not mark their release gates passed. The original Urban Vision AI application was not modified.

Evidence classes: VERIFIED FACT = inspected source statement; MEASURED RESULT = direct file inspection; MODEL OUTPUT = an executed analytical calculation (none yet); HYPOTHETICAL SCENARIO = explicitly assumed graph change; RECOMMENDATION = proposed work; UNRESOLVED ASSUMPTION = not established.

## Main decisions
1. Primary: a small **Kakkanad junction / Palarivattom–Kakkanad Road / Seaport–Airport Road** study in Kochi's urban region. This is a provisional evidence-based choice, not proof that Kochi has the most complete roads in India. KMRL and AIIB provide a stronger inspected project-evidence chain than the Bengaluru candidate.
2. Fallback: **Pune Ramwadi–Viman Nagar approach**, connected to the documented Ramwadi–Wagholi extension. Large project PDFs and exact construction restrictions still need inspection.
3. Use resident-to-essential-destination **route distance and reachability**, not real emergency response times, congestion forecasts or accident predictions.
4. Include a read-only, evidence-grounded AI analyst after the deterministic engine passes. Postpone Notice-to-Network until an authentic, independently annotated restriction corpus exists.
5. Evaluate finite, externally specified access/closure-sequencing alternatives. No invented roads, permissions, implementation costs or guaranteed winner.
6. Demonstrate real roads with hypothetical restrictions unless dated official segment-level restrictions and usable plans are obtained.

## Pilot comparison
See PILOT_SITE_EVIDENCE.md for boundaries, datasets, missing evidence and selection rationale. All three candidates have inspectable OSM geometry. None has established complete legal access or turn restrictions. Comparing raw object counts does not compare completeness: the boxes differ and ways may extend outside them.

## Measured evidence
Kochi small sample, bbox west/south/east/north = 76.340,10.020,76.350,10.025:
- 1,488 nodes; 212 total ways; 100 highway-tagged ways.
- Eight highway ways explicitly carry a one-way tag; zero carry an access tag.
- Zero restriction relations returned; zero missing highway node references.
- These are tag-presence counts, not routing accuracy or true access completeness.
Bengaluru sample: 2,320 nodes and 101 highway ways. Pune sample: 6,086 nodes and 227 highway ways. Files and inspection manifests are included. No facility-completeness score was measured.

## Competition requirements
The current south-zone portal lists the submission window through **24 October 2026**. The earlier AICTE circular dated 18 September lists 7 October; current portal and orientation agree on 24 October. No later extension was established. The closing time/timezone was not published in inspected material; aim to finish 23 October.

The circular permits undergraduate participation, software under Track A, and AI as an enabling tool. It requires institution/SPOC submission and **one idea per theme per institute**. The supplied orientation states teams of 2–5 and up to five teams, with required problem/solution/impact fields of 500/1,000/500 words, plus a mandatory concept-note PDF up to 10 MB; supporting documents and video are optional. These orientation rules were inspected, but the authenticated live form was not accessed.

Theme conflict: orientation/AICTE annexure frame Surakshit Bharat around mobility, road safety and cyber security; the live theme page uses mobility and infrastructure, security and resilience, and digital public infrastructure for undergraduates. SafeBuild fits mobility/infrastructure, but copy the actual dashboard option instead of assuming a category label.

Existing-idea eligibility, prior hackathon submissions, detailed IP ownership terms and any AI-development disclosure rules remain unverified. The portal mentions IP guidance, which is not an ownership agreement. Ask the SPOC/support. Keep SafeBuild separately developed and disclose its relationship to the earlier project.

## Source–evidence register
All sources accessed 2026-10-12. “Accessible” refers to the stated source route; it does not mean every associated dataset file was downloaded. Publication/upload dates are not interchangeable.

| Claim | Source | URL | Publication/update date | Verification status | Limitations |
|---|---|---|---|---|---|
| Current south-zone deadline, Open-level prototype expectation | SFIC portal | https://sevafirst.mic.gov.in/ | Undated live page | VERIFIED FACT | Authenticated submission not inspected; schedule sections differ on finale |
| Current undergraduate theme wording | SFIC themes | https://sevafirst.mic.gov.in/themes | Undated | VERIFIED FACT | Differs from orientation labels |
| Institution-led process | SFIC participation | https://sevafirst.mic.gov.in/participate | Undated | VERIFIED FACT | No live roster checked |
| One idea/theme/institute; AI permitted; older deadline | AICTE circular | https://www.aicte.gov.in/sites/default/files/Circular_%20Seva%20First%20Innovation%20Challenge.pdf | 18 Sep 2026 | VERIFIED FACT | Older deadline superseded operationally by live window; other rules need SPOC confirmation |
| Team and form limits | Supplied orientation, pp31–38 | https://sevafirst.mic.gov.in/ | PDF supplied: Seva_First_Challenge_Orientation.pdf; version date unspecified | VERIFIED IN SUPPLIED FILE | URL is portal, not a claimed PDF download link; no authenticated form check |
| Kochi Phase II project and construction traffic/community risk; traffic plan exists | AIIB PSI | https://www.aiib.org/en/projects/details/2024/_download/India/AIIB-PSI-P000795-India_Kochi-Metro-Rail-Phase-II-v.8.pdf | 28 Aug 2024 | VERIFIED; PDF downloaded | Does not supply dated edge-level closures or certify proposed diversions |
| Station land acquisition; geographic jurisdiction | KMRL SIA | https://kochimetro.org/wp-content/uploads/2023/09/Phase%20II-Stations-Kochi%20metro%20stations%20English.pdf | 19 Jun 2023 | VERIFIED; PDF text inspected | Historical project document; no contemporary traffic order |
| EIA/EDDR public access links | KMRL | https://kochimetro.org/phase-ii-eia/ | Undated | VERIFIED INDEX | Linked files failed in web retrieval; full contents not inspected |
| Kochi revised DPR exists in search listing | KMRL | https://kochimetro.org/wp-content/uploads/2026/06/DPR%26AAR-Kochi_Metro_Phase_II_Corridor-%20JLN_Stadium%20_to_Infopark_via_Kakkanad.pdf | Upload path Jun 2026; document chronology unverified | EXISTS; CONTENT ACCESS FAILED | Do not infer newest geometry from URL date |
| Pune DPR and impact documents are publicly listed | Maha Metro | https://www.punemetrorail.org/report | Undated live index | VERIFIED INDEX | Linked DPR01.pdf exceeded web size limit; contents not inspected |
| Bengaluru Hope Farm construction report | Times of India | https://timesofindia.indiatimes.com/city/bengaluru/finally-some-hope-after-11-year-delay-work-to-ease-traffic-on-one-of-whitefields-worst-choke-point-begins/articleshow/131332183.cms | 26 May 2026 | SECONDARY EVIDENCE | No authoritative segment geometry/traffic order established |
| Southern-zone current OSM formats and snapshot | Geofabrik | https://download.geofabrik.de/asia/india/southern-zone.html | Data through 11 Oct 2026 20:21:06Z | VERIFIED INDEX | Regional file not downloaded; current network accuracy unknown |
| Western-zone extract availability | Geofabrik | https://download.geofabrik.de/asia/india/western-zone.html | Same displayed snapshot date | VERIFIED INDEX | Regional file not downloaded |
| OSM ODbL and attribution | OSM Foundation | https://www.openstreetmap.org/copyright | Undated policy | VERIFIED | Data rights differ from tile/API service terms |
| Kochi road geometry sample | OSM API | https://api.openstreetmap.org/api/0.6/map?bbox=76.34,10.02,76.35,10.025 | Download 12 Oct 2026 | DOWNLOADED & INSPECTED | Tiny sample; access/turn completeness unverified |
| India population raster and downloadable file list | WorldPop | https://hub.worldpop.org/doi/10.5258/SOTON/WP00532 | Version 2, 2017; epochs 2010/15/20 | VERIFIED CATALOG | No raster downloaded; landing page production dates inconsistent; old modeled counts |
| GHSL population access and terms | JRC | https://human-settlement.emergency.copernicus.eu/downloadWizard.php ; https://human-settlement.emergency.copernicus.eu/faq.php | R2023A; page dates unspecified | VERIFIED ACCESS/TERMS | Exact pilot tile not selected or inspected |
| Sentinel-2 worldwide collection | Copernicus | https://dataspace.copernicus.eu/data-collections/copernicus-sentinel-missions/sentinel-2 | Collection Jul 2015–present | VERIFIED COLLECTION | No scene selected; cannot resolve permissions or all local road details |
| Bhuvan archive exists | NRSC | https://bhuvan-app3.nrsc.gov.in/data/download/index.php?c=p&g=OS&p=wstg&s=NICES | Undated | EXISTS; COVERAGE UNVERIFIED | Login shown; product coverage/terms not verified |
| Sunrise Hospital address | Hospital operator | https://www.sunrisehospitalcochin.com/contact | Undated | VERIFIED ADDRESS | Exact entrance, vehicle entry and service capability not independently verified |
| Forma environmental/site comparison | Autodesk | https://blogs.autodesk.com/forma/2026/08/28/forma-site-design-tools-overview/ | 28 Aug 2026 | VERIFIED DOCUMENTATION | Product not hands-on benchmarked |
| ArcGIS Urban scenario/suitability workflow | Esri | https://doc.esri.com/en/arcgis-urban/latest/help/help-scenarios.html ; https://doc.esri.com/en/arcgis-urban/latest/help/help-suitability.html | Current docs; version date not captured | VERIFIED DOCUMENTATION | No feature-absence claim |
| ArcGIS routing/location allocation | Esri | https://doc.esri.com/en/arcgis-pro/latest/arcpy/network-analyst/locationallocation.html | Current docs | VERIFIED DOCUMENTATION | External routing service data differs from SafeBuild snapshot |
| QGIS directed shortest-path capability | QGIS | https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/networkanalysis.html | Version 3.44 docs | VERIFIED DOCUMENTATION | Simple line network reference insufficient for complex turn restrictions |
| UrbanSim land-use and accessibility | UrbanSim | https://cloud.urbansim.com/docs/general/documentation/travel%20model%20integration.html | Docs 3.13.1 | VERIFIED DOCUMENTATION | Local calibrated India model not established |
| Construction scenario modeling | PTV | https://www.ptvgroup.com/en/products/ptv-visum | Undated current page | VERIFIED PRODUCT DESCRIPTION | Not independently tested |
| Digital-twin communication | Bentley | https://help.opencitiesplanner.bentley.com/index.html%40p%3D8662.html | Undated guide | VERIFIED DOCUMENTATION | Custom analytics may extend capabilities |
| Closures/rerouting simulation | Eclipse SUMO | https://eclipse.dev/sumo/docs/Simulation/Routing.html | Current docs | VERIFIED DOCUMENTATION | Demands/calibration needed for realistic flow estimates |
| Existing road vulnerability research | Publisher abstract | https://www.sciencedirect.com/science/article/pii/S0966692314001392 | 2014 | SEARCH-ACCESSIBLE ABSTRACT; FULL OPEN FAILED | Full methodological comparison incomplete |
| Runtime model capability and pricing | Google | https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite ; https://ai.google.dev/gemini-api/docs/pricing | Model page 30 Jul 2026; current pricing | VERIFIED DOCUMENTATION | No credential/account quota or inference test |
| Structured JSON generation | Google | https://ai.google.dev/gemini-api/docs/structured-output | Current docs | VERIFIED DOCUMENTATION | Schema compliance is not factual correctness |
| KMRL contact route | KMRL | https://kochimetro.org/contact-us/ | Undated live page | VERIFIED CONTACT CHANNEL | No contact attempted; no partner commitment |

## Final feasibility assessment
Problem significance: supported by official construction/community-impact assessment, but local accessibility loss has not been measured.
Distinctiveness: a plausible workflow hypothesis, not a novel routing algorithm or established first-of-kind invention.
Data: authentic geometry accessible; lawful/public planning evidence exists; critical movement permissions remain missing.
Engineering: testable with frozen graphs, independently checked movements and five-state attribution; not yet validated.
AI: actual inference is feasible in documented APIs, but value must beat a deterministic report baseline.
Interventions: can be screened, but none is verified implementable today.
Adoption: a planner might use a reproducible access review attached to a traffic-management discussion; demand remains untested.
Deadline: narrow prototype plausible under a gated schedule, not guaranteed; see deployment plan.
Truthful current claim: “We have identified an official infrastructure case and inspected authentic road samples; the analytical prototype and field validation are pending.”
Postpone traffic prediction, flood prediction, autonomous planning, live digital twins, citywide deployment and predictive safety ML.

