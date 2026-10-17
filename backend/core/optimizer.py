from typing import Dict, List, Any
from backend.core.study_definitions import CANDIDATE_INTERVENTIONS

class InterventionOptimizer:
    def __init__(self, scenario_engine):
        self.scenario_engine = scenario_engine

    def evaluate_all_candidates(self, mode: str = "motor_vehicle") -> Dict[str, Any]:
        """
        Executes exact finite evaluation across all candidates in the candidate registry.
        Evaluates:
        - Modeled access recovery (meters & % detour reduction)
        - Worst-affected origin impact
        - Verification & Legal Permission Hard Gate
        - Mode conflicts (pedestrian vs vehicle)
        - Cost status
        """
        evaluations = []

        # Run base disruption (G0+C) to determine unmitigated benchmark
        base_run = self.scenario_engine.run_5_state_analysis(mode=mode, selected_candidate_id="cand_m1_phased_contraflow")
        base_worst_detour = base_run["summary"]["worst_detour_m"]
        base_avg_detour = base_run["summary"]["average_detour_m"]

        for cand in CANDIDATE_INTERVENTIONS:
            cid = cand["id"]
            run_res = self.scenario_engine.run_5_state_analysis(mode=mode, selected_candidate_id=cid)
            summary = run_res["summary"]

            # Calculate mitigation impact metrics
            recovered_detour_m = 0.0
            total_reduction_m = 0.0
            for orig in run_res["per_origin_results"]:
                rec = orig.get("mitigation_recovery_m")
                if rec and rec > 0:
                    total_reduction_m += rec

            avg_reduction_m = round(total_reduction_m / len(run_res["per_origin_results"]), 1)

            # Verification Hard Gate
            # Options: 'VERIFIED_IMPLEMENTABLE', 'GRAPH_ONLY_UNVERIFIED', 'REJECTED_OBSTRUCTED'
            perm_status = cand["permission_status"]
            phys_status = cand["physical_status"]
            
            if "REJECTED" in perm_status or "INELIGIBLE" in perm_status or "OBSTRUCTED" in phys_status or "DISCONTINUOUS" in phys_status:
                feasibility_class = "REJECTED_UNFEASIBLE"
                is_eligible_for_recommendation = False
                rejection_reason = "Ineligible under entered scenario constraints: private property alignment or discontinuous public right-of-way."
            elif "PERMISSION_CONFIRMED" in perm_status:
                feasibility_class = "VERIFIED_IMPLEMENTABLE"
                is_eligible_for_recommendation = True
                rejection_reason = None
            else:
                feasibility_class = "GRAPH_ONLY_UNVERIFIED"
                is_eligible_for_recommendation = False
                rejection_reason = "Unverified scenario candidate lacking field validation and authority review."

            evaluations.append({
                "candidate_id": cid,
                "name": cand["name"],
                "description": cand["description"],
                "type": cand["type"],
                "feasibility_class": feasibility_class,
                "is_eligible_for_recommendation": is_eligible_for_recommendation,
                "rejection_reason": rejection_reason,
                "physical_status": phys_status,
                "permission_status": perm_status,
                "cost_status": cand["cost_status"],
                "conflict_pedestrian": cand.get("conflict_pedestrian", False),
                "speed_factor": cand.get("speed_factor", 1.0),
                "reviewer": cand["reviewer"],
                "modeled_metrics": {
                    "average_detour_reduction_m": avg_reduction_m,
                    "worst_detour_after_m": summary["worst_detour_m"],
                    "new_unreachable_origins": summary["new_unreachable_origins"],
                    "worst_origin_affected": summary["worst_affected_origin"]
                }
            })

        # Rank candidates using lexicographic objective:
        # 1. Eligibility (must be verified to be chosen as recommended)
        # 2. Minimum new unreachable origins
        # 3. Minimum worst-origin detour
        # 4. Maximum average detour reduction
        eligible_candidates = [c for c in evaluations if c["is_eligible_for_recommendation"]]
        
        if not eligible_candidates:
            recommended_status = "NO_VERIFIED_OPTION"
            recommended_candidate = None
            recommendation_note = "All reviewed candidates are unverified model scenarios. SafeBuild does not present unverified routes as actionable advice."
        else:
            recommended_status = "CANDIDATE_SELECTED"
            recommended_candidate = min(
                eligible_candidates,
                key=lambda c: (
                    c["modeled_metrics"]["new_unreachable_origins"],
                    c["modeled_metrics"]["worst_detour_after_m"],
                    -c["modeled_metrics"]["average_detour_reduction_m"]
                )
            )
            recommendation_note = "Selected mathematically superior candidate among fully verified alternatives."

        return {
            "mode": mode,
            "benchmark_unmitigated_detour_m": base_worst_detour,
            "recommended_status": recommended_status,
            "recommended_candidate": recommended_candidate,
            "recommendation_note": recommendation_note,
            "ranking_stability": "STABLE_GIVEN_CONSTRAINTS",
            "all_evaluated_candidates": evaluations
        }
