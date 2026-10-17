import React from "react";
import { StudyMetadata, Facility } from "@/types";
import { X, Database } from "lucide-react";

interface EvidenceModalProps {
  isOpen: boolean;
  onClose: () => void;
  metadata: StudyMetadata | null;
  facility: Facility | null;
  runId: string | null;
}

export const EvidenceModal: React.FC<EvidenceModalProps> = ({
  isOpen,
  onClose,
  metadata,
  facility,
  runId
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white border border-slate-200 rounded-xl max-w-xl w-full shadow-2xl overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
          <div className="flex items-center space-x-2">
            <Database className="w-4 h-4 text-teal-700" />
            <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Material Evidence & Provenance Inspector
            </span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-3.5 text-xs text-slate-700 overflow-y-auto max-h-[80vh]">
          <div className="bg-slate-50 p-3 rounded border border-slate-200 space-y-1">
            <div className="font-semibold text-slate-900">Run Identification & Snapshot</div>
            <div>• <b>Execution Run ID:</b> <span className="font-mono">{runId || "N/A"}</span></div>
            <div>• <b>Study Area:</b> {metadata?.name} ({metadata?.region})</div>
            <div>• <b>Snapshot Date:</b> {metadata?.snapshot_date}</div>
            <div>• <b>Coordinate Systems:</b> {metadata?.crs_source} / Projected: {metadata?.crs_projected}</div>
          </div>

          <div className="border border-slate-200 p-3 rounded space-y-1.5">
            <div className="font-semibold text-slate-900">Road Network Provenance</div>
            <div>• <b>Data Source:</b> OpenStreetMap Contributors (ODbL)</div>
            <div>• <b>Topology Status:</b> Mapped road network (referential integrity audited; 0 missing node refs)</div>
            <div>• <b>Field Verification:</b> UNVERIFIED_FIELD_TOPOLOGY (research boundary, not official surveyed limits)</div>
          </div>

          <div className="border border-slate-200 p-3 rounded space-y-1.5">
            <div className="font-semibold text-slate-900">Destination Facility Status</div>
            <div>• <b>Facility Name:</b> {facility?.name}</div>
            <div>• <b>Operator Address:</b> {facility?.address} (Verified via hospital operator)</div>
            <div>• <b>Entrance Coordinates:</b> PROVISIONAL (ground access surveyed entrance pending official review)</div>
          </div>

          <div className="p-3 bg-amber-50/70 border border-amber-200 rounded text-amber-900 space-y-1">
            <div className="font-semibold">Calculation Method & Non-Emergency Disclaimers</div>
            <div>• Shortest path calculations are deterministic directed graph traversals (Dijkstra algorithm).</div>
            <div>• Detour meters represent modeled graph path differences, NEVER live ambulance response times or congestion forecasts.</div>
          </div>
        </div>

        <div className="px-5 py-3 bg-slate-50 border-t border-slate-100 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-800 hover:bg-slate-900 text-white rounded text-xs font-semibold"
          >
            Close Inspector
          </button>
        </div>
      </div>
    </div>
  );
};
