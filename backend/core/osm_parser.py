import xml.etree.ElementTree as ET
import glob
import os
import hashlib
from typing import Dict, List, Tuple, Any, Optional
from backend.core.geo_utils import haversine_distance_m, polyline_length_m

class OSMNetwork:
    def __init__(self):
        self.nodes: Dict[str, Tuple[float, float, Dict[str, str]]] = {} # nid -> (lat, lon, tags)
        self.ways: Dict[str, Tuple[List[str], Dict[str, str]]] = {}      # wid -> (nd_refs, tags)
        self.relations: Dict[str, Tuple[List[Tuple[str, str, str]], Dict[str, str]]] = {} # rid -> (members, tags)
        self.source_hashes: Dict[str, str] = {}
        self.manifest: Dict[str, Any] = {}

    def load_osm_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Loads and merges multiple OSM XML files, computing SHA256 hashes and checking referential integrity."""
        for path in file_paths:
            with open(path, "rb") as f:
                content = f.read()
                file_hash = hashlib.sha256(content).hexdigest()
                self.source_hashes[os.path.basename(path)] = file_hash

            tree = ET.parse(path)
            root = tree.getroot()

            for n in root.findall("node"):
                nid = n.get("id")
                lat = float(n.get("lat"))
                lon = float(n.get("lon"))
                tags = {t.get("k"): t.get("v") for t in n.findall("tag")}
                self.nodes[nid] = (lat, lon, tags)

            for w in root.findall("way"):
                wid = w.get("id")
                nd_refs = [nd.get("ref") for nd in w.findall("nd")]
                tags = {t.get("k"): t.get("v") for t in w.findall("tag")}
                self.ways[wid] = (nd_refs, tags)

            for r in root.findall("relation"):
                rid = r.get("id")
                members = [(m.get("type"), m.get("ref"), m.get("role")) for m in r.findall("member")]
                tags = {t.get("k"): t.get("v") for t in r.findall("tag")}
                self.relations[rid] = (members, tags)

        # Audit referential integrity of highway ways
        highway_ways = {wid: (refs, tags) for wid, (refs, tags) in self.ways.items() if "highway" in tags}
        missing_refs = []
        for wid, (refs, _) in highway_ways.items():
            for r in refs:
                if r not in self.nodes:
                    missing_refs.append((wid, r))

        turn_restrictions = [
            (rid, tags.get("restriction", "unknown"), members)
            for rid, (members, tags) in self.relations.items()
            if tags.get("type") == "restriction"
        ]

        self.manifest = {
            "total_nodes": len(self.nodes),
            "total_ways": len(self.ways),
            "highway_ways": len(highway_ways),
            "total_relations": len(self.relations),
            "turn_restrictions_count": len(turn_restrictions),
            "turn_restrictions": turn_restrictions,
            "missing_highway_node_refs": len(missing_refs),
            "source_hashes": self.source_hashes
        }
        return self.manifest

    def build_directed_edges(self, mode: str = "motor_vehicle") -> List[Dict[str, Any]]:
        """
        Builds directed road network edges adhering to:
        - Highway filtering (exclude footway/cycleway for motor vehicle, allow for pedestrian)
        - Oneway tagging
        - Access tagging (exclude private unless overridden)
        - Bridge/layer/tunnel tags
        - Exact polyline geometry & geodesic length
        """
        edges = []
        excluded_hw_mv = {"footway", "pedestrian", "path", "cycleway", "steps", "corridor", "bridleway"}
        
        for wid, (refs, tags) in self.ways.items():
            hw = tags.get("highway")
            if not hw:
                continue

            if mode == "motor_vehicle" and hw in excluded_hw_mv:
                continue

            access = tags.get("access", "yes")
            if mode == "motor_vehicle":
                mv_access = tags.get("motor_vehicle", tags.get("vehicle", access))
                if mv_access in {"private", "no"}:
                    continue
            elif mode == "pedestrian":
                foot_access = tags.get("foot", access)
                if foot_access in {"no", "private"}:
                    continue

            # Determine directionality
            oneway_tag = tags.get("oneway", "no")
            junction = tags.get("junction")
            is_oneway = oneway_tag in {"yes", "1", "true"} or junction == "roundabout"
            is_reverse_oneway = oneway_tag in {"-1", "reverse"}

            # Grade & Layer
            layer = int(tags.get("layer", "0")) if tags.get("layer", "0").lstrip("-").isdigit() else 0
            bridge = tags.get("bridge", "no") in {"yes", "true", "1"}
            tunnel = tags.get("tunnel", "no") in {"yes", "true", "1"}
            name = tags.get("name", "Unnamed road")

            # Split way into segments between consecutive nodes
            valid_refs = [r for r in refs if r in self.nodes]
            if len(valid_refs) < 2:
                continue

            for i in range(len(valid_refs) - 1):
                u = valid_refs[i]
                v = valid_refs[i+1]
                u_lat, u_lon, _ = self.nodes[u]
                v_lat, v_lon, _ = self.nodes[v]
                length = haversine_distance_m(u_lat, u_lon, v_lat, v_lon)

                # Forward edge (u -> v)
                if not is_reverse_oneway:
                    edge_id_fwd = f"osm_{wid}_{u}_{v}_fwd"
                    edges.append({
                        "edge_id": edge_id_fwd,
                        "osm_way_id": wid,
                        "u": u,
                        "v": v,
                        "length_m": length,
                        "name": name,
                        "highway": hw,
                        "layer": layer,
                        "bridge": bridge,
                        "tunnel": tunnel,
                        "access": access,
                        "mode": mode,
                        "geometry": [[u_lat, u_lon], [v_lat, v_lon]]
                    })

                # Reverse edge (v -> u)
                if not is_oneway and not is_reverse_oneway:
                    edge_id_rev = f"osm_{wid}_{v}_{u}_rev"
                    edges.append({
                        "edge_id": edge_id_rev,
                        "osm_way_id": wid,
                        "u": v,
                        "v": u,
                        "length_m": length,
                        "name": name,
                        "highway": hw,
                        "layer": layer,
                        "bridge": bridge,
                        "tunnel": tunnel,
                        "access": access,
                        "mode": mode,
                        "geometry": [[v_lat, v_lon], [u_lat, u_lon]]
                    })

        return edges

    def extract_building_polygons(self) -> List[Dict[str, Any]]:
        """
        Extracts authentic building footprint polygons from OSM ways.
        Uses sourced height tags when present, or building:levels * 3.5m.
        Otherwise falls back to an illustrative default height (8.0m) with is_estimated=True.
        """
        features = []
        for wid, (refs, tags) in self.ways.items():
            if "building" in tags:
                coords = []
                for r in refs:
                    if r in self.nodes:
                        lat, lon, _ = self.nodes[r]
                        coords.append([lon, lat])
                if len(coords) >= 4:
                    height = 8.0
                    is_estimated = True
                    if "height" in tags:
                        try:
                            height = float(tags["height"].replace("m", "").strip())
                            is_estimated = False
                        except Exception:
                            pass
                    elif "building:levels" in tags:
                        try:
                            levels = float(tags["building:levels"])
                            height = levels * 3.5
                            is_estimated = False
                        except Exception:
                            pass
                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [coords]
                        },
                        "properties": {
                            "id": wid,
                            "height": height,
                            "is_estimated": is_estimated,
                            "name": tags.get("name", "Building footprint")
                        }
                    })
        return features

    def extract_road_geometries(self) -> List[Dict[str, Any]]:
        """
        Extracts all road centerlines as GeoJSON LineStrings for map-level edge selection.
        """
        features = []
        for wid, (refs, tags) in self.ways.items():
            if "highway" in tags:
                coords = []
                for r in refs:
                    if r in self.nodes:
                        lat, lon, _ = self.nodes[r]
                        coords.append([lon, lat])
                if len(coords) >= 2:
                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": coords
                        },
                        "properties": {
                            "way_id": wid,
                            "name": tags.get("name", "Unnamed road"),
                            "highway": tags.get("highway", "road"),
                            "oneway": tags.get("oneway", "no")
                        }
                    })
        return features

