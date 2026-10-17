import unittest
from backend.core.geo_utils import haversine_distance_m, wgs84_to_utm43n, polyline_length_m
from backend.core.routing_engine import DirectedRoutingEngine

class TestAnalyticalCore(unittest.TestCase):
    def test_rg01_crs_and_geodesic_units(self):
        """RG-01: Coordinate units and non-zero positive distances."""
        # Check Kakkanad center to Sunrise Hospital anchor
        kakkanad_center = (10.0225, 76.3450)
        sunrise_anchor = (10.0252315, 76.3388796)
        dist = haversine_distance_m(kakkanad_center[0], kakkanad_center[1], sunrise_anchor[0], sunrise_anchor[1])
        self.assertGreater(dist, 500.0)
        self.assertLess(dist, 1500.0)

        # UTM 43N conversion produces realistic positive coordinates
        e, n = wgs84_to_utm43n(kakkanad_center[0], kakkanad_center[1])
        self.assertGreater(e, 600000.0) # Zone 43 easting
        self.assertGreater(n, 1000000.0) # North equator distance

    def test_rg03_forbidden_movements_and_oneway(self):
        """RG-03: Strict directed edges: reverse movement on one-way road is unreachable."""
        engine = DirectedRoutingEngine()
        engine.set_nodes({'N1': (10.0, 76.0), 'N2': (10.0, 76.01)})
        # Only forward edge
        engine.load_edges([{'edge_id': 'fwd_1', 'u': 'N1', 'v': 'N2', 'length_m': 120.0}])
        fwd = engine.shortest_path('N1', 'N2')
        self.assertTrue(fwd['reachable'])
        self.assertEqual(fwd['distance_m'], 120.0)

        rev = engine.shortest_path('N2', 'N1')
        self.assertFalse(rev['reachable'])
        self.assertIsNone(rev['distance_m'])

    def test_rg04_grade_separation_crossing(self):
        """RG-04: Crossing roads at different levels without shared node do not create a fake junction."""
        engine = DirectedRoutingEngine()
        # Highway A: N1 -> N2 (at grade layer 0)
        # Highway B: M1 -> M2 (flyover layer 1, crossing geometric path of A but no common node)
        engine.set_nodes({
            'N1': (10.0, 76.0), 'N2': (10.0, 76.02),
            'M1': (9.99, 76.01), 'M2': (10.01, 76.01)
        })
        engine.load_edges([
            {'edge_id': 'e_A', 'u': 'N1', 'v': 'N2', 'length_m': 200.0, 'layer': 0},
            {'edge_id': 'e_B', 'u': 'M1', 'v': 'M2', 'length_m': 200.0, 'layer': 1}
        ])
        # Path from N1 to M2 must be impossible (unreachable)
        cross = engine.shortest_path('N1', 'M2')
        self.assertFalse(cross['reachable'])

    def test_rg07_closure_monotonicity(self):
        """RG-07: Removing an edge cannot shorten shortest distance or create new connectivity."""
        engine = DirectedRoutingEngine()
        engine.set_nodes({'A': (10.0, 76.0), 'B': (10.0, 76.01), 'C': (10.0, 76.02)})
        # Direct route A->C (dist 100), detour A->B->C (dist 60 + 60 = 120)
        edges = [
            {'edge_id': 'direct', 'u': 'A', 'v': 'C', 'length_m': 100.0},
            {'edge_id': 'd1', 'u': 'A', 'v': 'B', 'length_m': 60.0},
            {'edge_id': 'd2', 'u': 'B', 'v': 'C', 'length_m': 60.0}
        ]
        engine.load_edges(edges)
        p0 = engine.shortest_path('A', 'C')
        self.assertEqual(p0['distance_m'], 100.0)

        # Apply closure: remove 'direct'
        detour_edges = [e for e in edges if e['edge_id'] != 'direct']
        engine.load_edges(detour_edges)
        p_closed = engine.shortest_path('A', 'C')
        self.assertTrue(p_closed['reachable'])
        self.assertGreaterEqual(p_closed['distance_m'], p0['distance_m'])
        self.assertEqual(p_closed['distance_m'], 120.0)

if __name__ == '__main__':
    unittest.main()
