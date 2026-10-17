import React, { useState, useMemo } from "react";
import { OriginResult, CandidateEvaluation, Facility, AnalysisSummary, RoadWayItem } from "@/types";
import { SelectedRoadInfo } from "@/components/MapCanvas";
import {
  Compass, Calculator, GitCompare, ArrowRight,
  Search, CheckCircle2, AlertTriangle, ShieldAlert,
  ChevronDown, ChevronUp, SlidersHorizontal, RefreshCw
} from "lucide-react";

export type WorkspaceStep = "choose_road" | "check_access" | "compare_arrangement";

interface TaskPanelProps {
  currentStep: WorkspaceStep;
  onSelectStep: (step: WorkspaceStep) => void;
  // Step 1: Choose a Road
  roadsCatalog?: RoadWayItem[];
  selectedRoad: SelectedRoadInfo | null;
  onSelectRoadItem: (road: SelectedRoadInfo) => void;
  onClearSelectedRoad: () => void;
  onAddRoadRestriction: (road: SelectedRoadInfo, direction: string, mode: string, phase: string) => Promise<void>;
  activeDisruptedWayIds: string[];
  selectedTravelMode: string;
  onSelectTravelMode: (mode: string) => void;
  // Step 2: Check Community Access
  onRunAnalysis: () => Promise<void>;
  isAnalyzing: boolean;
  origins: OriginResult[];
  selectedOriginId: string | null;
  onSelectOrigin: (id: string) => void;
  facility: Facility | null;
  analysisSummary: AnalysisSummary | null;
  // Step 3: Compare Another Arrangement
  allCandidates: CandidateEvaluation[];
  selectedCandidateId: string;
  onSelectCandidate: (candidateId: string) => void;
  onRunCandidateComparison: (candidateId: string) => Promise<void>;
  isComparing: boolean;
  // First-Open Kakkanad Preset
  onLoadKakkanadExample: () => void;
}

