import React from "react";
import { OriginResult, CandidateEvaluation, Facility } from "@/types";
import { SelectedRoadInfo } from "@/components/MapCanvas";
import { X, ShieldAlert } from "lucide-react";

export type DrawerContent =
  | { type: "origin"; data: OriginResult }
  | { type: "road"; data: SelectedRoadInfo }
  | { type: "candidate"; data: CandidateEvaluation }
  | { type: "facility"; data: Facility }
  | null;

interface ContextDrawerProps {
  content: DrawerContent;
  onClose: () => void;
  onAddRoadRestriction?: (road: SelectedRoadInfo) => void;
  isRoadRestricted?: boolean;
}

export const ContextDrawer: React.FC<ContextDrawerProps> = ({
  content,
  onClose,
  onAddRoadRestriction,
  isRoadRestricted = false
}) => {
  if (!content) return null;

  return (
    <div className="absolute top-4 right-4 z-30 w-80 max-w-[calc(100vw-32px)] bg-white/95 backdrop-blur-md border border-slate-200 rounded-2xl shadow-xl p-4 text-xs space-y-3 animate-in fade-in slide-in-from-right-4 duration-200">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-2">
        <span className="text-[10px] font-bold uppercase tracking-wider text-teal-800">
          Context Details
        </span>
        <button
          type="button"
          onClick={onClose}
          className="text-slate-400 hover:text-slate-700 font-bold p-1 rounded-md cursor-pointer"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Origin Details */}
      {content.type === "origin" && (
        <div className="space-y-2">
          <div className="text-[10px] text-slate-400 uppercase font-semibold">Community Origin Anchor</div>
          <h3 className="font-bold text-sm text-slate-900">{content.data.origin_name}</h3>
          <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-xl space-y-1 font-mono text-[11px]">
            <div className="flex justify-between">
              <span className="text-slate-500 font-sans">Baseline Route:</span>
              <span className="font-bold text-slate-800">{content.data.G0_distance_m} m</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500 font-sans">Under Restriction:</span>
              <span className="font-bold text-rose-600">{content.data.G0_C_distance_m} m</span>
            </div>
            <div className="flex justify-between border-t border-slate-200 pt-1 mt-1">
              <span className="text-slate-500 font-sans">Net Detour Delta:</span>
              <span className="font-bold text-rose-600">+{content.data.construction_delta_m} m ({content.data.detour_percentage}%)</span>
            </div>
          </div>
          <div className="text-[11px] text-slate-500 leading-relaxed">
            Sampling Method: <span className="font-mono">{content.data.sampling_method}</span>
          </div>
        </div>
      )}

      {/* Road Details */}
      {content.type === "road" && (
        <div className="space-y-2">
          <div className="text-[10px] text-slate-400 uppercase font-semibold">Selected Road Edge</div>
          <h3 className="font-bold text-sm text-slate-900">{content.data.name}</h3>
          <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-xl space-y-1 font-mono text-[11px]">
            <div>Way ID: <b>{content.data.way_id}</b></div>
            <div>Highway Class: <b>{content.data.highway}</b></div>
            <div>Oneway: <b>{content.data.oneway}</b></div>
          </div>
          {onAddRoadRestriction && (
            <button
              type="button"
              onClick={() => onAddRoadRestriction(content.data)}
              className={`w-full py-2 rounded-xl font-bold text-xs shadow-sm transition flex items-center justify-center space-x-1 cursor-pointer ${
                isRoadRestricted
                  ? "bg-slate-200 text-slate-500 cursor-not-allowed"
                  : "bg-amber-600 hover:bg-amber-700 text-white"
              }`}
            >
              <span>{isRoadRestricted ? "Segment Already Restricted" : "+ Add Workzone Restriction"}</span>
            </button>
          )}
        </div>
      )}

      {/* Candidate Details */}
      {content.type === "candidate" && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 uppercase font-semibold">Alternative Intervention</span>
            <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded font-bold ${
              content.data.feasibility_class === "VERIFIED_IMPLEMENTABLE"
                ? "bg-teal-100 text-teal-800"
                : "bg-amber-100 text-amber-800"
            }`}>
              {content.data.feasibility_class}
            </span>
          </div>
          <h3 className="font-bold text-sm text-slate-900">{content.data.name}</h3>
          <p className="text-[11px] text-slate-600 leading-relaxed">
            {content.data.description}
          </p>

          <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-xl space-y-1 text-[11px]">
            <div className="flex justify-between">
              <span className="text-slate-500">Average Detour Recovery:</span>
              <span className="font-mono font-bold text-teal-700">
                {content.data.modeled_metrics.average_detour_reduction_m > 0
                  ? `-${content.data.modeled_metrics.average_detour_reduction_m} m`
                  : "0 m"}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Pedestrian Conflict:</span>
              <span className={content.data.conflict_pedestrian ? "text-rose-600 font-bold" : "text-slate-700"}>
                {content.data.conflict_pedestrian ? "YES (Sidewalk Compressed)" : "None"}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Statutory Permission:</span>
              <span className="font-mono text-[10px] text-amber-800 font-semibold">{content.data.permission_status}</span>
            </div>
          </div>

          {content.data.rejection_reason && (
            <div className="p-2 bg-amber-50 border border-amber-200 rounded-lg text-[11px] text-amber-900 flex items-start space-x-1.5">
              <ShieldAlert className="w-3.5 h-3.5 text-amber-700 shrink-0 mt-0.5" />
              <span>{content.data.rejection_reason}</span>
            </div>
          )}
        </div>
      )}

      {/* Facility Details */}
      {content.type === "facility" && (
        <div className="space-y-2">
          <div className="text-[10px] text-slate-400 uppercase font-semibold">Primary Target Facility</div>
          <h3 className="font-bold text-sm text-slate-900">{content.data.name}</h3>
          <p className="text-[11px] text-slate-600 font-mono">{content.data.address}</p>
          <div className="p-2 bg-teal-50 border border-teal-200 rounded-lg text-[11px] text-teal-900">
            Designated Entrance: <b>{content.data.notes}</b>
          </div>
        </div>
      )}
    </div>
  );
};
