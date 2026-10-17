import glob
import copy
import uuid
from typing import Dict, List, Any, Optional
from backend.core.osm_parser import OSMNetwork
from backend.core.routing_engine import DirectedRoutingEngine
from backend.core.study_definitions import (
    STUDY_AREA_METADATA, FACILITIES, COMMUNITY_ORIGINS,
    CONSTRUCTION_DISRUPTIONS, CANDIDATE_INTERVENTIONS
)

class ScenarioEngine:
    def __init__(self, osm_files: Optional[List[str]] = None):
        self.osm_network = OSMNetwork()
        if osm_files is None:
            osm_files = sorted(glob.glob("data/raw_osm/subbox_*.osm"))
        if not osm_files:
            raise RuntimeError("No OSM XML files found to build network.")
        self.osm_manifest = self.osm_network.load_osm_files(osm_files)
        self.raw_edges = {
            "motor_vehicle": self.osm_network.build_directed_edges("motor_vehicle"),
            "pedestrian": self.osm_network.build_directed_edges("pedestrian")
        }
        self.node_coords = {nid: (data[0], data[1]) for nid, data in self.osm_network.nodes.items()}
        
        # In-memory custom user restriction state
        self.active_disruptions = copy.deepcopy(CONSTRUCTION_DISRUPTIONS)

    def _build_engine(self, edges: List[Dict[str, Any]]) -> DirectedRoutingEngine:
        engine = DirectedRoutingEngine()
        engine.set_nodes(self.node_coords)
        engine.load_edges(edges)
        return engine

    def get_road_ways_catalog(self) -> List[Dict[str, Any]]:
        """Returns indexed road ways with their names, highway types, total lengths and coordinate extents."""
        ways_dict = {}
        for e in self.raw_edges["motor_vehicle"]:
            wid = e.get("osm_way_id")
            if wid not in ways_dict:
                ways_dict[wid] = {
                    "osm_way_id": wid,
                    "name": e.get("name", "Unnamed road"),
                    "highway": e.get("highway"),
                    "length_m": 0.0,
                    "layer": e.get("layer", 0),
                    "oneway": e.get("oneway", False),
                    "coordinates": []
                }
            ways_dict[wid]["length_m"] += e.get("length_m", 0.0)
            ways_dict[wid]["coordinates"].extend(e.get("geometry", []))

        # Simplify coordinates representation for frontend list
        catalog = []
        for wid, data in sorted(ways_dict.items(), key=lambda x: (x[1]["name"] == "Unnamed road", -x[1]["length_m"])):
            catalog.append({
                "osm_way_id": wid,
                "name": data["name"],
                "highway": data["highway"],
                "length_m": round(data["length_m"], 1),
                "layer": data["layer"],
                "sample_point": data["coordinates"][0] if data["coordinates"] else [10.0225, 76.3450]
            })
        return catalog

    def get_building_features(self) -> List[Dict[str, Any]]:
        return self.osm_network.extract_building_polygons()

    def get_road_features(self) -> List[Dict[str, Any]]:
        return self.osm_network.extract_road_geometries()

    def update_disruptions(self, target_way_ids: List[str], name: str = "User Configured Restriction", direction: str = "both", mode: str = "motor_vehicle", phase: str = "Custom Phase"):
        """Updates in-memory restriction configuration."""
        self.active_disruptions = [{
            "id": f"c_user_{uuid.uuid4().hex[:6]}",
            "name": name,
            "description": f"Custom user-configured restriction on {len(target_way_ids)} road ways.",
            "target_way_ids": target_way_ids,
            "modes_affected": [mode],
            "direction": direction,
            "phase": phase,
            "status": "USER_CONFIGURED_RESTRICTION",
            "authority_status": "HYPOTHETICAL_USER_SCENARIO"
        }]

    def reset_disruptions(self):
        """Resets to baseline hypothetical corridor disruption."""
        self.active_disruptions = copy.deepcopy(CONSTRUCTION_DISRUPTIONS)

    def run_5_state_analysis(self, mode: str = "motor_vehicle", selected_candidate_id: str = "cand_m1_phased_contraflow") -> Dict[str, Any]:
        run_id = f"run_{uuid.uuid4().hex[:8]}"
        base_edges = self.raw_edges[mode]
        primary_disruption = self.active_disruptions[0]
        disrupted_way_ids = set(primary_disruption["target_way_ids"])

        candidate = next((c for c in CANDIDATE_INTERVENTIONS if c["id"] == selected_candidate_id), CANDIDATE_INTERVENTIONS[0])

        # Graph 0 (G0)
        edges_g0 = base_edges
        engine_g0 = self._build_engine(edges_g0)

        # Graph G0+C: remove disrupted edges
        # Handle direction: if 'both', remove all edges with that way_id
        # If 'fwd_only', remove only edges ending with '_fwd'
        edges_g0_c = []
        for e in base_edges:
            wid = e.get("osm_way_id")
            if wid in disrupted_way_ids:
                if primary_disruption.get("direction") == "fwd_only" and e.get("edge_id", "").endswith("_fwd"):
                    continue
                elif primary_disruption.get("direction") == "rev_only" and e.get("edge_id", "").endswith("_rev"):
                    continue
                elif primary_disruption.get("direction") in ["both", None]:
                    continue
            edges_g0_c.append(e)

        engine_g0_c = self._build_engine(edges_g0_c)

        # Graph G0+P: P is identity
        engine_g0_p = engine_g0

        # Graph G0+P+C
        engine_g0_p_c = engine_g0_c

        # Graph G0+P+C+M
        restored_ways = set(candidate.get("restores_way_ids", []))
        edges_g0_p_c_m = []
        for e in base_edges:
            wid = e.get("osm_way_id")
            if wid in disrupted_way_ids:
                if wid in restored_ways:
                    penalty_factor = 1.0 / candidate.get("speed_factor", 0.5)
                    e_mit = dict(e)
                    e_mit["length_m"] = e["length_m"] * penalty_factor
                    edges_g0_p_c_m.append(e_mit)
            else:
                edges_g0_p_c_m.append(e)

        engine_g0_p_c_m = self._build_engine(edges_g0_p_c_m)

        # Extract geometry of affected segments for mapping
        disrupted_segments_geometry = []
        for e in base_edges:
            if e.get("osm_way_id") in disrupted_way_ids:
                disrupted_segments_geometry.append({
                    "way_id": e.get("osm_way_id"),
                    "name": e.get("name"),
                    "geometry": e.get("geometry")
                })

        # Snap facilities & origins to active road network
        primary_facility = FACILITIES[0]
        dest_snap = engine_g0.find_nearest_road_node(primary_facility["lat"], primary_facility["lon"])
        if not dest_snap:
            raise RuntimeError("Could not snap primary facility to road network.")
        dest_node, dest_snap_dist = dest_snap

        origin_snaps = {}
        for orig in COMMUNITY_ORIGINS:
            snap = engine_g0.find_nearest_road_node(orig["lat"], orig["lon"])
            if snap:
                origin_snaps[orig["id"]] = snap

        engines = {
            "G0": engine_g0,
            "G0_C": engine_g0_c,
            "G0_P": engine_g0_p,
            "G0_P_C": engine_g0_p_c,
            "G0_P_C_M": engine_g0_p_c_m
        }

        per_origin_results = []
        for orig in COMMUNITY_ORIGINS:
            oid = orig["id"]
            if oid not in origin_snaps:
                continue
            orig_node, snap_dist = origin_snaps[oid]

            state_routes = {}
            for s_name, eng in engines.items():
                res = eng.shortest_path(orig_node, dest_node)
                state_routes[s_name] = res

            d_g0 = state_routes["G0"]["distance_m"] if state_routes["G0"]["reachable"] else None
            d_g0_c = state_routes["G0_C"]["distance_m"] if state_routes["G0_C"]["reachable"] else None
            d_g0_p = state_routes["G0_P"]["distance_m"] if state_routes["G0_P"]["reachable"] else None
            d_g0_p_c = state_routes["G0_P_C"]["distance_m"] if state_routes["G0_P_C"]["reachable"] else None
            d_g0_p_c_m = state_routes["G0_P_C_M"]["distance_m"] if state_routes["G0_P_C_M"]["reachable"] else None

            # Attribution Deltas
            construction_delta_m = (d_g0_c - d_g0) if (d_g0 is not None and d_g0_c is not None) else None
            proposal_delta_m = (d_g0_p - d_g0) if (d_g0 is not None and d_g0_p is not None) else 0.0
            mitigation_recovery_m = (d_g0_p_c - d_g0_p_c_m) if (d_g0_p_c is not None and d_g0_p_c_m is not None) else None

            detour_pct = ((d_g0_c - d_g0) / d_g0 * 100.0) if (d_g0 and d_g0_c and d_g0 > 0) else 0.0

            per_origin_results.append({
                "origin_id": oid,
                "origin_name": orig["name"],
                "sampling_method": orig["sampling_method"],
                "origin_coords": [orig["lat"], orig["lon"]],
                "destination_id": primary_facility["id"],
                "destination_name": primary_facility["name"],
                "destination_coords": [primary_facility["lat"], primary_facility["lon"]],
                "G0_distance_m": round(d_g0, 1) if d_g0 else None,
                "G0_reachable": state_routes["G0"]["reachable"],
                "G0_C_distance_m": round(d_g0_c, 1) if d_g0_c else None,
                "G0_C_reachable": state_routes["G0_C"]["reachable"],
                "G0_P_distance_m": round(d_g0_p, 1) if d_g0_p else None,
                "G0_P_reachable": state_routes["G0_P"]["reachable"],
                "G0_P_C_distance_m": round(d_g0_p_c, 1) if d_g0_p_c else None,
                "G0_P_C_reachable": state_routes["G0_P_C"]["reachable"],
                "G0_P_C_M_distance_m": round(d_g0_p_c_m, 1) if d_g0_p_c_m else None,
                "G0_P_C_M_reachable": state_routes["G0_P_C_M"]["reachable"],
                "construction_delta_m": round(construction_delta_m, 1) if construction_delta_m is not None else None,
                "proposal_delta_m": round(proposal_delta_m, 1) if proposal_delta_m is not None else 0.0,
                "mitigation_recovery_m": round(mitigation_recovery_m, 1) if mitigation_recovery_m is not None else None,
                "detour_percentage": round(detour_pct, 1),
                "routes": {
                    s: {
                        "reachable": state_routes[s]["reachable"],
                        "distance_m": round(state_routes[s]["distance_m"], 1) if state_routes[s]["distance_m"] else None,
                        "geometry": state_routes[s]["geometry"]
                    }
                    for s in ["G0", "G0_C", "G0_P", "G0_P_C", "G0_P_C_M"]
                }
            })

        reachable_g0 = sum(1 for r in per_origin_results if r["G0_reachable"])
        reachable_g0_c = sum(1 for r in per_origin_results if r["G0_C_reachable"])
        reachable_mit = sum(1 for r in per_origin_results if r["G0_P_C_M_reachable"])

        valid_detours = [r["construction_delta_m"] for r in per_origin_results if r["construction_delta_m"] is not None]
        worst_detour_m = max(valid_detours) if valid_detours else 0.0
        avg_detour_m = (sum(valid_detours) / len(valid_detours)) if valid_detours else 0.0

        worst_origin = max(per_origin_results, key=lambda r: (r["construction_delta_m"] or 0.0))

        return {
            "run_id": run_id,
            "metadata": STUDY_AREA_METADATA,
            "mode": mode,
            "primary_facility": primary_facility,
            "disruption_definition": primary_disruption,
            "disrupted_segments": disrupted_segments_geometry,
            "evaluated_candidate": candidate,
            "summary": {
                "total_origins": len(per_origin_results),
                "origins_reachable_G0": reachable_g0,
                "origins_reachable_G0_C": reachable_g0_c,
                "origins_reachable_G0_P_C_M": reachable_mit,
                "new_unreachable_origins": reachable_g0 - reachable_g0_c,
                "worst_detour_m": round(worst_detour_m, 1),
                "average_detour_m": round(avg_detour_m, 1),
                "worst_affected_origin": worst_origin["origin_name"],
                "proposal_algebra_invariant_met": all(r["proposal_delta_m"] == 0.0 for r in per_origin_results)
            },
            "per_origin_results": per_origin_results
        }
