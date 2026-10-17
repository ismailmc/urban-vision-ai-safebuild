import React, { useState } from "react";
import { OriginResult, CandidateEvaluation, AnalyticalState, StudyMetadata, Facility, AnalysisSummary } from "@/types";
import { askAIAnalyst } from "@/lib/api";
import { StudioTab } from "@/components/NavigationRail";
import { SelectedRoadInfo } from "@/components/MapCanvas";
import {
  AlertTriangle, Send, Sparkles,
  Compass, Layers, Users, ChevronDown, ChevronRight,
  PlusCircle, Trash2, Check, ArrowRight, Download, FileSpreadsheet, GitCompare
} from "lucide-react";

interface StudioSidePanelProps {
  activeTab: StudioTab;
  onSelectTab: (tab: StudioTab) => void;
  selectedOrigin: OriginResult | null;
  onSelectOrigin: (id: string) => void;
  allOrigins: OriginResult[];
  selectedState: AnalyticalState;
  onSelectState: (state: AnalyticalState) => void;
  metadata: StudyMetadata | null;
  facility: Facility | null;
  candidate: CandidateEvaluation | null;
  allCandidates: CandidateEvaluation[];
  onSelectCandidate: (candidateId: string) => void;
  onOpenEvidenceModal: () => void;
  onOpenEditorModal: () => void;
  runId: string | null;
  summary: AnalysisSummary | null;
  selectedRoad: SelectedRoadInfo | null;
  onClearSelectedRoad: () => void;
  onAddRoadRestriction: (road: SelectedRoadInfo) => void;
  onRemoveRoadRestriction: (wayId: string) => void;
  activeDisruptedWayIds: string[];
  onAnalyzeAccess: () => void;
  isAnalyzing: boolean;
  selectedTravelMode: string;
}

