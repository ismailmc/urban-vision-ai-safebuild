import React from "react";
import { Download, Box, Database, Sparkles, BookOpen } from "lucide-react";

interface StudioTopBarProps {
  onReturnToLanding?: () => void;
  selectedTravelMode: string;
  onSelectTravelMode: (mode: string) => void;
  is3DMode: boolean;
  onToggle3DMode: () => void;
  onOpenEvidenceModal: () => void;
  onOpenAIModal: () => void;
  onLoadKakkanadExample: () => void;
}

export const StudioTopBar: React.FC<StudioTopBarProps> = ({
  selectedTravelMode,
  onSelectTravelMode,
  is3DMode,
  onToggle3DMode,
  onOpenEvidenceModal,
  onOpenAIModal,
  onLoadKakkanadExample
}) => {
  return (
    <header className="bg-white border-b border-slate-200 px-4 sm:px-6 h-16 flex items-center justify-between shrink-0 z-20 shadow-sm text-slate-800">
      {/* Left: Brand & Study Identification */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-teal-700 flex items-center justify-center font-black text-white text-xs shadow-sm">
            SB
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-xs sm:text-sm tracking-tight text-slate-900">
                SafeBuild
              </span>
              <span className="text-slate-300 font-mono text-xs">/</span>
              <span className="text-xs font-semibold text-slate-700 hidden sm:inline">
                Construction Access Review
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-50 border border-emerald-200 text-emerald-800 font-bold">
                Kakkanad Scenario Study
              </span>
            </div>
            <div className="text-[10px] text-slate-500 hidden md:block">
              Palarivattom–Kakkanad Corridor • Sunrise Hospital Access
            </div>
          </div>
        </div>
      </div>

      {/* Center: First-Open Example Prompt */}
      <div className="hidden lg:flex items-center space-x-2">
        <button
          type="button"
          onClick={onLoadKakkanadExample}
          className="text-xs font-semibold text-teal-800 bg-teal-50 hover:bg-teal-100 border border-teal-200 px-3 py-1.5 rounded-lg flex items-center space-x-1.5 transition cursor-pointer"
        >
          <BookOpen className="w-3.5 h-3.5 text-teal-700" />
          <span>Try the Kakkanad example</span>
        </button>
      </div>

      {/* Right: Mode, 3D, Secondary Actions (Evidence, AI, Report) */}
      <div className="flex items-center space-x-2 sm:space-x-2.5">
        {/* Travel Mode Toggle */}
        <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs">
          <button
            type="button"
            onClick={() => onSelectTravelMode("motor_vehicle")}
            className={`px-2.5 py-1 rounded-md text-xs font-semibold transition cursor-pointer ${
              selectedTravelMode === "motor_vehicle"
                ? "bg-white text-slate-900 shadow-sm"
                : "text-slate-500 hover:text-slate-800"
            }`}
          >
            Motor
          </button>
          <button
            type="button"
            onClick={() => onSelectTravelMode("pedestrian")}
            className={`px-2.5 py-1 rounded-md text-xs font-semibold transition cursor-pointer ${
              selectedTravelMode === "pedestrian"
                ? "bg-white text-slate-900 shadow-sm"
                : "text-slate-500 hover:text-slate-800"
            }`}
          >
            Pedestrian
          </button>
        </div>

        {/* 2D / 3D Toggle */}
        <button
          type="button"
          onClick={onToggle3DMode}
          className={`px-2.5 py-1.5 text-xs font-semibold rounded-lg border flex items-center space-x-1.5 transition cursor-pointer ${
            is3DMode
              ? "bg-slate-900 text-white border-slate-950 shadow-sm"
              : "bg-white text-slate-700 hover:bg-slate-50 border-slate-200"
          }`}
          title="Toggle 2D / 3D map perspective"
        >
          <Box className="w-3.5 h-3.5" />
          <span>{is3DMode ? "3D Active" : "2D View"}</span>
        </button>

        {/* Secondary: View Evidence & Advanced Formulas */}
        <button
          type="button"
          onClick={onOpenEvidenceModal}
          className="px-2.5 py-1.5 text-xs font-semibold bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg flex items-center space-x-1 transition cursor-pointer"
          title="View 5-state algebra, provenance and raw graph metadata"
        >
          <Database className="w-3.5 h-3.5 text-slate-500" />
          <span className="hidden sm:inline">Evidence & Advanced</span>
        </button>

        {/* Secondary: Explain with AI */}
        <button
          type="button"
          onClick={onOpenAIModal}
          className="px-2.5 py-1.5 text-xs font-semibold bg-teal-50/70 border border-teal-200 hover:bg-teal-100 text-teal-800 rounded-lg flex items-center space-x-1 transition cursor-pointer"
          title="Ask Dijkstra-grounded analyst questions"
        >
          <Sparkles className="w-3.5 h-3.5 text-teal-600" />
          <span className="hidden sm:inline">Explain with AI</span>
        </button>

        {/* Secondary: Download Report */}
        <a
          href={`http://localhost:8000/api/report/pdf?mode=${selectedTravelMode}`}
          download
          className="px-3 py-1.5 text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-white rounded-lg flex items-center space-x-1.5 shadow-sm transition"
          title="Download audited PDF decision brief"
        >
          <Download className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Download Report</span>
        </a>
      </div>
    </header>
  );
};
