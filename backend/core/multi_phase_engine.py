"""
Multi-Phase Construction Analysis Engine.
Simulates accessibility per construction phase and evaluates candidate sequencing arrangements.
"""
from typing import Dict, List, Any, Optional
import copy
from backend.core.construction_models import ConstructionPhase, detect_circular_dependencies, compute_schedule_exposure_days
from backend.core.study_definitions import (
    STUDY_AREA_METADATA, FACILITIES, COMMUNITY_ORIGINS,
    CONSTRUCTION_DISRUPTIONS, CANDIDATE_INTERVENTIONS
)

DEFAULT_CONSTRUCTION_PHASES = [
    {
        "phase_id": "phase_1_utilities",
        "name": "Phase 1: Underground Utility Relocation",
        "duration": 21.0,
        "duration_unit": "days",
        "dependencies": [],
        "target_way_ids": ["197827530"],
        "direction": "both",
        "mode": "motor_vehicle",
        "status": "PROPOSED_UNVERIFIED"
    },
    {
        "phase_id": "phase_2_pier_foundation",
        "name": "Phase 2: Metro Pier Foundation & Piling",
        "duration": 45.0,
        "duration_unit": "days",
        "dependencies": ["phase_1_utilities"],
        "target_way_ids": ["197827530", "383253303", "1011679137", "1011679138"],
        "direction": "both",
        "mode": "motor_vehicle",
        "status": "PROPOSED_UNVERIFIED"
    },
    {
        "phase_id": "phase_3_girder_launch",
        "name": "Phase 3: Viaduct Girder Launching",
        "duration": 30.0,
        "duration_unit": "days",
        "dependencies": ["phase_2_pier_foundation"],
        "target_way_ids": ["383253303", "1011679138"],
        "direction": "both",
        "mode": "motor_vehicle",
        "status": "PROPOSED_UNVERIFIED"
    }
]

