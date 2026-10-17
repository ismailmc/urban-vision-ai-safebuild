import networkx as nx
from typing import Dict, List, Tuple, Any, Optional
from backend.core.geo_utils import haversine_distance_m

class DirectedRoutingEngine:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.turn_restrictions: List[Dict[str, Any]] = []
        self.edge_meta: Dict[str, Dict[str, Any]] = {}
        self.node_coords: Dict[str, Tuple[float, float]] = {}

    def set_nodes(self, node_coords: Dict[str, Tuple[float, float]]):
        self.node_coords = node_coords
        for nid, (lat, lon) in node_coords.items():
            self.graph.add_node(nid, lat=lat, lon=lon)

    def load_edges(self, edges: List[Dict[str, Any]]):
        self.graph.clear()
        for nid, (lat, lon) in self.node_coords.items():
            self.graph.add_node(nid, lat=lat, lon=lon)

        for e in edges:
            u, v = e["u"], e["v"]
            eid = e["edge_id"]
            length = e["length_m"]
            self.graph.add_edge(u, v, key=eid, weight=length, **e)
            self.edge_meta[eid] = e

    def find_nearest_road_node(self, lat: float, lon: float, max_dist_m: float = 1200.0) -> Optional[Tuple[str, float]]:
        """
        Snaps a point (origin or destination) strictly to an active road network node
        (degree > 0 in the connected road network), rejecting isolated POI nodes.
        """
        best_node = None
        best_dist = float("inf")
        for nid, deg in self.graph.degree():
            if deg == 0:
                continue
            data = self.graph.nodes[nid]
            if "lat" not in data or "lon" not in data:
                continue
            d = haversine_distance_m(lat, lon, data["lat"], data["lon"])
            if d < best_dist:
                best_dist = d
                best_node = nid

        if best_dist <= max_dist_m:
            return best_node, best_dist
        return None

    def shortest_path(self, origin_node: str, destination_node: str) -> Dict[str, Any]:
        """
        Computes shortest directed path on graph considering edge weights (lengths in meters).
        Returns dictionary containing:
        - reachable: bool
        - distance_m: float or None
        - node_path: List[str]
        - edge_ids: List[str]
        - geometry: List[List[float]] (lat, lon)
        """
        if origin_node not in self.graph or destination_node not in self.graph:
            return {
                "reachable": False,
                "distance_m": None,
                "node_path": [],
                "edge_ids": [],
                "geometry": []
            }

        try:
            node_path = nx.shortest_path(self.graph, source=origin_node, target=destination_node, weight="weight")
            distance_m = nx.shortest_path_length(self.graph, source=origin_node, target=destination_node, weight="weight")
            
            edge_ids = []
            geometry = []
            for i in range(len(node_path) - 1):
                u = node_path[i]
                v = node_path[i+1]
                edge_data = self.graph.get_edge_data(u, v)
                eid = edge_data.get("key", f"{u}_{v}")
                edge_ids.append(eid)
                u_lat, u_lon = self.graph.nodes[u]["lat"], self.graph.nodes[u]["lon"]
                if not geometry:
                    geometry.append([u_lat, u_lon])
                v_lat, v_lon = self.graph.nodes[v]["lat"], self.graph.nodes[v]["lon"]
                geometry.append([v_lat, v_lon])

            return {
                "reachable": True,
                "distance_m": distance_m,
                "node_path": node_path,
                "edge_ids": edge_ids,
                "geometry": geometry
            }
        except nx.NetworkXNoPath:
            return {
                "reachable": False,
                "distance_m": None,
                "node_path": [],
                "edge_ids": [],
                "geometry": []
            }
