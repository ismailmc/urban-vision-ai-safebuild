import React, { useState, useEffect } from "react";
import { RoadWayItem } from "@/types";
import { fetchRoadsCatalog, updateDisruption, resetDisruption } from "@/lib/api";
import { X, RefreshCw, Check } from "lucide-react";

interface ScenarioEditorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onScenarioSaved: () => void;
}

export const ScenarioEditorModal: React.FC<ScenarioEditorModalProps> = ({
  isOpen,
  onClose,
  onScenarioSaved
}) => {
  const [roads, setRoads] = useState<RoadWayItem[]>([]);
  const [selectedWayIds, setSelectedWayIds] = useState<string[]>([
    "197827530", "383253303", "1011679137", "1011679138"
  ]);
  const [restrictionName, setRestrictionName] = useState("Palarivattom-Kakkanad Rd Metro Pier Erection Zone");
  const [direction, setDirection] = useState("both");
  const [mode, setMode] = useState("motor_vehicle");
  const [phase, setPhase] = useState("Pier Foundation Phase (Hypothetical)");
  const [loading, setLoading] = useState(false);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [searchFilter, setSearchFilter] = useState("");

  useEffect(() => {
    if (isOpen) {
      loadRoads();
    }
  }, [isOpen]);

  const loadRoads = async () => {
    try {
      const data = await fetchRoadsCatalog();
      setRoads(data);
    } catch (err) {
      console.error("Failed to load roads catalog", err);
    }
  };

  const handleToggleWay = (wayId: string) => {
    setHasUnsavedChanges(true);
    if (selectedWayIds.includes(wayId)) {
      setSelectedWayIds(selectedWayIds.filter(id => id !== wayId));
    } else {
      setSelectedWayIds([...selectedWayIds, wayId]);
    }
  };

  const handleSave = async () => {
    if (selectedWayIds.length === 0) {
      alert("Please select at least one road way segment to restrict.");
      return;
    }
    setLoading(true);
    try {
      await updateDisruption({
        target_way_ids: selectedWayIds,
        name: restrictionName,
        direction,
        mode,
        phase
      });
      setHasUnsavedChanges(false);
      onScenarioSaved();
      onClose();
    } catch (err) {
      alert("Failed to save hypothetical scenario: " + String(err));
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    setLoading(true);
    try {
      await resetDisruption();
      setSelectedWayIds(["197827530", "383253303", "1011679137", "1011679138"]);
      setRestrictionName("Palarivattom-Kakkanad Rd Metro Pier Erection Zone");
      setDirection("both");
      setHasUnsavedChanges(false);
      onScenarioSaved();
    } catch (err) {
      alert("Failed to reset: " + String(err));
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const filteredRoads = roads.filter(r => 
    r.name.toLowerCase().includes(searchFilter.toLowerCase()) || 
    r.osm_way_id.includes(searchFilter) ||
    r.highway.toLowerCase().includes(searchFilter.toLowerCase())
  );

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white border border-slate-200 rounded-xl max-w-2xl w-full shadow-2xl flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
          <div>
            <div className="text-sm font-bold text-slate-900 flex items-center space-x-2">
              <span>Interactive Scenario & Restriction Editor</span>
              {hasUnsavedChanges && (
                <span className="text-[10px] bg-amber-100 text-amber-800 font-semibold px-2 py-0.5 rounded border border-amber-300">
                  Unsaved Changes
                </span>
              )}
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Select mapped road edges to define custom civil workzone restrictions and trigger live recalculation.
            </p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Form Body */}
        <div className="p-5 space-y-4 overflow-y-auto flex-1 text-xs">
          {/* Metadata Inputs */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-semibold text-slate-700">Restriction Label</label>
              <input
                type="text"
                value={restrictionName}
                onChange={(e) => { setRestrictionName(e.target.value); setHasUnsavedChanges(true); }}
                className="w-full mt-1 px-2.5 py-1.5 border border-slate-300 rounded text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="font-semibold text-slate-700">Construction Phase</label>
              <input
                type="text"
                value={phase}
                onChange={(e) => { setPhase(e.target.value); setHasUnsavedChanges(true); }}
                className="w-full mt-1 px-2.5 py-1.5 border border-slate-300 rounded text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-semibold text-slate-700">Directionality Restriction</label>
              <select
                value={direction}
                onChange={(e) => { setDirection(e.target.value); setHasUnsavedChanges(true); }}
                className="w-full mt-1 px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white focus:ring-1 focus:ring-teal-500"
              >
                <option value="both">Both Directions (Full Closure)</option>
                <option value="fwd_only">Forward Direction Only</option>
                <option value="rev_only">Reverse Direction Only</option>
              </select>
            </div>
            <div>
              <label className="font-semibold text-slate-700">Travel Mode Affected</label>
              <select
                value={mode}
                onChange={(e) => { setMode(e.target.value); setHasUnsavedChanges(true); }}
                className="w-full mt-1 px-2.5 py-1.5 border border-slate-300 rounded text-xs bg-white focus:ring-1 focus:ring-teal-500"
              >
                <option value="motor_vehicle">Motor Vehicle</option>
                <option value="pedestrian">Pedestrian</option>
              </select>
            </div>
          </div>

          {/* Road Selection Table */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="font-semibold text-slate-700">
                Target Road Way Segments ({selectedWayIds.length} selected)
              </label>
              <input
                type="text"
                placeholder="Search road name or way ID..."
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
                className="px-2 py-1 border border-slate-300 rounded text-[11px] w-48"
              />
            </div>

            <div className="border border-slate-200 rounded max-h-48 overflow-y-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-slate-50 sticky top-0 border-b border-slate-200 text-slate-500">
                  <tr>
                    <th className="py-1 px-2 w-8"></th>
                    <th className="py-1 px-2">Road Name</th>
                    <th className="py-1 px-2">OSM Way ID</th>
                    <th className="py-1 px-2">Class</th>
                    <th className="py-1 px-2">Length</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredRoads.slice(0, 50).map((r) => {
                    const isSelected = selectedWayIds.includes(r.osm_way_id);
                    return (
                      <tr
                        key={r.osm_way_id}
                        onClick={() => handleToggleWay(r.osm_way_id)}
                        className={`border-b border-slate-100 cursor-pointer ${
                          isSelected ? "bg-amber-50 font-medium text-amber-900" : "hover:bg-slate-50"
                        }`}
                      >
                        <td className="py-1 px-2 text-center">
                          <input
                            type="checkbox"
                            checked={isSelected}
                            onChange={() => {}}
                            className="rounded text-teal-600"
                          />
                        </td>
                        <td className="py-1 px-2">{r.name}</td>
                        <td className="py-1 px-2 font-mono text-[11px] text-slate-500">{r.osm_way_id}</td>
                        <td className="py-1 px-2 text-slate-500">{r.highway}</td>
                        <td className="py-1 px-2 font-mono">{r.length_m}m</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="px-5 py-3.5 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
          <button
            onClick={handleReset}
            disabled={loading}
            className="px-3 py-1.5 border border-slate-300 hover:bg-slate-100 rounded text-xs font-medium text-slate-600 flex items-center space-x-1"
          >
            <RefreshCw className="w-3 h-3" />
            <span>Reset to Baseline Corridor</span>
          </button>

          <div className="flex space-x-2">
            <button
              onClick={onClose}
              className="px-3 py-1.5 border border-slate-300 hover:bg-slate-100 rounded text-xs font-medium text-slate-700"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={loading}
              className="px-4 py-1.5 bg-teal-700 hover:bg-teal-800 text-white rounded text-xs font-semibold shadow-sm flex items-center space-x-1"
            >
              <Check className="w-3.5 h-3.5" />
              <span>{loading ? "Recalculating Graph..." : "Save & Recalculate Scenario"}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
