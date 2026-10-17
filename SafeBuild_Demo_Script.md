# SafeBuild 2–3 Minute Evaluation & Demonstration Script

**Urban Vision AI — SafeBuild**  
*“Plan roadwork. Keep communities connected.”*  
**Corridor Pilot:** Kakkanad Metro Phase II Corridor (Sunrise Hospital Access)  
**Total Duration:** ~2 Minutes 30 Seconds  

---

## Demonstration Overview

This script guides an evaluator, municipal planner, or reviewer through the live SafeBuild prototype. The workflow follows four clear, logical steps:
1. **Define Work:** Select a road corridor and configure a hypothetical restriction.
2. **Check Access:** Compute deterministic routing detours to essential healthcare destinations.
3. **Compare Arrangements:** Audit candidate construction sequences under strict statutory gates.
4. **Export Plan:** Download auditable CSV data and tamper-evident PDF reports.

---

## Script Walkthrough & Narration

### Segment 1: Introduction & Study Area Context (0:00 – 0:35)
* **Screen State:** Open `http://localhost:3000/`. The MapLibre map renders the Kakkanad study area (19,582 authentic OSM nodes, 11,675 highway edges).
* **Click Action:** Click `Try the Kakkanad example` in the header or task workflow bar.
* **Spoken Narration:**
  > “Welcome to SafeBuild. Major infrastructure works—like metro rail viaduct construction—often sever connections between neighborhoods and critical community destinations. Planners need to know: if this road is restricted during construction, how does community access change, and would another arrangement help?
  > Here in the Kakkanad pilot corridor in Kochi, we are analyzing proposed metro construction along the Palarivattom–Kakkanad arterial, evaluating access to Sunrise Hospital from seven residential cluster anchors.”

---

### Segment 2: Define Work (Step 1) (0:35 – 1:05)
* **Screen State:** Left panel displays **Step 1: Choose a Road**.
* **Click Action:**
  1. Inspect the selected segment: `Palarivattom - Kakkanad Road` (OSM Way ID `197827530`).
  2. Toggle between `Motor Vehicle` and `Pedestrian` travel mode.
  3. Expand `Direction & Phase Settings` to view closure direction (`Both Directions`) and phase assignment (`Phase 1: Civil Pier Foundation`).
  4. Note the yellow pill label: `Hypothetical Restriction (Research Model)`.
* **Spoken Narration:**
  > “In Step 1, planners choose any road on the authentic OSM network to restrict. SafeBuild models this connection as restricted during construction. Planners can set directionality, travel mode, and construction phasing. Notice that unverified closures are clearly labeled as hypothetical research models to prevent premature public confusion.”

---

### Segment 3: Check Access (Step 2) (1:05 – 1:40)
* **Screen State:** Click the green button `Next: Check Community Access` (or tab `2. Access`).
* **Click Action:**
  1. Primary action button: Click `Check impact`.
  2. The system executes a live Dijkstra shortest-path recalculation on the restricted graph G0_C.
  3. Observe the modeled impact metrics:
     * **Sampled Points Affected:** 3 of 7 anchors.
     * **Newly Unreachable Points:** 0 (all anchors retain connected bypasses).
     * **Largest Modeled Distance Increase:** +354.9 m (+22.6% over baseline) at Kakkanad West / Civil Station Environs.
  4. Click through the sampled community anchors in the list (e.g., `Kakkanad West`, `Padamugal`, `DLF City`) to watch the pink detour route highlight on the map.
* **Spoken Narration:**
  > “In Step 2, SafeBuild runs deterministic Dijkstra shortest-path calculations across all origins to the ground-surveyed Sunrise Hospital entrance. 
  > Notice what the numbers show: restricting the main arterial increases the travel distance for Kakkanad West by 354.9 meters—a 22.6% increase over baseline. Western and central neighborhoods are forced onto narrower collector streets, while eastern anchors like DLF City remain largely insulated.”

---

### Segment 4: Compare Another Arrangement (Step 3) (1:40 – 2:15)
* **Screen State:** Click `Next: Compare Another Arrangement` (or tab `3. Compare`).
* **Click Action:**
  1. Select `Single-Lane Managed Contraflow & Signal Priority` (Candidate M1).
  2. Click `Compare “Single-Lane...”`.
  3. Inspect the Tradeoff Review cards:
     * **What Improves:** Recovers 174.5 m arterial access via flaggers.
     * **What Worsens:** Sidewalk width narrowed below 1.5 m, creating pedestrian & worker exposure.
     * **What Stays Unchanged:** Eastern anchors remain unaffected.
  4. Point to the amber statutory gate box: `STATUTORY GATE: NO_VERIFIED_OPTION`.
* **Spoken Narration:**
  > “Now in Step 3, the planner asks: would another arrangement help? We compare candidate sequencing options. Arrangement B restores one managed lane through the workzone, reducing the detour by 174 meters. But look at the tradeoff: it compresses pedestrian sidewalks below 1.5 meters.
  > Most importantly, look at the statutory gate: SafeBuild outputs `NO_VERIFIED_OPTION`. Under municipal law, no automated tool can grant formal clearance without signed approval from the Kerala State Traffic Police and KMRL safety inspectors. SafeBuild protects against false authority.”

---

### Segment 5: Evidence Audit & Export (2:15 – 2:30)
* **Screen State:** Top navigation bar actions.
* **Click Action:**
  1. Click `Evidence & Advanced` to open the full Provenance Inspector modal (showing Run ID, EPSG:4326/EPSG:32643 projections, checksums, and non-emergency disclaimers).
  2. Close the modal, then click `Download Report` to obtain the official PDF decision report.
* **Spoken Narration:**
  > “Finally, every metric in SafeBuild is backed by a full provenance audit trail. With one click, planners can inspect dataset checksums or export an auditable PDF report ready for municipal review. SafeBuild plans roadwork while keeping communities connected.”
