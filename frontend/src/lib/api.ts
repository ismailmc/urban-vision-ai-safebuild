import { AnalysisResponse, OptimizerResponse, RoadWayItem } from "@/types";

const API_BASE = "http://localhost:8000/api";

export async function fetchAnalysis(mode: string = "motor_vehicle", candidateId: string = "cand_m1_phased_contraflow"): Promise<AnalysisResponse> {
  const res = await fetch(`${API_BASE}/analysis?mode=${mode}&candidate_id=${candidateId}`);
  if (!res.ok) throw new Error("Failed to fetch analysis");
  return res.json();
}

export async function fetchOptimizer(mode: string = "motor_vehicle"): Promise<OptimizerResponse> {
  const res = await fetch(`${API_BASE}/optimizer?mode=${mode}`);
  if (!res.ok) throw new Error("Failed to fetch optimizer");
  return res.json();
}

export async function fetchRoadsCatalog(): Promise<RoadWayItem[]> {
  const res = await fetch(`${API_BASE}/roads`);
  if (!res.ok) throw new Error("Failed to fetch roads catalog");
  return res.json();
}

export async function fetchBuildings(): Promise<GeoJSON.FeatureCollection> {
  const res = await fetch(`${API_BASE}/geography/buildings`);
  if (!res.ok) throw new Error("Failed to fetch buildings");
  return res.json();
}

export async function fetchRoadGeometries(): Promise<GeoJSON.FeatureCollection> {
  const res = await fetch(`${API_BASE}/geography/roads`);
  if (!res.ok) throw new Error("Failed to fetch road geometries");
  return res.json();
}

export async function updateDisruption(payload: {
  target_way_ids: string[];
  name?: string;
  direction?: string;
  mode?: string;
  phase?: string;
}) {
  const res = await fetch(`${API_BASE}/disruptions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Failed to update disruption");
  return res.json();
}

export async function resetDisruption() {
  const res = await fetch(`${API_BASE}/disruptions/reset`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to reset disruption");
  return res.json();
}

export async function askAIAnalyst(prompt: string, mode: string = "motor_vehicle", candidateId: string = "cand_m1_phased_contraflow") {
  const res = await fetch(`${API_BASE}/ai/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, mode, candidate_id: candidateId })
  });
  if (!res.ok) throw new Error("Failed to communicate with AI Analyst");
  return res.json();
}

export async function fetchPhases(): Promise<Record<string, unknown>[]> {
  const res = await fetch(`${API_BASE}/phases`);
  if (!res.ok) throw new Error("Failed to fetch default phases");
  return res.json();
}

export async function analyzePhases(phases: Record<string, unknown>[], mode: string = "motor_vehicle") {
  const res = await fetch(`${API_BASE}/phases/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phases, mode })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail?.errors ? err.detail.errors.join(", ") : "Failed to analyze phases");
  }
  return res.json();
}

export async function evaluateArrangements(phases?: Record<string, unknown>[], mode: string = "motor_vehicle") {
  const res = await fetch(`${API_BASE}/arrangements/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phases: phases || undefined, mode })
  });
  if (!res.ok) throw new Error("Failed to evaluate work arrangements");
  return res.json();
}
