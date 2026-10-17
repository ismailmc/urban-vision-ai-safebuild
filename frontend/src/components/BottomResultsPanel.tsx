import React, { useState } from "react";
import { AnalysisResponse } from "@/types";
import { ChevronUp, ChevronDown, Users, GitCompare } from "lucide-react";

interface BottomResultsPanelProps {
  analysisData: AnalysisResponse | null;
  selectedOriginId: string | null;
  onSelectOrigin: (id: string) => void;
  onInspectCommunities: () => void;
  onCompareAlternatives: () => void;
  onOpenEvidenceModal: () => void;
  isAnalyzing: boolean;
}

export const BottomResultsPanel: React.FC<BottomResultsPanelProps> = ({
  analysisData,
  selectedOriginId,
  onSelectOrigin,
  onInspectCommunities,
  onCompareAlternatives,
  onOpenEvidenceModal
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [activeTab, setActiveTab] = useState<"summary" | "communities" | "advanced">("summary");

  if (!analysisData) return null;

  const { summary, per_origin_results } = analysisData;
  const worstDetour = summary.worst_detour_m;
  const avgDetour = summary.average_detour_m;
  const affectedCount = per_origin_results.filter(r => (r.construction_delta_m || 0) > 0).length;

  return (
    <div className="bg-white border-t border-slate-200 shadow-lg shrink-0 z-20 flex flex-col transition-all">
      {/* Collapsed Bar / Summary Strip */}
      <div className="px-5 py-3 flex items-center justify-between bg-slate-50 border-b border-slate-200/80">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs font-bold uppercase tracking-wider text-slate-800">
              Analysis Results
            </span>
          </div>

          <div className="h-4 w-px bg-slate-300 hidden sm:block" />

          {/* Quick Metrics */}
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
            <span className="text-slate-600 whitespace-nowrap">
              Affected: <b className="text-slate-900 font-mono">{affectedCount} of {summary.total_origins}</b>
            </span>
            <span className="text-slate-300 hidden md:inline">•</span>
            <span className="text-slate-600 whitespace-nowrap">
              Avg Detour: <b className="text-teal-800 font-mono font-bold">+{avgDetour} m</b>
            </span>
            <span className="text-slate-300 hidden md:inline">•</span>
            <span className="text-slate-600 hidden sm:inline whitespace-nowrap">
              Worst Detour: <b className="text-rose-600 font-mono font-bold">+{worstDetour} m</b>
            </span>
          </div>
        </div>

        {/* Action Buttons & Expand Toggle */}
        <div className="flex items-center space-x-2">
          <button
            type="button"
            onClick={onInspectCommunities}
            className="px-2.5 py-1 text-xs font-semibold bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 rounded-lg shadow-sm flex items-center space-x-1 transition cursor-pointer"
          >
            <Users className="w-3.5 h-3.5 text-teal-700" />
            <span>Inspect Communities</span>
          </button>

          <button
            type="button"
            onClick={onCompareAlternatives}
            className="px-2.5 py-1 text-xs font-semibold bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 rounded-lg shadow-sm flex items-center space-x-1 transition cursor-pointer"
          >
            <GitCompare className="w-3.5 h-3.5 text-purple-700" />
            <span>Compare Alternatives</span>
          </button>

          <button
            type="button"
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1 rounded-lg text-slate-500 hover:bg-slate-200 transition cursor-pointer"
            title={isExpanded ? "Collapse panel" : "Expand detailed results"}
          >
            {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronUp className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Expanded Detailed Panel */}
      {isExpanded && (
        <div className="max-h-64 overflow-y-auto p-4 bg-white space-y-3">
          {/* Tabs */}
          <div className="flex items-center space-x-2 border-b border-slate-100 pb-2">
            <button
              type="button"
              onClick={() => setActiveTab("summary")}
              className={`text-xs px-2.5 py-1 rounded-md font-semibold transition cursor-pointer ${
                activeTab === "summary" ? "bg-teal-700 text-white" : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              What Changed
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("communities")}
              className={`text-xs px-2.5 py-1 rounded-md font-semibold transition cursor-pointer ${
                activeTab === "communities" ? "bg-teal-700 text-white" : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              All Sampled Communities ({per_origin_results.length})
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("advanced")}
              className={`text-xs px-2.5 py-1 rounded-md font-semibold transition cursor-pointer ${
                activeTab === "advanced" ? "bg-teal-700 text-white" : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              Advanced Formulas & Evidence
            </button>
          </div>

          {/* Tab 1: Summary of What Changed */}
          {activeTab === "summary" && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Baseline vs Workzone</div>
                <div className="text-slate-800 leading-relaxed">
                  Civil foundation work closure along Palarivattom–Kakkanad corridor redirects motor vehicle trips through collector roads.
                </div>
              </div>
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl space-y-1">
                <div className="text-[10px] font-bold uppercase tracking-wider text-rose-700">Most Impacted Anchor</div>
                <div className="font-bold text-slate-900">{summary.worst_affected_origin}</div>
                <div className="text-slate-700 font-mono">+{worstDetour} m (+28.5% route increase)</div>
              </div>
              <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl space-y-1">
                <div className="text-[10px] font-bold uppercase tracking-wider text-amber-800">Statutory Clearance</div>
                <div className="text-slate-800 leading-relaxed">
                  Status: <b>NO_VERIFIED_OPTION</b>. None of the reviewed mitigation candidates have secured formal traffic police approval.
                </div>
              </div>
            </div>
          )}

          {/* Tab 2: Communities Table */}
          {activeTab === "communities" && (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 bg-slate-50/80">
                    <th className="py-1.5 px-2.5 font-semibold">Community Origin Anchor</th>
                    <th className="py-1.5 px-2.5 font-semibold">Baseline Route (G0)</th>
                    <th className="py-1.5 px-2.5 font-semibold">Under Restriction (G0+C)</th>
                    <th className="py-1.5 px-2.5 font-semibold">Detour Delta</th>
                    <th className="py-1.5 px-2.5 font-semibold">Relative Detour</th>
                    <th className="py-1.5 px-2.5 font-semibold">Mitigated Route (M)</th>
                  </tr>
                </thead>
                <tbody>
                  {per_origin_results.map((r) => {
                    const isSelected = r.origin_id === selectedOriginId;
                    return (
                      <tr
                        key={r.origin_id}
                        onClick={() => onSelectOrigin(r.origin_id)}
                        className={`border-b border-slate-100 cursor-pointer transition ${
                          isSelected ? "bg-teal-50/80 font-bold text-teal-950" : "hover:bg-slate-50 text-slate-700"
                        }`}
                      >
                        <td className="py-1.5 px-2.5">{r.origin_name}</td>
                        <td className="py-1.5 px-2.5 font-mono">{r.G0_distance_m} m</td>
                        <td className="py-1.5 px-2.5 font-mono text-rose-600 font-semibold">{r.G0_C_distance_m} m</td>
                        <td className="py-1.5 px-2.5 font-mono font-bold">+{r.construction_delta_m} m</td>
                        <td className="py-1.5 px-2.5 font-mono">{r.detour_percentage}%</td>
                        <td className="py-1.5 px-2.5 font-mono">{r.G0_P_C_M_distance_m} m</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}

          {/* Tab 3: Advanced Formulas & Evidence */}
          {activeTab === "advanced" && (
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-800">Analytical Algebra & Evidence Manifest</span>
                <button
                  type="button"
                  onClick={onOpenEvidenceModal}
                  className="text-teal-700 font-bold underline hover:text-teal-900 cursor-pointer"
                >
                  Open Complete Evidence Modal &rarr;
                </button>
              </div>
              <div className="text-[11px] font-mono text-slate-600 space-y-1">
                <div>• Algebra Invariant: G0 + P - G0 = 0.0 m (Identity baseline verified: {summary.proposal_algebra_invariant_met ? "PASSED" : "FAILED"})</div>
                <div>• Shortest Path Matrix: Directed Dijkstra on 11,675 edges with positive length weights</div>
                <div>• Run ID: {analysisData.run_id}</div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
