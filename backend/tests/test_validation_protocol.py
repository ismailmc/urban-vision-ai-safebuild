import unittest
from backend.core.geo_utils import haversine_distance_m, wgs84_to_utm43n
from backend.core.scenario_engine import ScenarioEngine
from backend.core.optimizer import InterventionOptimizer
from backend.core.ai_analyst import SafeBuildGuardedAIAnalyst
from backend.core.study_definitions import STUDY_AREA_METADATA, FACILITIES, COMMUNITY_ORIGINS

class TestValidationProtocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = ScenarioEngine()
        cls.optimizer = InterventionOptimizer(cls.engine)
        cls.ai = SafeBuildGuardedAIAnalyst()

    def test_gate_01_crs_and_anchors(self):
        """RG-01: Zero CRS swaps; all Kakkanad anchors within true bbox bounds."""
        bbox = STUDY_AREA_METADATA["buffered_bbox"] # [76.330, 10.010, 76.360, 10.035]
        for orig in COMMUNITY_ORIGINS:
            self.assertGreaterEqual(orig["lon"], bbox[0])
            self.assertLessEqual(orig["lon"], bbox[2])
            self.assertGreaterEqual(orig["lat"], bbox[1])
            self.assertLessEqual(orig["lat"], bbox[3])

        for fac in FACILITIES:
            self.assertGreaterEqual(fac["lon"], bbox[0])
            self.assertLessEqual(fac["lon"], bbox[2])
            self.assertGreaterEqual(fac["lat"], bbox[1])
            self.assertLessEqual(fac["lat"], bbox[3])

    def test_gate_02_referential_integrity(self):
        """RG-02: Zero missing highway node references."""
        manifest = self.engine.osm_manifest
        self.assertEqual(manifest["missing_highway_node_refs"], 0)
        self.assertGreater(manifest["total_nodes"], 15000)

    def test_gate_06_proposal_algebra_invariant(self):
        """RG-06: Identity proposal P yields exactly 0 delta across all origins."""
        res = self.engine.run_5_state_analysis(mode="motor_vehicle")
        self.assertTrue(res["summary"]["proposal_algebra_invariant_met"])
        for r in res["per_origin_results"]:
            self.assertEqual(r["proposal_delta_m"], 0.0)

    def test_gate_07_closure_monotonicity(self):
        """RG-07: Construction closure C cannot shorten shortest distance or create connectivity."""
        res = self.engine.run_5_state_analysis(mode="motor_vehicle")
        for r in res["per_origin_results"]:
            if r["G0_reachable"] and r["G0_C_reachable"]:
                self.assertGreaterEqual(r["G0_C_distance_m"], r["G0_distance_m"])
                self.assertGreaterEqual(r["construction_delta_m"], 0.0)

    def test_gate_11_optimizer_permission_hard_gate(self):
        """RG-11: Unapproved candidates barred from VERIFIED_IMPLEMENTABLE; emits NO_VERIFIED_OPTION."""
        opt_res = self.optimizer.evaluate_all_candidates(mode="motor_vehicle")
        self.assertEqual(opt_res["recommended_status"], "NO_VERIFIED_OPTION")
        for cand in opt_res["all_evaluated_candidates"]:
            if cand["feasibility_class"] != "VERIFIED_IMPLEMENTABLE":
                self.assertFalse(cand["is_eligible_for_recommendation"])

    def test_gate_14_ai_assertion_integrity(self):
        """RG-14: AI filter blocks ungrounded causal claims and fabricated approvals."""
        scenario_res = self.engine.run_5_state_analysis(mode="motor_vehicle")
        opt_res = self.optimizer.evaluate_all_candidates(mode="motor_vehicle")
        
        # Test claim with forbidden phrase
        bad_text = "This intervention was approved by KMRL and saves 4 minutes in ambulance response time."
        val = self.ai.validate_assertion_claims(bad_text, scenario_res, opt_res)
        self.assertFalse(val.is_valid)
        self.assertGreater(len(val.violations), 0)

if __name__ == '__main__':
    unittest.main()
