import React, { useState } from "react";
import { AnalyticalState } from "@/types";
import { StudioTab } from "@/components/NavigationRail";
import { X, ArrowRight, ArrowLeft, Pause, Play, Compass, Layers, Users, Sliders, FileText } from "lucide-react";
import confetti from "canvas-confetti";

interface GuidedDemoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectTab: (tab: StudioTab) => void;
  onSelectState: (state: AnalyticalState) => void;
  onSelectOrigin: (id: string) => void;
  onTriggerFocusArea: () => void;
}

export const GuidedDemoModal: React.FC<GuidedDemoModalProps> = ({
  isOpen,
  onClose,
  onSelectTab,
  onSelectState,
  onSelectOrigin,
  onTriggerFocusArea
}) => {
  const [step, setStep] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  if (!isOpen) return null;

  const STEPS = [
    {
      stepNum: 1,
      tab: "explore" as StudioTab,
      title: "Step 1: Explore Real Area & 2D/3D Context",
      body: "We start with authentic Kakkanad OpenStreetMap geometry (19,582 nodes and 11,675 directed edges). You can switch between 2D and 3D with authentic building footprint extrusions and verify the corridor bounds around Palarivattom–Kakkanad Road.",
      highlightControl: "Map Canvas Toolbar: 2D/3D Toggle & Focus Area",
      icon: <Compass className="w-5 h-5 text-teal-600" />,
      action: () => {
        onSelectTab("explore");
        onSelectState("G0");
        onSelectOrigin("orig_kakkanad_west");
        onTriggerFocusArea();
      }
    },
    {
      stepNum: 2,
      tab: "define" as StudioTab,
      title: "Step 2: Define Change on Mapped Road Segments",
      body: "Planners can select any street directly on the map or choose preconfigured construction workzones along Palarivattom–Kakkanad Road. Each restriction preserves source OSM way IDs and records directional and phase properties.",
      highlightControl: "Studio Action Panel: Road Connection & Restriction Editor",
      icon: <Layers className="w-5 h-5 text-amber-600" />,
      action: () => {
        onSelectTab("define");
        onSelectState("G0_C");
        onSelectOrigin("orig_kakkanad_west");
      }
    },
    {
      stepNum: 3,
      tab: "impact" as StudioTab,
      title: "Step 3: Analyze Community Access & Detours",
      body: "Running the analytical engine calculates true shortest paths for all 6 community origins. Residents of Kakkanad West face a +354.9 m (+22.6%) modeled detour to reach Sunrise Hospital under workzone closures.",
      highlightControl: "Community Access Panel: 'Analyze Community Access' & Origin Selector",
      icon: <Users className="w-5 h-5 text-rose-600" />,
      action: () => {
        onSelectTab("impact");
        onSelectState("G0_C");
        onSelectOrigin("orig_kakkanad_west");
      }
    },
    {
      stepNum: 4,
      tab: "alternatives" as StudioTab,
      title: "Step 4: Compare Candidate Alternatives Safely",
      body: "We review candidate arrangements like contraflow (M1). While contraflow mathematically recovers detour distance, it compresses pedestrian sidewalk width and lacks statutory police permits. The optimizer safely returns 'NO_VERIFIED_OPTION'.",
      highlightControl: "Alternatives Ledger: Candidate Cards & Mode Conflict Warnings",
      icon: <Sliders className="w-5 h-5 text-indigo-600" />,
      action: () => {
        onSelectTab("alternatives");
        onSelectState("G0_P_C_M");
      }
    },
    {
      stepNum: 5,
      tab: "summary" as StudioTab,
      title: "Step 5: Decision Summary & Guarded Intelligence",
      body: "Review the comprehensive trade-off brief, query the guarded AI analyst with context-aware prompts, and export defensible PDF and CSV reports for municipal stakeholders without fabricated claims.",
      highlightControl: "Decision Brief: Tradeoffs, Guarded AI, and PDF/CSV Export",
      icon: <FileText className="w-5 h-5 text-teal-700" />,
      action: () => {
        onSelectTab("summary");
        confetti({ particleCount: 70, spread: 60, origin: { y: 0.6 } });
      }
    }
  ];

  const current = STEPS[step];

  const handleNext = () => {
    if (step < STEPS.length - 1) {
      const nextStep = step + 1;
      setStep(nextStep);
      STEPS[nextStep].action();
    } else {
      onClose();
    }
  };

  const handleBack = () => {
    if (step > 0) {
      const prevStep = step - 1;
      setStep(prevStep);
      STEPS[prevStep].action();
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white border border-slate-200 rounded-2xl max-w-lg w-full shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-teal-600 animate-pulse" />
            <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              SafeBuild Guided Walkthrough ({step + 1} of {STEPS.length})
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsPaused(!isPaused)}
              className="text-slate-500 hover:text-slate-800 p-1 rounded hover:bg-slate-200 transition"
              title={isPaused ? "Resume Walkthrough" : "Pause Walkthrough"}
            >
              {isPaused ? <Play className="w-3.5 h-3.5 text-teal-700" /> : <Pause className="w-3.5 h-3.5" />}
            </button>
            <button onClick={onClose} className="text-slate-400 hover:text-slate-700">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-4">
          <div className="flex items-start space-x-3">
            <div className="p-2.5 bg-slate-100 rounded-xl shrink-0">
              {current.icon}
            </div>
            <div>
              <div className="text-base font-extrabold text-slate-900">{current.title}</div>
              <div className="text-xs text-slate-600 leading-relaxed mt-1">{current.body}</div>
            </div>
          </div>

          {/* Highlight Target Control */}
          <div className="p-3 bg-teal-50/70 border border-teal-200 rounded-xl text-xs space-y-0.5">
            <div className="text-[10px] font-bold uppercase tracking-wider text-teal-800">Highlighted Interface Control:</div>
            <div className="font-semibold text-slate-900">{current.highlightControl}</div>
          </div>

          {/* Step Progress Indicators */}
          <div className="flex items-center space-x-1.5 pt-2">
            {STEPS.map((_, i) => (
              <span
                key={i}
                className={`h-1.5 rounded-full transition-all ${
                  i === step ? "w-8 bg-teal-600" : "w-2.5 bg-slate-200"
                }`}
              />
            ))}
          </div>
        </div>

        {/* Footer Actions */}
        <div className="px-6 py-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
          <button
            onClick={onClose}
            className="text-xs font-medium text-slate-500 hover:text-slate-800"
          >
            Exit Walkthrough
          </button>

          <div className="flex items-center space-x-2">
            {step > 0 && (
              <button
                onClick={handleBack}
                className="px-3 py-1.5 border border-slate-300 hover:bg-slate-100 text-slate-700 rounded-lg text-xs font-semibold flex items-center space-x-1 transition"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Back</span>
              </button>
            )}

            <button
              onClick={handleNext}
              className="px-4 py-2 bg-teal-700 hover:bg-teal-800 text-white rounded-lg text-xs font-semibold flex items-center space-x-1.5 shadow-sm transition"
            >
              <span>{step === STEPS.length - 1 ? "Finish Walkthrough" : "Next Step"}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

