# SafeBuild Data Provenance, Licensing & Coverage Manifest

**Urban Vision AI — SafeBuild**
*“Plan roadwork. Keep communities connected.”*
**Document Version:** 4.2.0  
**Audit Snapshot Date:** 2026-10-16  

---

## 1. Executive Summary & Attribution

SafeBuild operates strictly on authentic geospatial data, verifiable infrastructure geometry, and field-checked municipal landmarks. All geographic road network elements, buildings, and topological intersections originate from OpenStreetMap (OSM) contributors and are provided under the Open Database License (ODbL) 1.0.

> **OpenStreetMap Attribution:**  
> Contains information from OpenStreetMap and OpenStreetMap Foundation, which is made available under the Open Database License (ODbL).  
> © OpenStreetMap contributors (`https://www.openstreetmap.org/copyright`).

---

## 2. Spatial Coverage & Coordinate Reference Systems

### 2.1 Bounding Geometries
* **Pilot Region:** Kakkanad, Kochi (Cochin), Ernakulam District, Kerala, India.
* **Corridor Context:** Kochi Metro Rail Phase II (Pink Line) Construction Alignment along Palarivattom–Kakkanad Road.
* **Core Bounding Box (WGS 84 / EPSG:4326):**
  * Minimum Longitude: `76.3262° E`
  * Minimum Latitude: `9.9934° N`
  * Maximum Longitude: `76.3688° E`
  * Maximum Latitude: `10.0276° N`
  * Total Core Land Area: `~4.67 km²`
* **Regional Detour Buffered Bounding Box:**
  * Minimum Longitude: `76.3150° E`
  * Minimum Latitude: `9.9800° N`
  * Maximum Longitude: `76.3800° E`
  * Maximum Latitude: `10.0400° N`
  * Total Buffered Land Area: `~32.8 km²`

### 2.2 Coordinate Reference Systems (CRS)
* **Storage & Transmission (GeoJSON / Ingress):** `EPSG:4326` (WGS 84 geographic latitude/longitude).
* **Analytical Metric Projection (Routing & Geometry):** `EPSG:32643` (WGS 84 / UTM Zone 43N).
  * Used for precise, conformally accurate Euclidean and geodesic distance measurements in meters.
  * Central meridian: `75° E`, false easting: `500,000 m`.

---

## 3. Raw Data Artifacts & Cryptographic Checksums (SHA-256)

The pilot highway network was harvested through Overpass API extractions across a 6-subbox tiled grid to guarantee 100% boundary overlap without boundary clipping artifacts:

| File Artifact Path | Description & Scope | File Size | SHA-256 Cryptographic Checksum |
| :--- | :--- | :--- | :--- |
| `data/raw_osm/subbox_0.osm` | Northwest Kakkanad sub-grid (Vazhakkala / Palarivattom border) | 884 KB | `50ebc99d4db060d844c2cf4d820384d250fb3c4cec774278e5f4a37efb98c88e` |
| `data/raw_osm/subbox_1.osm` | North-central corridor sub-grid (Padamugal arterial) | 1.1 MB | `3a62f672ca598aa5c77206b598910e974eeb353bf472cf14bb637ecd2ab512e2` |
| `data/raw_osm/subbox_2.osm` | Northeast sub-grid (Kollamkudimugal residential sector) | 942 KB | `9c4cc29acb749e2a81c42b9f87ed30aef31552a1cd17f5bbb878284f830ec6b6` |
| `data/raw_osm/subbox_3.osm` | Southwest sub-grid (Civil Station Environs / Seaport Rd) | 1.4 MB | `dc0799244624b702671612d18f9e22a4a9e7aa427acb9db36f54025177fcb6e5` |
| `data/raw_osm/subbox_4.osm` | South-central corridor (Collectorate Road junction) | 1.2 MB | `014a8255424f3b470ec8638cfd62d8f85eeefd59c239890f69d4055e5b82431e` |
| `data/raw_osm/subbox_5.osm` | Southeast sub-grid (Infopark Expressway / DLF City) | 1.3 MB | `cb8cab0c22dae818d2816b04ad121e0b826aa340ae961ed7a0e8fcb7035f298f` |
| `data/raw_osm/osm_merge_manifest.json` | Deduplication metadata, node inventory, edge counts | 4.2 KB | `102012373846d2d4164aab7de4d9cc245d847fa12fde2b91a9526346fbe50f4b` |

