import React, { useState } from "react";
import { OriginResult, CandidateEvaluation, AnalyticalState, StudyMetadata, Facility } from "@/types";
import { askAIAnalyst } from "@/lib/api";
import { CheckCircle2, AlertTriangle, Bot, FileText } from "lucide-react";

interface EvidenceInspectorProps {
  selectedOrigin: OriginResult | null;
  selectedState: AnalyticalState;
  metadata: StudyMetadata | null;
  facility: Facility | null;
  candidate: CandidateEvaluation | null;
  allCandidates: CandidateEvaluation[];
  onSelectCandidate: (candidateId: string) => void;
  onOpenEvidenceModal: () => void;
  runId: string | null;
}

export const EvidenceInspector: React.FC<EvidenceInspectorProps> = ({
  selectedOrigin,
  selectedState,
  
  facility,
  candidate,
  allCandidates,
  onSelectCandidate,
  onOpenEvidenceModal,
  runId
}) => {
  const [activeTab, setActiveTab] = useState<"origin" | "candidate" | "ai">("origin");
  const [aiQuestion, setAiQuestion] = useState("Explain the accessibility impact and alternatives.");
  const [aiAnswer, setAiAnswer] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiViolations, setAiViolations] = useState<string[]>([]);

  const handleAskAI = async () => {
    setAiLoading(true);
    setAiAnswer(null);
    setAiViolations([]);
    try {
      const res = await askAIAnalyst(aiQuestion);
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

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-3.5 shadow-sm flex flex-col h-full text-slate-800">
      {/* Top Header & Tabs */}
      <div className="flex items-center justify-between border-b border-slate-200 mb-3 pb-2">
        <div className="flex space-x-3 text-xs font-medium">
          <button
            onClick={() => setActiveTab("origin")}
            className={`pb-1 border-b-2 transition-colors ${
              activeTab === "origin" ? "border-teal-600 text-teal-800 font-bold" : "border-transparent text-slate-500 hover:text-slate-800"
            }`}
          >
            Community Lens
          </button>
          <button
            onClick={() => setActiveTab("candidate")}
            className={`pb-1 border-b-2 transition-colors ${
              activeTab === "candidate" ? "border-teal-600 text-teal-800 font-bold" : "border-transparent text-slate-500 hover:text-slate-800"
            }`}
          >
            Alternatives (Optimizer)
          </button>
          <button
            onClick={() => setActiveTab("ai")}
            className={`pb-1 border-b-2 transition-colors flex items-center space-x-1 ${
              activeTab === "ai" ? "border-teal-600 text-teal-800 font-bold" : "border-transparent text-slate-500 hover:text-slate-800"
            }`}
          >
            <Bot className="w-3.5 h-3.5" />
            <span>Guarded AI</span>
          </button>
        </div>

        {/* View Evidence Action */}
        <button
          onClick={onOpenEvidenceModal}
          className="text-[11px] font-semibold text-teal-700 hover:text-teal-900 flex items-center space-x-1 bg-teal-50 px-2 py-0.5 rounded border border-teal-200"
          title="Inspect full dataset and calculation provenance"
        >
          <FileText className="w-3 h-3" />
          <span>View Evidence</span>
        </button>
      </div>

      {/* Tab 1: Community Lens */}
      {activeTab === "origin" && selectedOrigin && (
        <div className="space-y-3 text-xs overflow-y-auto flex-1">
          <div>
            <div className="font-bold text-slate-900 text-sm">{selectedOrigin.origin_name}</div>
            <div className="text-slate-500 text-[11px] mt-0.5">
              Sampling: {selectedOrigin.sampling_method || "Public settlement anchor"}
            </div>
            <div className="text-slate-500 text-[11px]">
              Destination: <span className="font-semibold text-slate-700">{facility?.name || selectedOrigin.destination_name}</span>
            </div>
          </div>

          {/* Metric Cards */}
          <div className="grid grid-cols-2 gap-2 bg-slate-50 p-2.5 rounded border border-slate-200">
            <div>
              <span className="text-slate-500 text-[11px]">Baseline Distance (G0):</span>
              <div className="font-bold text-slate-900 text-sm font-mono">{selectedOrigin.G0_distance_m} m</div>
            </div>
            <div>
              <span className="text-slate-500 text-[11px]">Workzone Distance (G0+C):</span>
              <div className="font-bold text-rose-700 text-sm font-mono">{selectedOrigin.G0_C_distance_m} m</div>
            </div>
            <div>
              <span className="text-slate-500 text-[11px]">Modeled Detour Delta:</span>
              <div className="font-bold text-slate-900 text-sm font-mono">+{selectedOrigin.construction_delta_m} m</div>
            </div>
            <div>
              <span className="text-slate-500 text-[11px]">Relative Detour %:</span>
              <div className="font-bold text-slate-900 text-sm font-mono">{selectedOrigin.detour_percentage}%</div>
            </div>
          </div>

          {/* Attribution & Uncertainty Ledger */}
          <div className="border border-slate-200 rounded p-2.5 bg-white space-y-1.5">
            <div className="font-semibold text-slate-800">Causal Attribution & Uncertainty</div>
            <div className="text-[11px] text-slate-600">
              • <b>Proposal Effect (G0+P - G0):</b> <span className="font-mono">{selectedOrigin.proposal_delta_m} m</span> (Identity invariant)
            </div>
            <div className="text-[11px] text-slate-600">
              • <b>Mitigation Recovery:</b> <span className="font-mono">-{selectedOrigin.mitigation_recovery_m || 0} m</span>
            </div>
            <div className="text-[11px] text-slate-600">
              • <b>Reachability:</b> {selectedOrigin.G0_C_reachable ? "Preserved via surrounding street grid" : "DISCONNECTED"}
            </div>
            <div className="text-[11px] text-slate-500 pt-1 border-t border-slate-100">
              <b>Run ID:</b> <span className="font-mono text-[10px]">{runId || "N/A"}</span> | <b>State:</b> {selectedState}
            </div>
          </div>

          <div className="p-2 bg-amber-50/80 border border-amber-200/80 rounded text-amber-900 text-[11px] leading-relaxed">
            <b>Scientific Note:</b> Distances are deterministic shortest paths on mapped road network topology. They do not constitute measured ambulance response times or live congestion.
          </div>
        </div>
      )}

      {/* Tab 2: Alternatives Workflow */}
      {activeTab === "candidate" && (
        <div className="space-y-3 text-xs overflow-y-auto flex-1">
          {/* Candidate Selector */}
          <div>
            <label className="font-semibold text-slate-700 block mb-1">Select Candidate Mitigation:</label>
            <select
              value={candidate?.candidate_id || ""}
              onChange={(e) => onSelectCandidate(e.target.value)}
              className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white focus:ring-1 focus:ring-teal-500"
            >
              {allCandidates.map(c => (
                <option key={c.candidate_id} value={c.candidate_id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          {candidate && (
            <>
              <div className="border border-slate-200 p-2.5 rounded bg-slate-50 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Recommendation Status:</span>
                  <span className="px-2 py-0.5 rounded font-mono font-bold text-[10px] bg-amber-100 text-amber-900 border border-amber-300">
                    {candidate.feasibility_class}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Statutory Permission:</span>
                  <span className="text-slate-800 font-medium">{candidate.permission_status}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Physical Review:</span>
                  <span className="text-slate-800 font-medium">{candidate.physical_status}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Cost Input:</span>
                  <span className="text-slate-800 font-medium">{candidate.cost_status}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Avg Detour Reduction:</span>
                  <span className="text-teal-700 font-bold font-mono">-{candidate.modeled_metrics.average_detour_reduction_m} m</span>
                </div>
              </div>

              {candidate.conflict_pedestrian && (
                <div className="p-2.5 bg-rose-50 border border-rose-200 rounded text-rose-800 text-[11px] flex items-start space-x-2">
                  <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600" />
                  <div>
                    <b>Pedestrian Conflict Detected:</b> Contraflow vehicle allocation compresses the active footway width along Palarivattom Rd. Not universally safer.
                  </div>
                </div>
              )}

              <div className="p-2.5 bg-slate-100 border border-slate-200 rounded text-slate-700 text-[11px] leading-relaxed">
                <b>Optimizer Finding:</b> {candidate.rejection_reason || "Verified and permissible."}
              </div>

              <div className="p-2 bg-amber-50 border border-amber-200 rounded text-amber-900 text-[11px]">
                <b>Global Decision Status: NO_VERIFIED_OPTION.</b> System strictly refuses to fabricate an approved alternative when statutory police permissions are unverified.
              </div>
            </>
          )}
        </div>
      )}

      {/* Tab 3: Guarded AI Analyst */}
      {activeTab === "ai" && (
        <div className="space-y-3 text-xs flex flex-col h-full overflow-y-auto">
          <div className="text-[11px] text-slate-600 leading-relaxed">
            The Guarded AI Analyst provides read-only explanations strictly grounded in structured run records.
            All numeric claims are validated by server assertion filters prior to display.
          </div>

          <div className="space-y-1.5">
            <label className="text-slate-700 font-medium">Inquire with Geospatial Evidence:</label>
            <input
              type="text"
              value={aiQuestion}
              onChange={(e) => setAiQuestion(e.target.value)}
              className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none"
            />
          </div>

          <button
            onClick={handleAskAI}
            disabled={aiLoading}
            className="w-full py-1.5 px-3 bg-teal-700 hover:bg-teal-800 text-white font-medium rounded text-xs transition-colors flex items-center justify-center space-x-1.5"
          >
            {aiLoading ? <span>Consulting Evidence Store...</span> : <span>Run Guarded Inference</span>}
          </button>

          {aiAnswer && (
            <div className="p-3 bg-slate-50 border border-slate-200 rounded text-slate-800 text-xs leading-relaxed space-y-2 mt-2">
              <div className="font-semibold text-slate-900 flex items-center space-x-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-teal-600" />
                <span>Analyst Explanation</span>
              </div>
              <div>{aiAnswer}</div>
            </div>
          )}

          {aiViolations.length > 0 && (
            <div className="p-2 bg-rose-50 border border-rose-200 rounded text-rose-800 text-[11px] space-y-1">
              <b>Claim Violations Intercepted:</b>
              {aiViolations.map((v, i) => (
                <div key={i}>• {v}</div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
