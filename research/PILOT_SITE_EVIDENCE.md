# Pilot selection and documented case
Date 2026-10-12. Coordinates below are **proposed research boundaries**, not official project extents or surveyed limits. WGS84, latitude/longitude; bbox commands use longitude/latitude.

## Comparable candidates
| Item | Kochi urban region: Kakkanad | Bengaluru: Hope Farm/Kadugodi | Pune: Ramwadi/Viman Nagar |
|---|---|---|---|
| Proposed core bbox south,west,north,east | 10.015,76.335,10.030,76.355 | 12.980,77.745,13.000,77.775 | 18.548,73.900,18.575,73.945 |
| Proposed center lat,lon | 10.0225,76.3450 | 12.9900,77.7600 | 18.5615,73.9225 |
| Road source | OSM API; Geofabrik southern zone | Same southern zone | OSM API; Geofabrik western zone |
| Download/formats | XML bbox sample inspected; PBF/SHP/GPKG regional catalog | XML sample inspected; regional formats listed | XML sample inspected; regional formats listed |
| Sample bbox W,S,E,N | 76.340,10.020,76.350,10.025 | 77.754,12.987,77.764,12.992 | 73.920,18.557,73.930,18.562 |
| Sample measured highway ways | 100 | 101 | 227 |
| Connectivity evidence | All road node references present in sample; full directed graph not checked | Geometry present; topology/direction not audited | Geometry present; topology/direction not audited |
| Planning evidence | KMRL SIA, EIA/EDDR index; AIIB assessment downloaded | Secondary Hope Farm underpass reporting; official searchable references insufficient for geometry | Official Metro reports index lists Ramwadi–Wagholi DPR and wider assessments |
| Road-restriction records | Traffic plan existence documented; exact dated orders not obtained | No inspected authoritative edge-level order | No inspected authoritative edge-level order |
| Essential services | Sunrise address independently sourced from operator; entrance remains unresolved | OSM POIs available in principle; independently audited destination list not assembled | Same limitation |
| Infrastructure context | Existing Palarivattom–Kakkanad and Seaport–Airport roads observed in sample names; Phase II corridor documented | Junction/underpass context reported; current project status not independently verified | Extension planning documented; approved construction phasing unverified |
| License | OSM ODbL; planning documents publicly readable but no open republication license established | OSM ODbL; news copyright; avoid republication | OSM ODbL; official reports not assumed open-license |
| Last known update | OSM regional snapshot 11 Oct 2026; SIA 19 Jun 2023; AIIB 28 Aug 2024 | Same OSM snapshot; secondary construction report 26 May 2026 | Regional OSM snapshot 11 Oct 2026; index publication chronology unspecified |
| Practical advantage | Strongest inspected primary evidence; Kerala-based team may arrange local verification, subject to actual ability | Matches original preferred area | Strong official planning-document repository |
| Practical disadvantage | Exact closure geometry and municipality/authority scope need confirmation | Weakest authoritative project geometry found in this search | Documents large; remote local verification not arranged |
| Critical unknown | Permitted movements, current barriers, facility entrances, reviewer | Same plus approved design | Same plus detailed local phase plan |

**Primary recommendation: Kakkanad. Fallback: Pune.** The judgment prioritizes inspectable primary case evidence, not larger sample counts. Bengaluru remains an option if a dated official design/diversion order becomes available. No candidate's completeness has been proven. Do not represent these three as an exhaustive Indian city ranking.

## Authentic planning case
- Title: Kochi Metro Rail Project, Phase II, JLN Stadium–Infopark via Kakkanad.
- Responsible implementing authority: KMRL; AIIB is the inspected lender/source, not a road-closure approving body.
- Primary document: AIIB Project Summary Information, 28 Aug 2024:
  https://www.aiib.org/en/projects/details/2024/_download/India/AIIB-PSI-P000795-India_Kochi-Metro-Rail-Phase-II-v.8.pdf
- Supporting document: KMRL station land-acquisition SIA, 19 Jun 2023:
  https://kochimetro.org/wp-content/uploads/2023/09/Phase%20II-Stations-Kochi%20metro%20stations%20English.pdf
- The AIIB summary establishes a real infrastructure corridor, civil-work traffic/community risks and an existing traffic-management plan. It does not establish current closures, permissible diversion edges, exact operating dates or modeled accessibility losses.
- The SIA establishes station-acquisition context and identifies Kochi Corporation/Thrikkakara municipality jurisdiction along different parts of the corridor. Verify jurisdiction of the chosen parcel/road; do not send every Kakkanad issue to Kochi Corporation.
- Candidate road segments: Palarivattom–Kakkanad Road and the Seaport–Airport Road junction approaches, present in the downloaded OSM sample. Exact relevant way IDs and direction-specific restriction extents still need a signed-off mapping.
- Proposed changes: infrastructure alignment/station works documented at project level. Changes to the **public road graph** are not established merely by the metro project existing.
- Current October 2026 barrier configuration and construction sequence: UNKNOWN.
- Document reuse: link/cite public documents; do not publish acquisition tables with household names or assume reuse permission for drawings.

## Honest fallback scenario
Label: **HYPOTHETICAL_CONSTRUCTION_ACCESS_REVIEW_ON_REAL_ROADS**.
Use a frozen, audited road graph. A reviewer chooses explicit existing edge IDs for a modeled construction restriction and defines two assumed closure sequences. Do not call them official diversions.
If no development road delta is supported, set P = identity. The result may demonstrate construction impact but must not claim permanent development-attributable vulnerability. The five states can legitimately include identical states.
No actual closure event is established by this report. No active emergency navigation should be provided.

## What turns this into a documented planning pilot
Obtain dated traffic-management drawing/order, permitted movement schedule, verified essential facility entry points and reviewer consent. Map the source's road names/endpoints to OSM IDs manually; log ambiguities, drawing scale and source date. Obtain corrections from the competent traffic/roadwork authority before marking movements verified.

## Data retrieval
Inspected small Kochi extract:
https://api.openstreetmap.org/api/0.6/map?bbox=76.34,10.02,76.35,10.025
The included sample is smaller than the proposed pilot. It is NOT a sufficient graph for route-distance comparisons.

For a full pilot, retrieve PBF and extract a buffered area with Osmium, preserving complete ways and restrictions. Prefer PBF over converted SHP for relation-aware routing. Follow public service limits:
```bash
curl -L https://download.geofabrik.de/asia/india/southern-zone-latest.osm.pbf -o southern.osm.pbf
osmium extract --bbox 76.29,9.97,76.40,10.08 --strategy complete_ways southern.osm.pbf -o kochi_buffer.osm.pbf
osmium fileinfo -e kochi_buffer.osm.pbf
sha256sum kochi_buffer.osm.pbf
```
These commands were **not run**. The buffer is an initial proposal, not a verified sufficient extent; expand and test convergence. Full relation handling must be checked, not assumed from complete ways.
Overpass public endpoint returned HTTP 406 in this session; alternative endpoint timed out. The OSM map API succeeded for small samples. That does not establish that Overpass is generally unavailable.