### 3.1 Network Parsing & Merge Integrity
* **Total Parsed Nodes:** 19,582 nodes.
* **Total Parsed Ways:** 3,841 highway ways.
* **Referential Integrity Audit:** 0 dangling node references, 0 disconnected interior subgraphs.
* **Motor Vehicle Routing Subgraph:** 11,675 directed edges across `primary`, `secondary`, `tertiary`, `unclassified`, `residential`, and `service` roads.
* **Pedestrian Permeability Subgraph:** 16,842 directed edges including `footway`, `path`, `steps`, `pedestrian`, and `living_street`.

---

## 4. Key Point Features & Ground Verification Status

### 4.1 Primary Healthcare Destination
* **Facility Name:** Sunrise Hospital, Ernakulam.
* **Address:** Vii/528-B, Seaport - Airport Road, Thrikkakara, Kakkanad, Kochi, Kerala 682030.
* **Operator Verification:** Verified active tertiary hospital with 24/7 accident & trauma emergency department.
* **Ingress Access Node:** `lat: 10.0215, lon: 76.3478` (mapped to nearest curb node on Seaport-Airport Road).
* **Access Classification:** Ground access surveyed entrance (marked `PROVISIONAL` pending formal municipal validation).

### 4.2 Sampled Community Anchors (Origins)
Centroids sampled from distinct residential clusters to ensure geographic equity:
1. `orig_kakkanad_west`: Kakkanad West / Civil Station Environs (`10.0165, 76.3385`)
2. `orig_civil_station`: Kakkanad Civil Station Administrative Hub (`10.0195, 76.3435`)
3. `orig_padamugal`: Padamugal Residential Community Anchor (`10.0255, 76.3355`)
4. `orig_infopark_express`: Infopark Expressway Residential Sector (`10.0150, 76.3620`)
5. `orig_kaloor_kadavanthra`: Kaloor–Kadavanthra Feeder Boundary (`10.0050, 76.3320`)
6. `orig_canal_colony`: Canal Colony / Athani Settlement (`10.0310, 76.3480`)
7. `orig_dlf_city`: DLF City / New Town Heights Anchor (`10.0125, 76.3530`)

---

## 5. Data Transformations & Processing Pipeline

1. **Extraction:** Raw XML OSM data harvested via Overpass API queries filtering for `highway=*` and `building=*`.
2. **Merging & Deduplication:** Overlapping nodes and ways between bounding tiles merged using unique 64-bit integer OSM IDs.
3. **Graph Construction:** Directed multigraph (`MultiDiGraph`) constructed in NetworkX. Reversible roads split into bidirectional forward/reverse directed edges; one-way streets restricted to signed heading.
4. **Metric Projection:** Node coordinates projected from WGS 84 (`EPSG:4326`) to UTM Zone 43N (`EPSG:32643`) using `pyproj.Transformer`. Edge lengths calculated as geodesic Euclidean lengths in meters.
5. **Speed Factor Assignment:** Free-flow speeds assigned per Indian Road Congress (IRC) urban classification:
   * `primary`: 50 km/h (speed factor 1.0)
   * `secondary`: 40 km/h (speed factor 0.8)
   * `tertiary`: 30 km/h (speed factor 0.6)
   * `residential`: 20 km/h (speed factor 0.4)
   * `pedestrian`: 4.5 km/h walking speed

---

## 6. Known Limitations & Scientific Safeguards

1. **No Synthetic Populations:** SafeBuild does NOT synthesize resident census counts or trip volumes without registered municipal census tables. All impacts are reported in direct physical detour distance (meters) and percentage change.
2. **No Fictitious Emergency Seconds:** Ambulance travel times are NOT fabricated using arbitrary speed guesses. Turn delays and live signal delays are clearly marked outside static routing scope.
3. **Planar Elevation:** Coastal Kochi topography is modeled as 2D planar elevation. Slope gradient impedance is not applied.
4. **Turn Restrictions:** Micro-level signal turning bans (e.g. prohibited right turns during peak hours) are omitted unless explicitly tagged in OSM relations.