export const StudioSidePanel: React.FC<StudioSidePanelProps> = ({
  activeTab,
  onSelectTab,
  selectedOrigin,
  onSelectOrigin,
  allOrigins,
  selectedState,
  onSelectState,
  metadata,
  facility,
  candidate,
  allCandidates,
  onSelectCandidate,
  onOpenEvidenceModal,
  onOpenEditorModal,
  runId,
  summary,
  selectedRoad,
  onClearSelectedRoad,
  onAddRoadRestriction,
  onRemoveRoadRestriction,
  activeDisruptedWayIds,
  onAnalyzeAccess,
  isAnalyzing,
  selectedTravelMode
}) => {
  const [showTechnicalDetails, setShowTechnicalDetails] = useState(false);
  const [aiQuestion, setAiQuestion] = useState("Explain this change");
  const [aiAnswer, setAiAnswer] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiViolations, setAiViolations] = useState<string[]>([]);

  // Road action form state
  const [roadDirection, setRoadDirection] = useState("both");
  const [roadMode, setRoadMode] = useState("motor_vehicle");
  const [roadPhase, setRoadPhase] = useState("Phase 1: Civil Pier Foundation");
  const [roadConfirmSaved, setRoadConfirmSaved] = useState(false);

  const CONTEXT_QUESTIONS = [
    "Explain this change",
    "Why did this option not qualify?",
    "What is the net detour for Kakkanad West?",
    "Which community experiences the greatest route increase?"
  ];

  const handleAskAI = async (queryText?: string) => {
    const q = queryText || aiQuestion;
    setAiLoading(true);
    setAiAnswer(null);
    setAiViolations([]);
    try {
      const res = await askAIAnalyst(q, selectedTravelMode, candidate?.candidate_id || "cand_m1_phased_contraflow");
      setAiAnswer(res.analysis);
      if (res.violations && res.violations.length > 0) {
        setAiViolations(res.violations);
      }
    } catch {
      setAiAnswer("Failed to reach analyst service. Please ensure the backend is running.");
    } finally {
      setAiLoading(false);
    }
  };

  const handleSaveRoadRestriction = () => {
    if (!selectedRoad) return;
    onAddRoadRestriction(selectedRoad);
    setRoadConfirmSaved(true);
    setTimeout(() => setRoadConfirmSaved(false), 2500);
  };

  const isCurrentRoadRestricted = selectedRoad ? activeDisruptedWayIds.includes(selectedRoad.way_id) : false;

  return (
    <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-sm flex flex-col h-full text-slate-800 overflow-hidden">
      {/* Workflow Step Bar / Header */}
      <div className="border-b border-slate-100 pb-3 mb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="w-5 h-5 rounded-full bg-teal-100 text-teal-800 text-xs font-extrabold flex items-center justify-center">
              {activeTab === "explore" && "1"}
              {activeTab === "define" && "2"}
              {activeTab === "impact" && "3"}
              {activeTab === "alternatives" && "4"}
              {activeTab === "summary" && "5"}
            </span>
            <div className="text-xs font-bold uppercase tracking-wider text-teal-800">
              {activeTab === "explore" && "Step 1: Explore Area"}
              {activeTab === "define" && "Step 2: Define Change"}
              {activeTab === "impact" && "Step 3: See Impact"}
              {activeTab === "alternatives" && "Step 4: Compare Alternatives"}
              {activeTab === "summary" && "Step 5: Decision Summary"}
            </div>
          </div>

          <button
            onClick={() => setShowTechnicalDetails(!showTechnicalDetails)}
            className="text-[11px] font-semibold text-slate-600 hover:text-slate-900 flex items-center space-x-1 bg-slate-100 hover:bg-slate-200 px-2 py-1 rounded transition"
          >
            <span>{showTechnicalDetails ? "Hide Technical" : "Technical View"}</span>
            {showTechnicalDetails ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
          </button>
        </div>

        <div className="text-sm font-extrabold text-slate-900 mt-1">
          {activeTab === "explore" && "Geographic Context & 3D Massing"}
          {activeTab === "define" && "Interactive Road Restrictions"}
          {activeTab === "impact" && "Community Access & Detour Evaluation"}
          {activeTab === "alternatives" && "Candidate Alternatives Ledger"}
          {activeTab === "summary" && "Decision Brief & Review Safeguards"}
        </div>
      </div>

      {/* Main Scrollable Body */}
      <div className="flex-1 overflow-y-auto space-y-4 text-xs pr-1">

        {/* STEP 1: EXPLORE AREA */}
        {activeTab === "explore" && (
          <div className="space-y-3.5">
            {/* Quick entry points */}
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => {
                  onSelectOrigin("orig_kakkanad_west");
                  onSelectState("G0_C");
                }}
                className="p-2.5 bg-teal-50 hover:bg-teal-100/70 border border-teal-200 rounded-xl text-left transition shadow-xs"
              >
                <div className="font-bold text-teal-900 text-xs">Try Kakkanad Example</div>
                <div className="text-[11px] text-teal-700 mt-0.5 leading-tight">Authentic network with Palarivattom workzone</div>
              </button>
              <button
                onClick={() => onSelectTab("define")}
                className="p-2.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl text-left transition shadow-xs"
              >
                <div className="font-bold text-slate-800 text-xs">Create Access Scenario</div>
                <div className="text-[11px] text-slate-500 mt-0.5 leading-tight">Select roads and define restrictions</div>
              </button>
            </div>

            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <div className="flex items-center space-x-2 text-teal-800 font-bold">
                <Compass className="w-4 h-4" />
                <span>Kakkanad Corridor Bounds</span>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Explore the mapped road network around Palarivattom–Kakkanad Road and Seaport–Airport Road. Use the <b>2D/3D toggle</b> on the map toolbar to inspect corridor massing with authentic building footprints.
              </p>
              <div className="pt-1 border-t border-slate-200 flex justify-between text-slate-500">
                <span>Total Mapped Nodes: <b>19,582</b></span>
                <span>Directed Edges: <b>11,675</b></span>
              </div>
            </div>

            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <div className="font-bold text-slate-900">Destination Anchor</div>
              <div className="text-slate-800 font-semibold">{facility?.name}</div>
              <div className="text-slate-500">{facility?.address}</div>
              <div className="inline-block px-2 py-0.5 bg-teal-100 text-teal-900 text-[10px] rounded font-semibold">
                Access Anchor: Seaport-Airport Rd Entrance
              </div>
            </div>

            <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-xl text-amber-900 leading-relaxed">
              <b>Planning Guidance:</b> You can click any street on the map to inspect its connection properties and define hypothetical construction closures in Step 2.
            </div>

            <button
              onClick={() => onSelectTab("define")}
              className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-semibold rounded-lg flex items-center justify-center space-x-1.5 shadow-sm transition"
            >
              <span>Next: Define Change</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* STEP 2: DEFINE CHANGE */}
        {activeTab === "define" && (
          <div className="space-y-3.5">
            {/* Selected Road Compact Action Panel */}
            {selectedRoad ? (
              <div className="p-4 bg-teal-50/60 border border-teal-200 rounded-xl space-y-3 shadow-sm">
                <div className="flex items-center justify-between border-b border-teal-200 pb-2">
                  <div className="font-bold text-slate-900 text-sm flex items-center space-x-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                    <span>{selectedRoad.name}</span>
                  </div>
                  <button
                    onClick={onClearSelectedRoad}
                    className="text-slate-400 hover:text-slate-700 text-xs font-semibold"
                  >
                    Deselect
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-2 text-slate-600">
                  <div>OSM Way ID: <b className="font-mono text-slate-800">{selectedRoad.way_id}</b></div>
                  <div>Highway Class: <b className="text-slate-800">{selectedRoad.highway}</b></div>
                </div>

                {/* Form Controls */}
                <div className="space-y-2 pt-1 border-t border-teal-200">
                  <div>
                    <label className="font-semibold text-slate-700 block mb-0.5">Directional Restriction:</label>
                    <select
                      value={roadDirection}
                      onChange={(e) => setRoadDirection(e.target.value)}
                      className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white"
                    >
                      <option value="both">Both Directions (Full Closure)</option>
                      <option value="fwd_only">Forward Only</option>
                      <option value="rev_only">Reverse Only</option>
                    </select>
                  </div>

                  <div>
                    <label className="font-semibold text-slate-700 block mb-0.5">Affected Mode:</label>
                    <select
                      value={roadMode}
                      onChange={(e) => setRoadMode(e.target.value)}
                      className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white"
                    >
                      <option value="motor_vehicle">Motor Vehicle</option>
                      <option value="pedestrian">Pedestrian</option>
                    </select>
                  </div>

                  <div>
                    <label className="font-semibold text-slate-700 block mb-0.5">Phase / Time Window:</label>
                    <input
                      type="text"
                      value={roadPhase}
                      onChange={(e) => setRoadPhase(e.target.value)}
                      className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white"
                    />
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="pt-2 flex items-center space-x-2">
                  {!isCurrentRoadRestricted ? (
                    <button
                      onClick={handleSaveRoadRestriction}
                      className="flex-1 py-2 bg-amber-600 hover:bg-amber-700 text-white font-semibold rounded-lg flex items-center justify-center space-x-1.5 shadow-sm transition"
                    >
                      <PlusCircle className="w-3.5 h-3.5" />
                      <span>Add Hypothetical Restriction</span>
                    </button>
                  ) : (
                    <button
                      onClick={() => onRemoveRoadRestriction(selectedRoad.way_id)}
                      className="flex-1 py-2 bg-rose-600 hover:bg-rose-700 text-white font-semibold rounded-lg flex items-center justify-center space-x-1.5 shadow-sm transition"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                      <span>Remove Restriction</span>
                    </button>
                  )}
                </div>

                {roadConfirmSaved && (
                  <div className="p-2 bg-emerald-50 border border-emerald-300 text-emerald-800 rounded text-xs font-semibold flex items-center space-x-1.5">
                    <Check className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Restriction staged. Click Analyze below to recalculate.</span>
                  </div>
                )}
              </div>
            ) : (
              <div className="p-4 bg-slate-50 border border-slate-200 border-dashed rounded-xl text-center space-y-2">
                <Layers className="w-6 h-6 text-slate-400 mx-auto" />
                <div className="font-bold text-slate-800">Select Any Road on Map</div>
                <p className="text-slate-500 leading-relaxed">
                  Click any road centerline directly on the map canvas to open its action panel, view its OSM way ID, and define a directional restriction.
                </p>
                <div className="pt-1">
                  <button
                    onClick={onOpenEditorModal}
                    className="px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold rounded-lg shadow-sm"
                  >
                    Open Multi-Road Scenario Catalog
                  </button>
                </div>
              </div>
            )}

            {/* Active Restrictions Count */}
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1.5">
              <div className="flex justify-between font-bold text-slate-800">
                <span>Active Workzone Restrictions:</span>
                <span className="font-mono text-amber-700 font-extrabold">{activeDisruptedWayIds.length} road segment(s)</span>
              </div>
              <p className="text-slate-500 text-[11px]">
                Classification: <b>HYPOTHETICAL_USER_SCENARIO</b>. Source edge IDs preserved for referential auditing.
              </p>
            </div>

            <button
              onClick={() => onSelectTab("impact")}
              className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-semibold rounded-lg flex items-center justify-center space-x-1.5 shadow-sm transition"
            >
              <span>Next: See Impact</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* STEP 3: SEE IMPACT */}
        {activeTab === "impact" && (
          <div className="space-y-3.5">
            {/* Prominent Analyze Button */}
            <button
              onClick={onAnalyzeAccess}
              disabled={isAnalyzing}
              className="w-full py-3 bg-teal-700 hover:bg-teal-800 text-white font-extrabold rounded-xl shadow-md flex items-center justify-center space-x-2 transition text-sm"
            >
              <Users className="w-4 h-4" />
              <span>{isAnalyzing ? "Recalculating Network Shortest Paths..." : "Analyze Community Access"}</span>
            </button>

            {/* Plain-Language Selected Comparison Explanation */}
            {selectedOrigin && (
              <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2.5">
                <div className="text-[11px] font-bold uppercase tracking-wider text-teal-800">Community Access Result</div>
                <div className="font-extrabold text-slate-900 text-sm">{selectedOrigin.origin_name}</div>

                {/* Plain language statement */}
                <div className="p-2.5 bg-white border border-slate-200 rounded-lg text-slate-700 leading-relaxed">
                  {selectedOrigin.construction_delta_m && selectedOrigin.construction_delta_m > 0 ? (
                    <span>
                      This sampled community origin has a <b>longer modeled route</b> to {facility?.name || "the hospital"}, requiring an extra <b>+{selectedOrigin.construction_delta_m} m ({selectedOrigin.detour_percentage}%)</b> under construction closures.
                    </span>
                  ) : (
                    <span>
                      This sampled community origin maintains an <b>unaffected modeled route</b> to {facility?.name || "the hospital"} with 0 m detour.
                    </span>
                  )}
                </div>

                {/* Actual Distances Grid */}
                <div className="grid grid-cols-2 gap-2 text-center">
                  <div className="p-2 bg-white rounded border border-slate-200">
                    <span className="text-slate-500 block text-[10px]">Baseline Route (G0)</span>
                    <span className="font-bold text-slate-800 font-mono text-sm">{selectedOrigin.G0_distance_m} m</span>
                  </div>
                  <div className="p-2 bg-white rounded border border-slate-200">
                    <span className="text-slate-500 block text-[10px]">Under Restriction (G0+C)</span>
                    <span className="font-bold text-rose-700 font-mono text-sm">{selectedOrigin.G0_C_distance_m} m</span>
                  </div>
                </div>

                {/* Compare this community action */}
                <div className="pt-1">
                  <button
                    onClick={() => onSelectTab("alternatives")}
                    className="w-full py-1.5 px-3 bg-teal-50 hover:bg-teal-100 border border-teal-300 text-teal-800 rounded-lg text-xs font-semibold flex items-center justify-center space-x-1.5 transition"
                  >
                    <GitCompare className="w-3.5 h-3.5 text-teal-600" />
                    <span>Compare this community under alternatives</span>
                  </button>
                </div>
              </div>
            )}

            {/* Origins selector list with sort */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <label className="font-bold text-slate-800 block">Community Access Points ({allOrigins.length}):</label>
                <span className="text-[10px] text-slate-500 font-medium">Ranked by Detour</span>
              </div>
              <div className="space-y-1 max-h-48 overflow-y-auto">
                {[...allOrigins]
                  .sort((a, b) => (b.construction_delta_m || 0) - (a.construction_delta_m || 0))
                  .map(o => {
                    const isSel = o.origin_id === selectedOrigin?.origin_id;
                    const hasDetour = (o.construction_delta_m || 0) > 0;
                    return (
                      <button
                        key={o.origin_id}
                        onClick={() => onSelectOrigin(o.origin_id)}
                        className={`w-full text-left p-2 rounded-lg border flex items-center justify-between transition ${
                          isSel
                            ? "bg-teal-50 border-teal-500 font-bold text-teal-950"
                            : "bg-white border-slate-200 hover:bg-slate-50 text-slate-700"
                        }`}
                      >
                        <div className="truncate pr-2">
                          <span className="block truncate">{o.origin_name}</span>
                          <span className="text-[10px] text-slate-400 font-normal">
                            Baseline: {o.G0_distance_m} m • Status: {o.G0_C_reachable ? "REACHABLE" : "UNREACHABLE"}
                          </span>
                        </div>
                        <span className={`font-mono text-xs whitespace-nowrap ${hasDetour ? "text-rose-600 font-bold" : "text-teal-700"}`}>
                          {hasDetour ? `+${o.construction_delta_m} m` : "0 m"}
                        </span>
                      </button>
                    );
                })}
              </div>
            </div>

            <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-xl text-amber-900 leading-relaxed text-[11px]">
              <b>Non-Emergency Notice:</b> Distances represent deterministic network shortest paths on mapped street geometry. Do not infer resident population counts, emergency response times, or observed congestion.
            </div>

            <button
              onClick={() => onSelectTab("alternatives")}
              className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-semibold rounded-lg flex items-center justify-center space-x-1.5 shadow-sm transition"
            >
              <span>Next: Compare Alternatives</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* STEP 4: COMPARE ALTERNATIVES */}
        {activeTab === "alternatives" && (
          <div className="space-y-3.5">
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <div className="font-bold text-slate-800">Candidate Interventions Ledger</div>
              <p className="text-slate-500 leading-relaxed">
                Compare candidate engineering arrangements. Unapproved candidates can be explored in simulation, but are strictly held to statutory verification safeguards.
              </p>
              
              {/* Category Segmented Control */}
              <div className="grid grid-cols-2 gap-1.5 pt-1">
                <button
                  className="py-1.5 px-2 bg-teal-700 text-white rounded-lg text-[11px] font-bold shadow-xs text-center"
                >
                  Explore Modeled Alternatives ({allCandidates.length})
                </button>
                <button
                  onClick={() => onOpenEvidenceModal()}
                  className="py-1.5 px-2 bg-white hover:bg-slate-100 border border-slate-200 text-slate-600 rounded-lg text-[11px] font-semibold text-center"
                  title="View statutory verification requirements"
                >
                  Verified Implementable Options (0)
                </button>
              </div>
            </div>

            {/* Alternatives Cards with Mini Preview */}
            <div className="space-y-2.5">
              {allCandidates.map(c => {
                const isSel = c.candidate_id === candidate?.candidate_id;
                return (
                  <div
                    key={c.candidate_id}
                    onClick={() => onSelectCandidate(c.candidate_id)}
                    className={`p-3.5 rounded-xl border cursor-pointer transition ${
                      isSel
                        ? "bg-teal-50/70 border-teal-600 ring-1 ring-teal-600 shadow-sm"
                        : "bg-white border-slate-200 hover:bg-slate-50"
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="font-bold text-slate-900 text-xs">{c.name}</div>
                      <span className="font-mono text-[10px] px-2 py-0.5 rounded font-bold bg-amber-100 text-amber-900 border border-amber-300">
                        {c.feasibility_class}
                      </span>
                    </div>

                    <div className="mt-2 space-y-1 text-slate-600">
                      <div>• <b>What changes:</b> {c.description}</div>
                      <div>• <b>Who benefits:</b> Kakkanad West / Civil Station (modeled detour reduction: <span className="font-mono text-teal-700 font-bold">-{c.modeled_metrics.average_detour_reduction_m} m</span>)</div>
                      <div>
                        • <b>Who may be adversely affected:</b> {c.conflict_pedestrian ? "Pedestrian walkway compressed by contraflow lane." : "No identified mode conflict."}
                      </div>
                      <div>• <b>What remains unverified:</b> {c.permission_status} / {c.cost_status}</div>
                    </div>

                    {c.conflict_pedestrian && (
                      <div className="mt-2 p-2 bg-rose-50 border border-rose-200 rounded text-rose-800 text-[11px] flex items-center space-x-1.5">
                        <AlertTriangle className="w-3.5 h-3.5 shrink-0 text-rose-600" />
                        <span>Pedestrian Conflict: Sidewalk width reduced. Mode conflict identified.</span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Strict Statutory Rejection Notice */}
            <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-xl text-amber-900 space-y-1 leading-relaxed">
              <div className="font-bold flex items-center space-x-1.5">
                <AlertTriangle className="w-4 h-4 text-amber-700" />
                <span>Global Feasibility: NO_VERIFIED_OPTION</span>
              </div>
              <p>
                Candidate arrangements can be modeled, but none possess confirmed statutory traffic police clearance or safety staffing BOQ. The system strictly refuses to display unverified candidates as actionable advice.
              </p>
            </div>

            <button
              onClick={() => onSelectTab("summary")}
              className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-semibold rounded-lg flex items-center justify-center space-x-1.5 shadow-sm transition"
            >
              <span>Next: Decision Summary</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* STEP 5: DECISION SUMMARY */}
        {activeTab === "summary" && (
          <div className="space-y-3.5">
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <div className="font-bold text-slate-900 text-xs">Assessed Infrastructure Change</div>
              <p className="text-slate-600 leading-relaxed">
                Hypothetical civil pier foundation workzone along Palarivattom–Kakkanad Road affecting motor vehicle access to Sunrise Hospital.
              </p>
            </div>

            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <div className="font-bold text-slate-900 text-xs">Affected Communities & Tradeoffs</div>
              <div className="space-y-1 text-slate-600">
                <div>• Worst Affected: <b>{summary?.worst_affected_origin}</b> (+{summary?.worst_detour_m} m detour)</div>
                <div>• Average Detour: <b>+{summary?.average_detour_m} m</b> across 6 sampled anchors</div>
                <div>• Tradeoff: Contraflow alternatives recover road distance but compress pedestrian sidewalks and lack traffic police sanction</div>
              </div>
            </div>

            {/* Export Actions */}
            <div className="grid grid-cols-2 gap-2 pt-1">
              <a
                href={`http://localhost:8000/api/report/csv?mode=${selectedTravelMode}`}
                download
                className="py-2 px-3 border border-slate-300 hover:bg-slate-50 rounded-lg text-slate-700 font-semibold flex items-center justify-center space-x-1.5 shadow-sm transition text-xs"
              >
                <FileSpreadsheet className="w-3.5 h-3.5 text-slate-500" />
                <span>Export CSV</span>
              </a>
              <a
                href={`http://localhost:8000/api/report/pdf?mode=${selectedTravelMode}`}
                download
                className="py-2 px-3 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-lg flex items-center justify-center space-x-1.5 shadow-sm transition text-xs"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export PDF</span>
              </a>
            </div>

            {/* Guarded Context-Aware AI Analyst */}
            <div className="p-3.5 bg-teal-50/70 border border-teal-200 rounded-xl space-y-2.5">
              <div className="flex items-center justify-between text-teal-900 font-bold">
                <div className="flex items-center space-x-1.5">
                  <Sparkles className="w-4 h-4 text-teal-700" />
                  <span>Context-Aware AI Analyst</span>
                </div>
                <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded bg-white border border-teal-300 text-teal-800">
                  Status: Grounded Baseline
                </span>
              </div>
              <p className="text-[11px] text-teal-900/80 leading-relaxed">
                Queries are verified against computed shortest-path matrices. When cloud LLM keys are absent, a strictly audited deterministic analytical engine answers without hallucination.
              </p>

              {/* Contextual Prompts */}
              <div className="flex flex-col space-y-1">
                {CONTEXT_QUESTIONS.map((q, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => {
                      setAiQuestion(q);
                      handleAskAI(q);
                    }}
                    className="text-left px-2.5 py-1 bg-white hover:bg-teal-100/60 border border-teal-200 rounded text-[11px] text-teal-950 transition cursor-pointer"
                  >
                    • {q}
                  </button>
                ))}
              </div>

              <div className="flex space-x-1 pt-1">
                <input
                  type="text"
                  value={aiQuestion}
                  onChange={(e) => setAiQuestion(e.target.value)}
                  className="flex-1 px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white focus:outline-none"
                  placeholder="Ask decision question..."
                />
                <button
                  type="button"
                  onClick={() => handleAskAI()}
                  disabled={aiLoading}
                  className="px-3 py-1.5 bg-teal-700 hover:bg-teal-800 text-white rounded text-xs font-bold flex items-center justify-center cursor-pointer"
                >
                  <Send className="w-3.5 h-3.5" />
                </button>
              </div>

              {aiLoading && (
                <div className="p-2 text-slate-500 text-xs italic">
                  Evaluating queries against shortest-path matrix...
                </div>
              )}

              {aiAnswer && (
                <div className="p-2.5 bg-white border border-teal-300 rounded text-slate-800 leading-relaxed text-[11px]">
                  <b>Analysis:</b> {aiAnswer}
                </div>
              )}

              {aiViolations.length > 0 && (
                <div className="p-2 bg-rose-50 border border-rose-200 text-rose-800 rounded text-[11px]">
                  <b>Filter Interception:</b> {aiViolations.join("; ")}
                </div>
              )}
            </div>
          </div>
        )}

        {/* EXPANDABLE TECHNICAL DETAILS DRAWER */}
        {showTechnicalDetails && (
          <div className="mt-4 p-3.5 bg-slate-900 text-slate-200 rounded-xl space-y-3 font-mono text-[11px]">
            <div className="flex items-center justify-between text-teal-400 font-bold border-b border-slate-800 pb-1">
              <span>Technical Graph Algebra</span>
              <button onClick={onOpenEvidenceModal} className="text-teal-300 underline text-[10px]">
                Open Evidence
              </button>
            </div>
            <div>• Study Area: {metadata?.name || "Kakkanad Pilot"} ({metadata?.snapshot_date || "ODbL"})</div>
            <div className="flex items-center space-x-2 pt-1 border-t border-slate-800">
              <span>• Graph State:</span>
              {(["G0", "G0_C", "G0_P_C_M"] as AnalyticalState[]).map(st => (
                <button
                  key={st}
                  onClick={() => onSelectState(st)}
                  className={`px-1.5 py-0.5 rounded text-[10px] ${selectedState === st ? "bg-teal-700 text-white font-bold" : "bg-slate-800 text-slate-400"}`}
                >
                  {st}
                </button>
              ))}
            </div>
            <div>• Run Hash: {runId || "N/A"}</div>
            <div>• Invariant: G0+P - G0 = {selectedOrigin?.proposal_delta_m || 0} m</div>
            <div>• Active Disruption Ways: [{activeDisruptedWayIds.join(", ")}]</div>
            <div>• CRS: EPSG:4326 / Projected: EPSG:32643</div>
            <div>• Referential Integrity: 0 missing refs across 19,582 nodes</div>
          </div>
        )}
      </div>
    </div>
  );
};

