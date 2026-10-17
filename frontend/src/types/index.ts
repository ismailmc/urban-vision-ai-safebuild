export type AnalyticalState = "G0" | "G0_C" | "G0_P" | "G0_P_C" | "G0_P_C_M";

export interface StudyMetadata {
  name: string;
  region: string;
  project_context: string;
  scenario_label: string;
  snapshot_date: string;
  core_bbox: [number, number, number, number];
  buffered_bbox: [number, number, number, number];
  crs_source: string;
  crs_projected: string;
  network_status: string;
}

export interface Facility {
  id: string;
  name: string;
  type: string;
  operator_source: string;
  lat: number;
  lon: number;
  address: string;
  verification_status: string;
  notes: string;
}

export interface RouteGeometry {
  reachable: boolean;
  distance_m: number | null;
  geometry: [number, number][];
}

export interface OriginResult {
  origin_id: string;
  origin_name: string;
  sampling_method?: string;
  origin_coords: [number, number];
  destination_id: string;
  destination_name: string;
  destination_coords: [number, number];
  G0_distance_m: number | null;
  G0_reachable: boolean;
  G0_C_distance_m: number | null;
  G0_C_reachable: boolean;
  G0_P_distance_m: number | null;
  G0_P_reachable: boolean;
  G0_P_C_distance_m: number | null;
  G0_P_C_reachable: boolean;
  G0_P_C_M_distance_m: number | null;
  G0_P_C_M_reachable: boolean;
  construction_delta_m: number | null;
  proposal_delta_m: number;
  mitigation_recovery_m: number | null;
  detour_percentage: number;
  routes: Record<AnalyticalState, RouteGeometry>;
}

export interface AnalysisSummary {
  total_origins: number;
  origins_reachable_G0: number;
  origins_reachable_G0_C: number;
  origins_reachable_G0_P_C_M: number;
  new_unreachable_origins: number;
  worst_detour_m: number;
  average_detour_m: number;
  worst_affected_origin: string;
  proposal_algebra_invariant_met: boolean;
}

export interface DisruptedSegment {
  way_id: string;
  name: string;
  geometry: [number, number][];
}

export interface CandidateEvaluation {
  candidate_id: string;
  name: string;
  description: string;
  type: string;
  feasibility_class: "VERIFIED_IMPLEMENTABLE" | "GRAPH_ONLY_UNVERIFIED" | "REJECTED_UNFEASIBLE";
  is_eligible_for_recommendation: boolean;
  rejection_reason: string | null;
  physical_status: string;
  permission_status: string;
  cost_status: string;
  conflict_pedestrian: boolean;
  speed_factor: number;
  reviewer: string;
  modeled_metrics: {
    average_detour_reduction_m: number;
    worst_detour_after_m: number;
    new_unreachable_origins: number;
    worst_origin_affected: string;
  };
}

export interface OptimizerResponse {
  mode: string;
  benchmark_unmitigated_detour_m: number;
  recommended_status: "NO_VERIFIED_OPTION" | "CANDIDATE_SELECTED";
  recommended_candidate: CandidateEvaluation | null;
  recommendation_note: string;
  ranking_stability: string;
  all_evaluated_candidates: CandidateEvaluation[];
}

export interface AnalysisResponse {
  run_id: string;
  metadata: StudyMetadata;
  mode: string;
  primary_facility: Facility;
  disruption_definition: {
    id: string;
    name: string;
    description: string;
    target_way_ids: string[];
    modes_affected: string[];
    direction?: string;
    phase?: string;
    status: string;
  };
  disrupted_segments: DisruptedSegment[];
  evaluated_candidate: Record<string, unknown>;
  summary: AnalysisSummary;
  per_origin_results: OriginResult[];
}

export interface RoadWayItem {
  osm_way_id: string;
  name: string;
  highway: string;
  length_m: number;
  layer: number;
  sample_point: [number, number];
}

export interface PhaseResult {
  phase_id: string;
  phase_name: string;
  duration_days: number;
  start_day: number;
  end_day: number;
  target_way_ids: string[];
  direction: string;
  mode: string;
  summary: AnalysisSummary;
  per_origin_results: OriginResult[];
}

export interface MultiPhaseAnalysisResponse {
  is_valid: boolean;
  validation_errors: string[];
  total_project_duration_days: number;
  phases_results: PhaseResult[];
}

export interface WorkArrangementCandidate {
  sequence_id: string;
  name: string;
  description: string;
  schedule_type: string;
  overall_project_duration_days: number;
  worst_modeled_detour_m: number;
  disconnection_count: number;
  is_eligible: boolean;
  ineligibility_reason: string | null;
  violations: string[];
  remaining_checks: string[];
  physical_status: string;
  permission_status: string;
}

export interface WorkArrangementsResponse {
  is_valid: boolean;
  evaluated_candidate_count: number;
  search_limitations: string;
  recommended_status: "NO_VERIFIED_OPTION" | "CANDIDATE_SELECTED";
  recommendation_note: string;
  candidate_arrangements: WorkArrangementCandidate[];
}
