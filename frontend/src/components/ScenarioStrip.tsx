import React from "react";
import { AnalyticalState } from "@/types";

interface ScenarioStripProps {
  selectedState: AnalyticalState;
  onSelectState: (state: AnalyticalState) => void;
}

const STATES: { id: AnalyticalState; plainLabel: string; technicalTag: string; desc: string }[] = [
  { id: "G0", plainLabel: "Existing Conditions", technicalTag: "G0", desc: "Baseline mapped street network before intervention." },
  { id: "G0_C", plainLabel: "Construction Restrictions", technicalTag: "G0+C", desc: "Active civil workzone closure along Palarivattom corridor." },
  { id: "G0_P", plainLabel: "Proposed Changes", technicalTag: "G0+P", desc: "Permanent network changes (identity baseline: P = I)." },
  { id: "G0_P_C", plainLabel: "Proposal Under Disruption", technicalTag: "G0+P+C", desc: "Combined impact of project phasing and workzone." },
  { id: "G0_P_C_M", plainLabel: "With Mitigation", technicalTag: "G0+P+C+M", desc: "Feasibility-tested alternative intervention applied." }
];

export const ScenarioStrip: React.FC<ScenarioStripProps> = ({ selectedState, onSelectState }) => {
  return (
    <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-sm">
      <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2.5 px-0.5 flex items-center justify-between">
        <span>Scenario Review Pipeline</span>
        <span className="text-slate-400 font-normal">Select state to project accessibility changes</span>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-2.5">
        {STATES.map((s) => {
          const isActive = selectedState === s.id;
          return (
            <button
              key={s.id}
              onClick={() => onSelectState(s.id)}
              className={`text-left p-3 rounded-lg border transition-all text-xs focus:outline-none focus:ring-2 focus:ring-teal-600 ${
                isActive
                  ? "border-teal-600 bg-teal-50/70 ring-1 ring-teal-600 shadow-sm"
                  : "border-slate-200 bg-slate-50/60 hover:bg-slate-100/80"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className={`font-bold ${isActive ? "text-teal-900" : "text-slate-800"}`}>
                  {s.plainLabel}
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white border border-slate-200 text-slate-500">
                  {s.technicalTag}
                </span>
              </div>
              <p className="text-[12px] text-slate-500 mt-1 line-clamp-2 leading-relaxed">
                {s.desc}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