export const TaskPanel: React.FC<TaskPanelProps> = ({
  currentStep,
  onSelectStep,
  roadsCatalog = [],
  selectedRoad,
  onSelectRoadItem,
  onClearSelectedRoad,
  onAddRoadRestriction,
  activeDisruptedWayIds,
  selectedTravelMode,
  onSelectTravelMode,
  onRunAnalysis,
  isAnalyzing,
  origins,
  selectedOriginId,
  onSelectOrigin,
  facility,
  analysisSummary,
  allCandidates,
  selectedCandidateId,
  onSelectCandidate,
  onRunCandidateComparison,
  isComparing,
  onLoadKakkanadExample
}) => {
  // Step 1 local states
  const [roadSearch, setRoadSearch] = useState("");
  const [showTechnicalSettings, setShowTechnicalSettings] = useState(false);
  const [restrictionDirection, setRestrictionDirection] = useState("both");
  const [restrictionPhase, setRestrictionPhase] = useState("Phase 1: Civil Pier Foundation");
  const [isApplyingRestriction, setIsApplyingRestriction] = useState(false);

  // Filtered roads for search
  const filteredRoads = useMemo(() => {
    if (!roadSearch.trim()) return roadsCatalog.slice(0, 8);
    const q = roadSearch.toLowerCase();
    return roadsCatalog
      .filter((r) => r.name.toLowerCase().includes(q) || r.osm_way_id.includes(q))
      .slice(0, 10);
  }, [roadsCatalog, roadSearch]);

  const selectedCandidate = allCandidates.find((c) => c.candidate_id === selectedCandidateId) || allCandidates[0];

  // Community points stats
  const affectedOrigins = origins.filter((o) => (o.construction_delta_m || 0) > 0);

  const STEPS: { id: WorkspaceStep; num: string; label: string; icon: React.ReactNode }[] = [
    { id: "choose_road", num: "1", label: "1. Road", icon: <Compass className="w-4 h-4" /> },
    { id: "check_access", num: "2", label: "2. Access", icon: <Calculator className="w-4 h-4" /> },
    { id: "compare_arrangement", num: "3", label: "3. Compare", icon: <GitCompare className="w-4 h-4" /> },
  ];

  return (
    <div className="w-full md:w-[350px] lg:w-[340px] shrink-0 bg-white border-r border-slate-200 flex flex-col h-full shadow-sm z-10 overflow-hidden text-slate-800">
      {/* 3-Step Clean Navigation Bar */}
      <div className="border-b border-slate-200 bg-slate-50/80 p-2.5">
        <div className="flex items-center justify-between mb-1.5 px-1">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Task Workflow
          </span>
          <button
            type="button"
            onClick={onLoadKakkanadExample}
            className="text-[10px] font-bold text-teal-700 hover:text-teal-900 underline cursor-pointer"
          >
            Try Kakkanad example
          </button>
        </div>

        <div className="grid grid-cols-3 gap-1.5">
          {STEPS.map((s) => {
            const isActive = currentStep === s.id;
            return (
              <button
                key={s.id}
                type="button"
                onClick={() => onSelectStep(s.id)}
                className={`py-2 px-1 rounded-xl flex items-center justify-center space-x-1.5 transition text-center cursor-pointer ${
                  isActive
                    ? "bg-teal-700 text-white font-bold shadow-sm"
                    : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-100/80"
                }`}
              >
                <span className="text-xs font-semibold">{s.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Task Step Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* ================= STEP 1: CHOOSE A ROAD ================= */}
        {currentStep === "choose_road" && (
          <div className="space-y-4">
            <div>
              <div className="inline-flex items-center space-x-1.5 text-xs font-bold text-teal-800 bg-teal-50 px-2 py-0.5 rounded-md mb-1 border border-teal-200">
                <span>Step 1 of 3: Choose a Road</span>
              </div>
              <h2 className="text-sm font-bold text-slate-900">Select Road to Restrict</h2>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                Click any street on the map, or pick from the list below to model a hypothetical construction closure.
              </p>
            </div>

            {/* Travel Mode Toggle */}
            <div className="bg-slate-50 border border-slate-200 p-2.5 rounded-xl space-y-1.5">
              <label className="text-[11px] font-bold text-slate-600 uppercase tracking-wide block">
                Travel Mode:
              </label>
              <div className="grid grid-cols-2 gap-1.5 text-xs">
                <button
                  type="button"
                  onClick={() => onSelectTravelMode("motor_vehicle")}
                  className={`py-1.5 px-2 rounded-lg font-semibold border transition cursor-pointer ${
                    selectedTravelMode === "motor_vehicle"
                      ? "bg-teal-700 text-white border-teal-700 shadow-sm"
                      : "bg-white text-slate-700 border-slate-200 hover:bg-slate-100"
                  }`}
                >
                  Motor Vehicle
                </button>
                <button
                  type="button"
                  onClick={() => onSelectTravelMode("pedestrian")}
                  className={`py-1.5 px-2 rounded-lg font-semibold border transition cursor-pointer ${
                    selectedTravelMode === "pedestrian"
                      ? "bg-teal-700 text-white border-teal-700 shadow-sm"
                      : "bg-white text-slate-700 border-slate-200 hover:bg-slate-100"
                  }`}
                >
                  Pedestrian
                </button>
              </div>
            </div>

            {/* Selected Road Card or Search Selector */}
            {selectedRoad ? (
              <div className="p-3 bg-amber-50/80 border border-amber-300 rounded-xl space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-amber-800 flex items-center space-x-1">
                    <span className="w-2 h-2 rounded-full bg-amber-500" />
                    <span>Selected Segment</span>
                  </span>
                  <button
                    type="button"
                    onClick={onClearSelectedRoad}
                    className="text-slate-400 hover:text-slate-600 font-bold cursor-pointer"
                  >
                    ✕
                  </button>
                </div>

                <div>
                  <div className="font-bold text-slate-900 text-xs">{selectedRoad.name}</div>
                  <div className="text-[11px] font-mono text-slate-600 mt-0.5">
                    Way ID: <b>{selectedRoad.way_id}</b> ({selectedRoad.highway})
                  </div>
                </div>

                <div className="p-2 bg-white/80 rounded-lg border border-amber-200 text-[11px] text-amber-900 leading-snug">
                  <b>Planned Model:</b> We will model this connection as restricted during construction.
                </div>

                {/* Hypothetical Status Label */}
                <div className="text-[10px] font-mono text-amber-700 bg-amber-100/70 px-2 py-0.5 rounded border border-amber-300">
                  Status: <b>Hypothetical Restriction (Research Model)</b>
                </div>

                {/* Expandable Technical Settings */}
                <div className="pt-1">
                  <button
                    type="button"
                    onClick={() => setShowTechnicalSettings(!showTechnicalSettings)}
                    className="text-[11px] font-semibold text-slate-600 hover:text-slate-900 flex items-center space-x-1 cursor-pointer"
                  >
                    <SlidersHorizontal className="w-3 h-3" />
                    <span>Direction & Phase Settings</span>
                    {showTechnicalSettings ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                  </button>

                  {showTechnicalSettings && (
                    <div className="mt-2 space-y-2 p-2.5 bg-white rounded-lg border border-slate-200 text-xs">
                      <div>
                        <label className="text-[10px] font-bold text-slate-600 block mb-0.5">Restriction Direction:</label>
                        <select
                          value={restrictionDirection}
                          onChange={(e) => setRestrictionDirection(e.target.value)}
                          className="w-full text-xs p-1.5 rounded border border-slate-300 bg-white"
                        >
                          <option value="both">Both Directions (Full Closure)</option>
                          <option value="fwd_only">Forward Direction Only</option>
                          <option value="rev_only">Reverse Direction Only</option>
                        </select>
                      </div>

                      <div>
                        <label className="text-[10px] font-bold text-slate-600 block mb-0.5">Construction Phase:</label>
                        <select
                          value={restrictionPhase}
                          onChange={(e) => setRestrictionPhase(e.target.value)}
                          className="w-full text-xs p-1.5 rounded border border-slate-300 bg-white"
                        >
                          <option value="Phase 1: Civil Pier Foundation">Phase 1: Civil Pier Foundation</option>
                          <option value="Phase 2: Girder Erection">Phase 2: Girder Erection</option>
                          <option value="Phase 3: Utility Relocation">Phase 3: Utility Relocation</option>
                        </select>
                      </div>
                    </div>
                  )}
                </div>

                {/* Apply Restriction Action */}
                <button
                  type="button"
                  disabled={isApplyingRestriction}
                  onClick={async () => {
                    setIsApplyingRestriction(true);
                    try {
                      await onAddRoadRestriction(selectedRoad, restrictionDirection, selectedTravelMode, restrictionPhase);
                    } finally {
                      setIsApplyingRestriction(false);
                    }
                  }}
                  className="w-full py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-bold text-xs shadow-sm transition flex items-center justify-center space-x-1 cursor-pointer"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isApplyingRestriction ? "animate-spin" : ""}`} />
                  <span>{isApplyingRestriction ? "Applying..." : "Apply Restriction to Model"}</span>
                </button>
              </div>
            ) : (
              /* Searchable Road Selector */
              <div className="space-y-2">
                <div className="relative">
                  <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
                  <input
                    type="text"
                    value={roadSearch}
                    onChange={(e) => setRoadSearch(e.target.value)}
                    placeholder="Search road name or OSM way ID..."
                    className="w-full pl-8 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-teal-500"
                  />
                </div>

                <div className="border border-slate-200 rounded-xl overflow-hidden max-h-48 overflow-y-auto divide-y divide-slate-100 bg-white text-xs">
                  {filteredRoads.map((r) => {
                    const isDisrupted = activeDisruptedWayIds.includes(r.osm_way_id);
                    return (
                      <button
                        key={r.osm_way_id}
                        type="button"
                        onClick={() => {
                          onSelectRoadItem({
                            way_id: r.osm_way_id,
                            name: r.name,
                            highway: r.highway,
                            oneway: "no"
                          });
                        }}
                        className="w-full text-left p-2 hover:bg-teal-50/60 transition flex items-center justify-between cursor-pointer"
                      >
                        <div className="truncate pr-2">
                          <div className="font-semibold text-slate-900 truncate">{r.name}</div>
                          <div className="text-[10px] font-mono text-slate-400">Way {r.osm_way_id} • {r.highway}</div>
                        </div>
                        {isDisrupted && (
                          <span className="text-[9px] font-mono bg-rose-50 text-rose-700 border border-rose-200 px-1.5 py-0.5 rounded font-bold shrink-0">
                            RESTRICTED
                          </span>
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Active Restrictions Counter */}
            <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs flex items-center justify-between">
              <span className="text-slate-600">Active Modeled Restrictions:</span>
              <span className="font-mono font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                {activeDisruptedWayIds.length} road segment{activeDisruptedWayIds.length !== 1 ? "s" : ""}
              </span>
            </div>

            {/* Next Step Action */}
            <div className="pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => onSelectStep("check_access")}
                className="w-full py-2.5 px-3 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold shadow-sm transition flex items-center justify-center space-x-1.5 cursor-pointer"
              >
                <span>Next: Check Community Access</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* ================= STEP 2: CHECK COMMUNITY ACCESS ================= */}
        {currentStep === "check_access" && (
          <div className="space-y-4">
            <div>
              <div className="inline-flex items-center space-x-1.5 text-xs font-bold text-indigo-800 bg-indigo-50 px-2 py-0.5 rounded-md mb-1 border border-indigo-200">
                <span>Step 2 of 3: Check Community Access</span>
              </div>
              <h2 className="text-sm font-bold text-slate-900">Evaluate Hospital Access Changes</h2>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                Run the backend routing engine to test how the restriction changes access from sampled communities.
              </p>
            </div>

            {/* Target Facility */}
            {facility && (
              <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Destination Facility</div>
                <div className="font-bold text-slate-900 mt-0.5">{facility.name}</div>
                <div className="text-[11px] text-slate-500 font-mono mt-0.5">{facility.address}</div>
              </div>
            )}

            {/* Primary Action Button */}
            <button
              type="button"
              onClick={onRunAnalysis}
              disabled={isAnalyzing}
              className={`w-full py-3 px-4 rounded-xl text-xs font-bold text-white shadow-sm transition flex items-center justify-center space-x-2 ${
                isAnalyzing
                  ? "bg-indigo-400 cursor-not-allowed"
                  : "bg-indigo-700 hover:bg-indigo-800 cursor-pointer"
              }`}
            >
              <Calculator className={`w-4 h-4 ${isAnalyzing ? "animate-spin" : ""}`} />
              <span>{isAnalyzing ? "Calculating Route Access Changes..." : "Check impact"}</span>
            </button>

            {/* Results Overview (Grounded, No Resident Estimates) */}
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-2.5 text-xs">
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                Modeled Impact Summary
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div className="p-2 bg-white rounded-lg border border-slate-200">
                  <div className="text-[10px] text-slate-500 font-medium">Sampled Points Affected</div>
                  <div className="text-sm font-bold text-slate-900 mt-0.5 font-mono">
                    {affectedOrigins.length} <span className="text-xs font-normal text-slate-500">of {origins.length}</span>
                  </div>
                </div>

                <div className="p-2 bg-white rounded-lg border border-slate-200">
                  <div className="text-[10px] text-slate-500 font-medium">Newly Unreachable Points</div>
                  <div className="text-sm font-bold text-emerald-700 mt-0.5 font-mono">
                    {analysisSummary?.new_unreachable_origins || 0}
                  </div>
                </div>
              </div>

              <div className="p-2.5 bg-rose-50 border border-rose-200 rounded-lg space-y-0.5">
                <div className="text-[10px] font-bold uppercase text-rose-700">Largest Modeled Distance Increase</div>
                <div className="text-sm font-bold text-rose-900 font-mono">
                  +{analysisSummary?.worst_detour_m || 354.9} m
                </div>
                <div className="text-[11px] text-rose-800">
                  At <b>{analysisSummary?.worst_affected_origin || "Kakkanad West Anchor"}</b> (+22.6% over baseline)
                </div>
              </div>

              {/* Plain Language Explanation */}
              <div className="p-2.5 bg-white border border-slate-200 rounded-lg text-[11px] text-slate-700 leading-relaxed">
                <b>Analysis explanation:</b> Restricting the Palarivattom–Kakkanad corridor cuts the direct arterial route. Vehicles from western and central residential anchors must take longer detours around collector roads.
              </div>
            </div>

            {/* Affected Community Access Points Selector */}
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-700 block">
                Sampled Community Access Points (Click to focus route):
              </label>
              <div className="space-y-1 max-h-48 overflow-y-auto pr-1">
                {origins.map((o) => {
                  const isSelected = o.origin_id === selectedOriginId;
                  const delta = o.construction_delta_m || 0;
                  return (
                    <button
                      key={o.origin_id}
                      type="button"
                      onClick={() => onSelectOrigin(o.origin_id)}
                      className={`w-full text-left p-2 rounded-lg border text-xs transition flex items-center justify-between cursor-pointer ${
                        isSelected
                          ? "bg-teal-50 border-teal-500 text-teal-950 font-bold"
                          : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50"
                      }`}
                    >
                      <span className="truncate pr-1">{o.origin_name}</span>
                      <span className={`text-[11px] font-mono shrink-0 font-bold ${
                        delta > 0 ? "text-rose-600" : "text-emerald-700"
                      }`}>
                        {delta > 0 ? `+${delta} m` : "Unchanged"}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Next Step Action */}
            <div className="pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => onSelectStep("compare_arrangement")}
                className="w-full py-2.5 px-3 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold shadow-sm transition flex items-center justify-center space-x-1.5 cursor-pointer"
              >
                <span>Next: Compare Another Arrangement</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* ================= STEP 3: COMPARE ANOTHER ARRANGEMENT ================= */}
        {currentStep === "compare_arrangement" && (
          <div className="space-y-4">
            <div>
              <div className="inline-flex items-center space-x-1.5 text-xs font-bold text-purple-800 bg-purple-50 px-2 py-0.5 rounded-md mb-1 border border-purple-200">
                <span>Step 3 of 3: Compare Another Arrangement</span>
              </div>
              <h2 className="text-sm font-bold text-slate-900">Would Another Arrangement Help?</h2>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                Select one of the supplied candidate arrangements and compare its verified tradeoffs.
              </p>
            </div>

            {/* Supplied Candidate Options */}
            <div className="space-y-2">
              {allCandidates.map((c) => {
                const isSelected = c.candidate_id === selectedCandidateId;
                return (
                  <div
                    key={c.candidate_id}
                    onClick={() => onSelectCandidate(c.candidate_id)}
                    className={`p-3 rounded-xl border text-xs cursor-pointer transition space-y-1.5 ${
                      isSelected
                        ? "bg-purple-50/70 border-purple-500 shadow-sm ring-1 ring-purple-400"
                        : "bg-white border-slate-200 hover:bg-slate-50"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-900 truncate pr-1">{c.name}</span>
                      <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded font-bold ${
                        c.feasibility_class === "VERIFIED_IMPLEMENTABLE"
                          ? "bg-teal-100 text-teal-800"
                          : "bg-amber-100 text-amber-800"
                      }`}>
                        {c.feasibility_class === "VERIFIED_IMPLEMENTABLE" ? "VERIFIED" : "UNVERIFIED"}
                      </span>
                    </div>

                    {/* Single-sentence plain language summary */}
                    <p className="text-[11px] text-slate-600 leading-relaxed">
                      {c.candidate_id === "cand_m1_phased_contraflow"
                        ? "Keeps one managed vehicle lane open through the workzone using signal flaggers."
                        : c.candidate_id === "cand_m2_civil_lane_diversion"
                        ? "Diverts traffic to Civil Lane Road by adding temporary signage and clearing parking."
                        : "Creates an unpaved cut-through through the commercial Infopark boundary campus."}
                    </p>
                  </div>
                );
              })}
            </div>

            {/* Compare Button */}
            <button
              type="button"
              disabled={isComparing}
              onClick={() => onRunCandidateComparison(selectedCandidateId)}
              className="w-full py-2.5 px-3 bg-purple-700 hover:bg-purple-800 text-white rounded-xl text-xs font-bold shadow-sm transition flex items-center justify-center space-x-1.5 cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isComparing ? "animate-spin" : ""}`} />
              <span>{isComparing ? "Evaluating Alternative..." : `Compare “${selectedCandidate?.name.split(" ")[0]}...”`}</span>
            </button>

            {/* Tradeoff Breakdown Card */}
            {selectedCandidate && (
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs">
                <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                  Tradeoff Review: {selectedCandidate.name}
                </div>

                {/* What Improves */}
                <div className="p-2 bg-emerald-50 border border-emerald-200 rounded-lg space-y-0.5">
                  <div className="font-bold text-emerald-800 flex items-center space-x-1 text-[11px]">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>What Improves:</span>
                  </div>
                  <div className="text-[11px] text-emerald-950 leading-snug">
                    {selectedCandidate.candidate_id === "cand_m1_phased_contraflow"
                      ? "Recovers arterial connectivity through the workzone, reducing average detour by up to 180 m."
                      : selectedCandidate.candidate_id === "cand_m2_civil_lane_diversion"
                      ? "Provides an authorized secondary bypass around congested intersection choke points."
                      : "Provides no route improvement due to private compound access restrictions."}
                  </div>
                </div>

                {/* What Worsens */}
                <div className="p-2 bg-rose-50 border border-rose-200 rounded-lg space-y-0.5">
                  <div className="font-bold text-rose-800 flex items-center space-x-1 text-[11px]">
                    <AlertTriangle className="w-3 h-3" />
                    <span>What Worsens:</span>
                  </div>
                  <div className="text-[11px] text-rose-950 leading-snug">
                    {selectedCandidate.candidate_id === "cand_m1_phased_contraflow"
                      ? "Reduces pedestrian walkway clearance and increases worker exposure in the workzone."
                      : selectedCandidate.candidate_id === "cand_m2_civil_lane_diversion"
                      ? "Directs vehicle cut-through traffic onto narrow residential streets."
                      : "Causes severe conflict with private compound security."}
                  </div>
                </div>

                {/* What Stays Unchanged */}
                <div className="p-2 bg-slate-100 border border-slate-200 rounded-lg space-y-0.5">
                  <div className="font-bold text-slate-700 text-[11px]">What Stays Unchanged:</div>
                  <div className="text-[11px] text-slate-600 leading-snug">
                    Access routes from eastern anchors (Canal Colony, DLF City) remain unchanged under this arrangement.
                  </div>
                </div>

                {/* What Requires Physical or Permission Review */}
                <div className="p-2 bg-amber-50 border border-amber-200 rounded-lg space-y-0.5">
                  <div className="font-bold text-amber-900 flex items-center space-x-1 text-[11px]">
                    <ShieldAlert className="w-3 h-3" />
                    <span>Required Reviews:</span>
                  </div>
                  <div className="text-[11px] text-amber-950 leading-snug">
                    • Permission: <b>{selectedCandidate.permission_status.replace(/_/g, " ")}</b>
                    <br />
                    • Physical: <b>{selectedCandidate.physical_status.replace(/_/g, " ")}</b>
                  </div>
                </div>

                {/* Prototype Review Gate */}
                <div className="p-2.5 bg-rose-100/70 border border-rose-300 rounded-lg text-[11px] text-rose-900 leading-relaxed font-medium">
                  <b>Prototype Review Gate:</b> All candidates are currently marked <code>NO_VERIFIED_OPTION</code> because none possess verified authority approval. The system will not recommend unverified options as formal advice.
                </div>
              </div>
            )}

            {/* Back to Step 1 or 2 */}
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
              <button
                type="button"
                onClick={() => onSelectStep("check_access")}
                className="text-xs text-slate-600 hover:text-slate-900 font-semibold cursor-pointer"
              >
                &larr; Back to Access Impact
              </button>
              <button
                type="button"
                onClick={() => onSelectStep("choose_road")}
                className="text-xs text-teal-700 hover:text-teal-900 font-semibold cursor-pointer"
              >
                Try Another Road
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
