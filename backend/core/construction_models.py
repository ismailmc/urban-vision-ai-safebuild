"""
Construction schedule, phase, and sequencing models with cycle detection and validation.
"""
from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field

class ConstructionPhase(BaseModel):
    phase_id: str = Field(..., description="Unique identifier for the construction phase")
    name: str = Field(..., description="Human-readable activity or phase name")
    duration: float = Field(..., gt=0, description="Duration value (must be positive)")
    duration_unit: str = Field("days", description="Duration unit: 'days', 'weeks', 'months'")
    dependencies: List[str] = Field(default_factory=list, description="IDs of preceding phases that must complete before this phase")
    target_way_ids: List[str] = Field(default_factory=list, description="Roadway OSM way IDs restricted in this phase")
    direction: str = Field("both", description="Restriction direction: 'both', 'fwd_only', 'rev_only'")
    mode: str = Field("motor_vehicle", description="Restricted mode: 'motor_vehicle' or 'pedestrian'")
    status: str = Field("PROPOSED_UNVERIFIED", description="Scenario verification status")

class WorkArrangementSequence(BaseModel):
    sequence_id: str
    name: str
    description: str
    schedule_type: str = Field("sequential", description="'sequential' or 'concurrent'")
    phase_order: List[str]
    max_concurrency: int = 1
    total_project_duration_days: float
    violations: List[str] = Field(default_factory=list)
    is_eligible: bool = True
    ineligibility_reason: Optional[str] = None
    remaining_checks: List[str] = Field(default_factory=list)

def detect_circular_dependencies(phases: List[ConstructionPhase]) -> List[str]:
    """
    Checks for circular dependencies among construction phases using Kahn's algorithm or DFS.
    Returns list of cycle error messages if any cycle is detected.
    """
    phase_map = {p.phase_id: p for p in phases}
    adj: Dict[str, List[str]] = {p.phase_id: [] for p in phases}
    
    # Check for missing dependency references first
    errors = []
    for p in phases:
        for dep in p.dependencies:
            if dep not in phase_map:
                errors.append(f"Phase '{p.name}' ({p.phase_id}) depends on unknown phase '{dep}'.")
            else:
                adj[dep].append(p.phase_id) # dep -> p
                
    if errors:
        return errors

    # Cycle detection via DFS
    visited = {} # 0: unvisited, 1: visiting, 2: visited
    for pid in phase_map:
        visited[pid] = 0

    cycle_nodes = []

    def dfs(node: str, path: List[str]) -> bool:
        visited[node] = 1
        path.append(node)
        for neighbor in adj[node]:
            if visited[neighbor] == 1:
                # Cycle detected
                cycle_path = " -> ".join(path + [neighbor])
                cycle_nodes.append(f"Circular dependency detected: {cycle_path}")
                return True
            elif visited[neighbor] == 0:
                if dfs(neighbor, path):
                    return True
        path.pop()
        visited[node] = 2
        return False

    for pid in phase_map:
        if visited[pid] == 0:
            if dfs(pid, []):
                break

    return cycle_nodes

def compute_schedule_exposure_days(phases: List[ConstructionPhase], order: List[str], schedule_type: str = "sequential") -> Dict[str, Any]:
    """
    Computes exact phase intervals without double-counting overlaps.
    Returns start/end offsets for each phase and overall project duration.
    """
    phase_map = {p.phase_id: p for p in phases}
    schedule = {}
    current_time = 0.0

    if schedule_type == "sequential":
        for pid in order:
            if pid not in phase_map:
                continue
            p = phase_map[pid]
            dur_days = p.duration * (7.0 if p.duration_unit == "weeks" else 30.0 if p.duration_unit == "months" else 1.0)
            start = current_time
            end = current_time + dur_days
            schedule[pid] = {
                "start_day": round(start, 1),
                "end_day": round(end, 1),
                "duration_days": round(dur_days, 1)
            }
            current_time = end
    else: # concurrent / dependency-based
        for pid in order:
            if pid not in phase_map:
                continue
            p = phase_map[pid]
            dur_days = p.duration * (7.0 if p.duration_unit == "weeks" else 30.0 if p.duration_unit == "months" else 1.0)
            dep_ends = [schedule[dep]["end_day"] for dep in p.dependencies if dep in schedule]
            start = max(dep_ends) if dep_ends else 0.0
            end = start + dur_days
            schedule[pid] = {
                "start_day": round(start, 1),
                "end_day": round(end, 1),
                "duration_days": round(dur_days, 1)
            }
            if end > current_time:
                current_time = end

    return {
        "schedule": schedule,
        "total_duration_days": round(current_time, 1)
    }
