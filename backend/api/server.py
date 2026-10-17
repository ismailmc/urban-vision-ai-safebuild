from fastapi import FastAPI, Query, HTTPException, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any, List
import os

from backend.core.scenario_engine import ScenarioEngine
from backend.core.optimizer import InterventionOptimizer
from backend.core.multi_phase_engine import MultiPhaseEngine, DEFAULT_CONSTRUCTION_PHASES
from backend.core.report_generator import generate_csv_report, generate_pdf_report
from backend.core.ai_analyst import SafeBuildGuardedAIAnalyst
from backend.core.study_definitions import STUDY_AREA_METADATA, FACILITIES, COMMUNITY_ORIGINS, CANDIDATE_INTERVENTIONS

app = FastAPI(
    title="Urban Vision AI — SafeBuild API",
    description="Community-First Infrastructure Accessibility & Resilience Scenario Evaluation Tool",
    version="4.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
scenario_engine = ScenarioEngine()
optimizer = InterventionOptimizer(scenario_engine)
multi_phase_engine = MultiPhaseEngine(scenario_engine)
ai_analyst = SafeBuildGuardedAIAnalyst()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SafeBuild Analytical Engine",
        "study_area": STUDY_AREA_METADATA["name"],
        "dataset_nodes": scenario_engine.osm_manifest["total_nodes"],
        "highway_edges_motor": len(scenario_engine.raw_edges["motor_vehicle"]),
        "ai_analyst_active": ai_analyst.is_available()
    }

@app.get("/api/metadata")
def get_metadata():
    return {
        "study_area": STUDY_AREA_METADATA,
        "facilities": FACILITIES,
        "origins": COMMUNITY_ORIGINS,
        "candidate_interventions": CANDIDATE_INTERVENTIONS,
        "osm_provenance": scenario_engine.osm_manifest,
        "active_disruptions": scenario_engine.active_disruptions,
        "default_phases": DEFAULT_CONSTRUCTION_PHASES
    }

@app.get("/api/roads")
def get_roads_catalog():
    """Returns catalog of mapped road ways for the interactive scenario editor."""
    return scenario_engine.get_road_ways_catalog()

@app.get("/api/geography/buildings")
def get_buildings():
    """Returns GeoJSON FeatureCollection of OSM building footprints with tagged or estimated default heights."""
    features = scenario_engine.get_building_features()
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/api/geography/roads")
def get_road_geometries():
    """Returns GeoJSON FeatureCollection of all road centerlines for direct map selection."""
    features = scenario_engine.get_road_features()
    return {
        "type": "FeatureCollection",
        "features": features
    }

# Analysis & Optimizer In-Memory Cache
_analysis_cache: Dict[str, Any] = {}
_optimizer_cache: Dict[str, Any] = {}

def get_cached_analysis(mode: str, candidate_id: str):
    cache_key = f"{mode}_{candidate_id}_{len(scenario_engine.active_disruptions)}"
    if cache_key not in _analysis_cache:
        _analysis_cache[cache_key] = scenario_engine.run_5_state_analysis(mode=mode, selected_candidate_id=candidate_id)
    return _analysis_cache[cache_key]

def get_cached_optimizer(mode: str):
    cache_key = f"{mode}_{len(scenario_engine.active_disruptions)}"
    if cache_key not in _optimizer_cache:
        _optimizer_cache[cache_key] = optimizer.evaluate_all_candidates(mode=mode)
    return _optimizer_cache[cache_key]

@app.post("/api/disruptions")
def update_disruptions(payload: Dict[str, Any] = Body(...)):
    """Allows user to configure hypothetical restrictions with specific target ways, direction, mode and phase."""
    target_way_ids = payload.get("target_way_ids", [])
    if not target_way_ids:
        raise HTTPException(status_code=400, detail="target_way_ids cannot be empty")
    name = payload.get("name", "User Configured Restriction")
    direction = payload.get("direction", "both")
    mode = payload.get("mode", "motor_vehicle")
    phase = payload.get("phase", "Custom Construction Phase")

    _analysis_cache.clear()
    _optimizer_cache.clear()

    scenario_engine.update_disruptions(
        target_way_ids=target_way_ids,
        name=name,
        direction=direction,
        mode=mode,
        phase=phase
    )
    return {
        "status": "updated",
        "active_disruptions": scenario_engine.active_disruptions
    }

@app.post("/api/disruptions/reset")
def reset_disruptions():
    """Resets restrictions to baseline corridor disruption."""
    _analysis_cache.clear()
    _optimizer_cache.clear()
    scenario_engine.reset_disruptions()
    return {
        "status": "reset",
        "active_disruptions": scenario_engine.active_disruptions
    }

@app.get("/api/analysis")
def run_analysis(
    mode: str = Query("motor_vehicle", enum=["motor_vehicle", "pedestrian"]),
    candidate_id: str = Query("cand_m1_phased_contraflow")
):
    try:
        results = get_cached_analysis(mode=mode, candidate_id=candidate_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/optimizer")
def run_optimizer(mode: str = Query("motor_vehicle", enum=["motor_vehicle", "pedestrian"])):
    try:
        opt_results = get_cached_optimizer(mode=mode)
        return opt_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Multi-Phase Construction Endpoints
@app.get("/api/phases")
def get_default_phases():
    return DEFAULT_CONSTRUCTION_PHASES

@app.post("/api/phases/analyze")
def analyze_construction_phases(payload: Dict[str, Any] = Body(...)):
    phases = payload.get("phases", DEFAULT_CONSTRUCTION_PHASES)
    mode = payload.get("mode", "motor_vehicle")
    result = multi_phase_engine.analyze_phases(phases, mode=mode)
    if not result["is_valid"]:
        raise HTTPException(status_code=400, detail={"errors": result["validation_errors"]})
    return result

@app.post("/api/arrangements/evaluate")
def evaluate_arrangements(payload: Dict[str, Any] = Body(...)):
    phases = payload.get("phases", DEFAULT_CONSTRUCTION_PHASES)
    mode = payload.get("mode", "motor_vehicle")
    result = multi_phase_engine.evaluate_work_arrangements(phases, mode=mode)
    return result

@app.get("/api/report/csv")
def download_csv(mode: str = Query("motor_vehicle")):
    scenario_res = get_cached_analysis(mode=mode, candidate_id="cand_m1_phased_contraflow")
    csv_content = generate_csv_report(scenario_res)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=safebuild_{mode}_report.csv"}
    )

@app.get("/api/report/pdf")
def download_pdf(mode: str = Query("motor_vehicle")):
    scenario_res = get_cached_analysis(mode=mode, candidate_id="cand_m1_phased_contraflow")
    opt_res = get_cached_optimizer(mode=mode)
    os.makedirs("data/processed", exist_ok=True)
    pdf_path = f"data/processed/safebuild_{mode}_report.pdf"
    generate_pdf_report(scenario_res, opt_res, pdf_path)
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=safebuild_{mode}_scenario_report.pdf"}
    )

@app.post("/api/ai/ask")
def ask_ai_analyst(payload: Dict[str, Any]):
    prompt = payload.get("prompt", "Summarize accessibility impact.")
    mode = payload.get("mode", "motor_vehicle")
    candidate_id = payload.get("candidate_id", "cand_m1_phased_contraflow")

    scenario_res = get_cached_analysis(mode=mode, candidate_id=candidate_id)
    opt_res = get_cached_optimizer(mode=mode)

    ai_response = ai_analyst.analyze_scenario(prompt, scenario_res, opt_res)
    return ai_response