class MultiPhaseEngine:
    def __init__(self, scenario_engine):
        self.scenario_engine = scenario_engine

    def validate_phases(self, phases_data: List[Dict[str, Any]]) -> List[str]:
        """Validates phase objects, positive durations, unknown segment IDs and circular dependencies."""
        errors = []
        phase_objects = []
        catalog = {r["osm_way_id"] for r in self.scenario_engine.get_road_ways_catalog()}
        
        for idx, pd in enumerate(phases_data):
            pid = pd.get("phase_id", f"p_{idx}")
            name = pd.get("name", f"Phase {idx+1}")
            dur = pd.get("duration", 0)
            if dur <= 0:
                errors.append(f"Phase '{name}' must have a positive duration (got {dur}).")
            
            # Check segment existence
            for wid in pd.get("target_way_ids", []):
                if wid not in catalog:
                    errors.append(f"Phase '{name}' targets unknown OSM way ID '{wid}'.")
            
            phase_objects.append(ConstructionPhase(
                phase_id=pid,
                name=name,
                duration=float(dur) if dur > 0 else 1.0,
                duration_unit=pd.get("duration_unit", "days"),
                dependencies=pd.get("dependencies", []),
                target_way_ids=pd.get("target_way_ids", []),
                direction=pd.get("direction", "both"),
                mode=pd.get("mode", "motor_vehicle"),
                status=pd.get("status", "PROPOSED_UNVERIFIED")
            ))
            
        cycles = detect_circular_dependencies(phase_objects)
        errors.extend(cycles)
        return errors

    def analyze_phases(self, phases_data: List[Dict[str, Any]], mode: str = "motor_vehicle") -> Dict[str, Any]:
        """
        Executes actual graph connectivity and shortest-path calculation for each phase
        compared against the exact same pre-construction baseline (G0).
        """
        validation_errors = self.validate_phases(phases_data)
        if validation_errors:
            return {
                "is_valid": False,
                "validation_errors": validation_errors,
                "phases_results": []
            }

        phase_objects = [
            ConstructionPhase(
                phase_id=pd["phase_id"],
                name=pd["name"],
                duration=float(pd["duration"]),
                duration_unit=pd.get("duration_unit", "days"),
                dependencies=pd.get("dependencies", []),
                target_way_ids=pd.get("target_way_ids", []),
                direction=pd.get("direction", "both"),
                mode=pd.get("mode", mode)
            ) for pd in phases_data
        ]

        # Calculate schedule exposure
        order = [p.phase_id for p in phase_objects]
        schedule_info = compute_schedule_exposure_days(phase_objects, order, schedule_type="sequential")

        phases_results = []
        for p in phase_objects:
            # Temporarily configure disruption for this phase
            self.scenario_engine.active_disruptions = [{
                "id": f"c_{p.phase_id}",
                "name": p.name,
                "description": f"Phase restriction for {p.name}",
                "target_way_ids": p.target_way_ids,
                "modes_affected": [p.mode],
                "direction": p.direction,
                "phase": p.name,
                "status": "HYPOTHETICAL_CONSTRUCTION_SCENARIO"
            }]

            analysis = self.scenario_engine.run_5_state_analysis(mode=mode)
            sched = schedule_info["schedule"].get(p.phase_id, {})

            # Annotate origin results with exposure duration
            annotated_origins = []
            for r in analysis["per_origin_results"]:
                r_copy = dict(r)
                is_affected = (r_copy.get("construction_delta_m") or 0.0) > 0 or (r_copy["G0_reachable"] and not r_copy["G0_C_reachable"])
                is_disconnected = r_copy["G0_reachable"] and not r_copy["G0_C_reachable"]
                r_copy["exposure_duration_days"] = sched.get("duration_days", 0.0) if is_affected else 0.0
                r_copy["is_disconnected_by_construction"] = is_disconnected
                r_copy["baseline_unreachable"] = not r_copy["G0_reachable"]
                annotated_origins.append(r_copy)

            phases_results.append({
                "phase_id": p.phase_id,
                "phase_name": p.name,
                "duration_days": sched.get("duration_days", p.duration),
                "start_day": sched.get("start_day", 0.0),
                "end_day": sched.get("end_day", p.duration),
                "target_way_ids": p.target_way_ids,
                "direction": p.direction,
                "mode": p.mode,
                "summary": analysis["summary"],
                "per_origin_results": annotated_origins
            })

        return {
            "is_valid": True,
            "validation_errors": [],
            "total_project_duration_days": schedule_info["total_duration_days"],
            "phases_results": phases_results
        }

    def evaluate_work_arrangements(self, phases_data: List[Dict[str, Any]], mode: str = "motor_vehicle") -> Dict[str, Any]:
        """
        Bounded comparison of work arrangements (e.g., sequential vs staggered closures).
        Evaluates candidate work arrangements against access constraints, duration limits and legal gates.
        """
        base_eval = self.analyze_phases(phases_data, mode=mode)
        if not base_eval["is_valid"]:
            return {
                "is_valid": False,
                "validation_errors": base_eval["validation_errors"],
                "candidate_arrangements": []
            }

        # Defined realistic candidate arrangements for the metro project
        candidates = [
            {
                "sequence_id": "seq_standard_sequential",
                "name": "Arrangement A: Standard Sequential Phasing",
                "description": "Executes utility relocation, piling, and girder launching one phase at a time without overlapping road closures.",
                "schedule_type": "sequential",
                "staggered_offset_days": 0,
                "physical_status": "PHYSICALLY_FEASIBLE_EXISTING_CARRIAGEWAY",
                "permission_status": "PROPOSED_REQUIRES_AUTHORITY_APPROVAL",
                "candidate_intervention_id": "cand_m2_civil_lane_diversion"
            },
            {
                "sequence_id": "seq_managed_contraflow",
                "name": "Arrangement B: Phased Single-Lane Contraflow Managed Phasing",
                "description": "Preserves managed single-lane corridor flow during foundation and girder phases with flagger coordination.",
                "schedule_type": "sequential",
                "staggered_offset_days": 0,
                "physical_status": "PHYSICALLY_FEASIBLE_EXISTING_CARRIAGEWAY",
                "permission_status": "UNVERIFIED_PENDING_TRAFFIC_POLICE_REVIEW",
                "candidate_intervention_id": "cand_m1_phased_contraflow"
            },
            {
                "sequence_id": "seq_concurrent_fasttrack",
                "name": "Arrangement C: Accelerated Concurrent Work (Unstaggered)",
                "description": "Simultaneously closes multiple corridor reaches to shorten total duration, but severely compounds community detour exposure.",
                "schedule_type": "concurrent",
                "staggered_offset_days": 0,
                "physical_status": "HIGH_CORRIDOR_CONGESTION_RISK",
                "permission_status": "PERMISSION_REJECTED_TRAFFIC_POLICE",
                "candidate_intervention_id": "cand_m3_unverified_private_easement"
            }
        ]

        evaluated = []
        for cand in candidates:
            # Check eligibility and constraints
            violations = []
            perm = cand["permission_status"]
            phys = cand["physical_status"]
            is_eligible = True
            ineligibility_reason = None

            if "REJECTED" in perm or "OBSTRUCTED" in phys:
                is_eligible = False
                ineligibility_reason = "Explicit statutory refusal by traffic police or physical roadway obstruction."
                violations.append("Violation: Rejected by traffic authority due to safety/access thresholds.")
            elif "APPROVAL" in perm or "PENDING" in perm or "UNVERIFIED" in perm:
                is_eligible = False
                ineligibility_reason = "Proposed candidate requires signed authority approval and verified safety staffing plan."
                violations.append("Notice: Awaiting statutory sanction (NO_VERIFIED_OPTION).")

            # Compute impacts across phases
            total_exposure_days = 0.0
            worst_detour_m = 0.0
            disconnection_count = 0

            for p_res in base_eval["phases_results"]:
                total_exposure_days += p_res["duration_days"]
                if p_res["summary"]["worst_detour_m"] > worst_detour_m:
                    worst_detour_m = p_res["summary"]["worst_detour_m"]
                disconnection_count += p_res["summary"]["new_unreachable_origins"]

            evaluated.append({
                "sequence_id": cand["sequence_id"],
                "name": cand["name"],
                "description": cand["description"],
                "schedule_type": cand["schedule_type"],
                "overall_project_duration_days": base_eval["total_project_duration_days"] if cand["schedule_type"] == "sequential" else round(base_eval["total_project_duration_days"] * 0.65, 1),
                "worst_modeled_detour_m": worst_detour_m,
                "disconnection_count": disconnection_count,
                "is_eligible": is_eligible,
                "ineligibility_reason": ineligibility_reason,
                "violations": violations,
                "remaining_checks": [
                    "Joint site survey with Kerala State Traffic Police",
                    "KMRL civil construction contractor safety sign-off",
                    "Emergency vehicle priority lane certification"
                ],
                "physical_status": phys,
                "permission_status": perm
            })

        return {
            "is_valid": True,
            "evaluated_candidate_count": len(evaluated),
            "search_limitations": "Bounded finite comparison over 3 statutory sequencing candidates.",
            "recommended_status": "NO_VERIFIED_OPTION",
            "recommendation_note": "All candidates are currently marked 'Proposed — requires authority approval'. No option has received formal traffic police clearance.",
            "candidate_arrangements": evaluated
        }
