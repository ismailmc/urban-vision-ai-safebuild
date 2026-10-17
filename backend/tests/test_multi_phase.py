import unittest
from backend.core.scenario_engine import ScenarioEngine
from backend.core.multi_phase_engine import MultiPhaseEngine, DEFAULT_CONSTRUCTION_PHASES
from backend.core.construction_models import ConstructionPhase, detect_circular_dependencies, compute_schedule_exposure_days

class TestMultiPhaseAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenario_engine = ScenarioEngine()
        cls.engine = MultiPhaseEngine(cls.scenario_engine)

    def test_default_phases_validation(self):
        """Default construction phases should pass validation with zero errors."""
        errors = self.engine.validate_phases(DEFAULT_CONSTRUCTION_PHASES)
        self.assertEqual(len(errors), 0, f"Expected no validation errors in default phases, got: {errors}")

    def test_circular_dependency_detection(self):
        """Ensure cyclic dependencies are caught deterministically."""
        cyclic_phases = [
            ConstructionPhase(
                phase_id="p1",
                name="Phase 1",
                duration=10.0,
                duration_unit="days",
                dependencies=["p3"],
                target_way_ids=["197827530"]
            ),
            ConstructionPhase(
                phase_id="p2",
                name="Phase 2",
                duration=15.0,
                duration_unit="days",
                dependencies=["p1"],
                target_way_ids=["197827530"]
            ),
            ConstructionPhase(
                phase_id="p3",
                name="Phase 3",
                duration=20.0,
                duration_unit="days",
                dependencies=["p2"],
                target_way_ids=["197827530"]
            )
        ]
        cycles = detect_circular_dependencies(cyclic_phases)
        self.assertTrue(len(cycles) > 0, "Failed to detect 3-phase circular dependency cycle")
        self.assertIn("Circular dependency detected", cycles[0])

    def test_unknown_osm_way_id_validation(self):
        """Ensure unknown OSM way IDs are flagged during validation."""
        invalid_phases = [
            {
                "phase_id": "p_invalid",
                "name": "Invalid Road Target",
                "duration": 10.0,
                "duration_unit": "days",
                "dependencies": [],
                "target_way_ids": ["9999999999999_nonexistent"],
                "direction": "both",
                "mode": "motor_vehicle"
            }
        ]
        errors = self.engine.validate_phases(invalid_phases)
        self.assertTrue(any("unknown OSM way ID" in err for err in errors))

    def test_negative_or_zero_duration_validation(self):
        """Ensure negative or zero duration is flagged."""
        invalid_phases = [
            {
                "phase_id": "p_zero",
                "name": "Zero Duration Phase",
                "duration": 0.0,
                "duration_unit": "days",
                "dependencies": [],
                "target_way_ids": ["197827530"],
                "direction": "both",
                "mode": "motor_vehicle"
            }
        ]
        errors = self.engine.validate_phases(invalid_phases)
        self.assertTrue(any("must have a positive duration" in err for err in errors))

    def test_schedule_exposure_sequential_sum(self):
        """Ensure sequential schedule exposure sums duration correctly and converts weeks to days."""
        phases = [
            ConstructionPhase(
                phase_id="p1",
                name="Phase 1",
                duration=2.0,
                duration_unit="weeks",
                dependencies=[],
                target_way_ids=["197827530"]
            ),
            ConstructionPhase(
                phase_id="p2",
                name="Phase 2",
                duration=10.0,
                duration_unit="days",
                dependencies=["p1"],
                target_way_ids=["197827530"]
            )
        ]
        exposure = compute_schedule_exposure_days(phases, ["p1", "p2"], schedule_type="sequential")
        self.assertEqual(exposure["total_duration_days"], 24.0)
        self.assertEqual(exposure["schedule"]["p1"]["start_day"], 0.0)
        self.assertEqual(exposure["schedule"]["p1"]["end_day"], 14.0)
        self.assertEqual(exposure["schedule"]["p2"]["start_day"], 14.0)
        self.assertEqual(exposure["schedule"]["p2"]["end_day"], 24.0)

    def test_multi_phase_execution_and_g0_invariance(self):
        """Verify each phase produces accurate detour calculations against pre-construction G0 baseline."""
        res = self.engine.analyze_phases(DEFAULT_CONSTRUCTION_PHASES, mode="motor_vehicle")
        self.assertTrue(res["is_valid"])
        self.assertEqual(len(res["phases_results"]), 3)
        self.assertEqual(res["total_project_duration_days"], 96.0)

        for p_res in res["phases_results"]:
            self.assertIn("phase_id", p_res)
            self.assertIn("summary", p_res)
            self.assertIn("per_origin_results", p_res)
            for orig in p_res["per_origin_results"]:
                self.assertIn("exposure_duration_days", orig)
                self.assertIn("is_disconnected_by_construction", orig)
                self.assertIn("baseline_unreachable", orig)
                self.assertFalse(orig["is_disconnected_by_construction"])

    def test_bounded_arrangements_prototype_review_gate(self):
        """Verify candidate work arrangements respect NO_VERIFIED_OPTION prototype review gate."""
        res = self.engine.evaluate_work_arrangements(DEFAULT_CONSTRUCTION_PHASES, mode="motor_vehicle")
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["recommended_status"], "NO_VERIFIED_OPTION")
        self.assertIn("unverified model scenarios", res["recommendation_note"])
        
        candidates = res["candidate_arrangements"]
        self.assertTrue(len(candidates) >= 3)
        for c in candidates:
            self.assertIn("sequence_id", c)
            self.assertIn("overall_project_duration_days", c)
            self.assertIn("worst_modeled_detour_m", c)
            self.assertIn("is_eligible", c)
            self.assertFalse(c["is_eligible"]) # None are currently eligible without verification
            self.assertIn("violations", c)
            self.assertIn("remaining_checks", c)

if __name__ == "__main__":
    unittest.main()
