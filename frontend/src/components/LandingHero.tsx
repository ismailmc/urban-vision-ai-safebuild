import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { ArrowRight, ShieldCheck, Play, Layers, Users, GitCompare } from "lucide-react";
import { AnalysisResponse, AnalyticalState } from "@/types";
import { fetchAnalysis } from "@/lib/api";

const MapCanvas = dynamic(() => import("@/components/MapCanvas").then((m) => m.MapCanvas), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full min-h-[360px] bg-slate-900 flex items-center justify-center text-slate-400 text-sm font-medium">
      Loading Kakkanad Study Map...
    </div>
  )
});

interface LandingHeroProps {
  onExplore: () => void;
  onStartDemo: () => void;
}

export const LandingHero: React.FC<LandingHeroProps> = ({ onExplore, onStartDemo }) => {
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null);
  const [previewState, setPreviewState] = useState<AnalyticalState>("G0_C");
  const [selectedOriginId, setSelectedOriginId] = useState<string>("orig_kakkanad_west");

  useEffect(() => {
    fetchAnalysis("motor_vehicle")
      .then((data) => setAnalysisData(data))
      .catch((err) => console.error("Landing preview fetch error:", err));
  }, []);

  const selectedOrigin = analysisData?.per_origin_results.find(o => o.origin_id === selectedOriginId) || analysisData?.per_origin_results[0];

  return (
    <div className="min-h-screen bg-[#0B132B] text-slate-100 flex flex-col justify-between selection:bg-teal-500 selection:text-white">
      {/* 1. Header (Shared Container Contract, 72px Height, Responsive Wrap) */}
      <header className="border-b border-[#2E3856] bg-[#1C2541]/90 backdrop-blur-md sticky top-0 z-30">
        <div className="max-w-[1280px] mx-auto px-5 sm:px-8 min-h-[72px] py-3 flex flex-wrap items-center justify-between gap-3">
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-teal-600 flex items-center justify-center font-extrabold text-white text-base shadow-md shadow-teal-950/40 shrink-0">
              SB
            </div>
            <div className="flex items-baseline space-x-1.5 sm:space-x-2">
              <span className="font-bold text-base sm:text-lg tracking-tight text-white whitespace-nowrap">Urban Vision AI</span>
              <span className="text-teal-400 font-mono text-[11px] sm:text-xs uppercase tracking-wider">SafeBuild</span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            <button
              onClick={onStartDemo}
              className="text-xs sm:text-sm font-medium h-9 sm:h-10 px-3 sm:px-4 rounded-xl border border-[#2E3856] hover:bg-[#253256] text-slate-200 transition flex items-center space-x-1.5"
            >
              <Play className="w-3.5 h-3.5 fill-slate-200" />
              <span>90s Demo</span>
            </button>
            <button
              onClick={onExplore}
              className="text-xs sm:text-sm font-bold h-9 sm:h-10 px-3.5 sm:px-5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white transition shadow-md shadow-teal-950/40 flex items-center space-x-1.5 whitespace-nowrap"
            >
              <span>Open Studio</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </header>

      {/* 2. Hero Section */}
      <main className="max-w-[1280px] mx-auto px-5 sm:px-8 pt-8 sm:pt-14 pb-16 flex-1 w-full">
        <div className="grid lg:grid-cols-12 gap-8 lg:gap-12 items-start">
          {/* Left Column: Headline and Context */}
          <div className="lg:col-span-5 space-y-5 sm:space-y-6">
            <div className="inline-flex items-center space-x-2 px-3 py-1 sm:px-3.5 sm:py-1.5 bg-[#1C2541] border border-[#2E3856] rounded-full text-xs font-semibold text-teal-300">
              <ShieldCheck className="w-4 h-4 text-teal-400 shrink-0" />
              <span>SFIC 2026 — Track A | Kakkanad Scenario Study</span>
            </div>

            <h1 className="text-3xl sm:text-5xl lg:text-[54px] font-black tracking-tight text-white leading-[1.14]">
              Plan construction.<br />
              <span className="text-teal-400">Protect community access.</span>
            </h1>

            <p className="text-base sm:text-lg text-slate-300 leading-relaxed font-normal">
              See how proposed road restrictions affect nearby communities, compare alternatives, and inspect the evidence behind each result.
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-1">
              <button
                onClick={onExplore}
                className="h-11 sm:h-12 px-5 sm:px-6 bg-teal-600 hover:bg-teal-500 text-white font-bold text-sm sm:text-base rounded-xl shadow-lg shadow-teal-950/50 transition flex items-center space-x-2"
              >
                <span>Open Planning Studio</span>
                <ArrowRight className="w-4 h-4" />
              </button>
              <button
                onClick={onStartDemo}
                className="h-11 sm:h-12 px-4 sm:px-5 bg-[#1C2541] border border-[#2E3856] hover:bg-[#253256] text-slate-200 font-semibold text-sm sm:text-base rounded-xl transition flex items-center space-x-2"
              >
                <span>Launch Walkthrough</span>
              </button>
            </div>

            <div className="pt-3 border-t border-[#2E3856]/60 text-xs text-slate-400 space-y-1">
              <div>• <b>Study Corridor:</b> Kakkanad, Kochi (Palarivattom-Kakkanad Rd Case Study)</div>
              <div>• <b>Network Scope:</b> 19,582 nodes, 11,675 directed edges (OpenStreetMap ODbL)</div>
            </div>
          </div>

          {/* Right Column: Genuine Geographic Product Preview */}
          <div className="lg:col-span-7">
            <div className="bg-[#1C2541] border border-[#2E3856] rounded-2xl p-4 sm:p-5 shadow-2xl relative overflow-hidden space-y-3.5">
              {/* Preview Header & Scenario Selector */}
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#2E3856] pb-3">
                <div className="flex items-center space-x-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-teal-400 animate-pulse" />
                  <span className="text-xs font-bold text-white uppercase tracking-wider">
                    Live Geographic Preview
                  </span>
                  <span className="text-[11px] font-mono text-slate-400 hidden sm:inline">
                    ({analysisData?.metadata.name || "Kakkanad Research Study Area"})
                  </span>
                </div>

                {/* Scenario Toggle */}
                <div className="flex bg-[#0B132B] p-0.5 rounded-lg border border-[#2E3856] text-xs">
                  <button
                    onClick={() => setPreviewState("G0")}
                    className={`px-2 py-1 sm:px-2.5 rounded-md text-[11px] sm:text-xs font-semibold transition ${
                      previewState === "G0" ? "bg-teal-600 text-white" : "text-slate-400 hover:text-white"
                    }`}
                  >
                    Baseline (G0)
                  </button>
                  <button
                    onClick={() => setPreviewState("G0_C")}
                    className={`px-2 py-1 sm:px-2.5 rounded-md text-[11px] sm:text-xs font-semibold transition ${
                      previewState === "G0_C" ? "bg-rose-600 text-white" : "text-slate-400 hover:text-white"
                    }`}
                  >
                    Workzone (G0+C)
                  </button>
                  <button
                    onClick={() => setPreviewState("G0_P_C_M")}
                    className={`px-2 py-1 sm:px-2.5 rounded-md text-[11px] sm:text-xs font-semibold transition ${
                      previewState === "G0_P_C_M" ? "bg-teal-700 text-white" : "text-slate-400 hover:text-white"
                    }`}
                  >
                    Mitigated (M)
                  </button>
                </div>
              </div>

              {/* Map Canvas Container */}
              <div className="h-[360px] sm:h-[460px] rounded-xl overflow-hidden border border-[#2E3856] relative">
                {analysisData ? (
                  <MapCanvas
                    origins={analysisData.per_origin_results}
                    selectedOriginId={selectedOriginId}
                    onSelectOrigin={(id) => setSelectedOriginId(id)}
                    selectedState={previewState}
                    facility={analysisData.primary_facility}
                    disruptedSegments={analysisData.disrupted_segments}
                  />
                ) : (
                  <div className="w-full h-full bg-[#0B132B] flex items-center justify-center text-slate-400 text-sm">
                    Connecting to Kakkanad Analytical Engine...
                  </div>
                )}
              </div>

              {/* Real Run Annotation Footer */}
              <div className="bg-[#0B132B] rounded-xl p-3 border border-[#2E3856] flex flex-wrap items-center justify-between gap-2 text-xs">
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-slate-300">Active Result:</span>
                  <span className="text-white font-bold">{selectedOrigin?.origin_name || "Kakkanad West Anchor"}</span>
                  <span className="font-mono text-rose-400 font-bold">
                    +{selectedOrigin?.construction_delta_m || 354.9} m ({selectedOrigin?.detour_percentage || 22.6}%)
                  </span>
                </div>
                <div className="flex items-center space-x-2 font-mono text-[11px] text-slate-400">
                  <span className="px-1.5 py-0.5 rounded bg-amber-950/80 text-amber-300 border border-amber-800/80">
                    HYPOTHETICAL_SCENARIO
                  </span>
                  <span>Run: {analysisData?.run_id || "run_live"}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 3. Workflow Section */}
        <section className="mt-14 sm:mt-20 pt-10 sm:pt-12 border-t border-[#2E3856]">
          <div className="mb-6">
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              A structured review workflow for infrastructure decisions
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              Replace subjective assumptions with reproducible shortest-path attribution and verified feasibility checks.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-[#1C2541]/70 hover:bg-[#1C2541] transition p-6 rounded-2xl border border-[#2E3856] space-y-3">
              <div className="w-9 h-9 rounded-xl bg-teal-600/20 text-teal-400 flex items-center justify-center font-bold text-base">
                1
              </div>
              <div className="text-base font-bold text-white flex items-center space-x-2">
                <Layers className="w-4 h-4 text-teal-400" />
                <span>Define a change</span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">
                Specify workzone locations, directional restrictions, and travel modes on real mapped road edges.
              </p>
            </div>

            <div className="bg-[#1C2541]/70 hover:bg-[#1C2541] transition p-6 rounded-2xl border border-[#2E3856] space-y-3">
              <div className="w-9 h-9 rounded-xl bg-teal-600/20 text-teal-400 flex items-center justify-center font-bold text-base">
                2
              </div>
              <div className="text-base font-bold text-white flex items-center space-x-2">
                <Users className="w-4 h-4 text-teal-400" />
                <span>See who is affected</span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">
                Trace route distances from community settlement anchors to essential facilities, isolating net detours.
              </p>
            </div>

            <div className="bg-[#1C2541]/70 hover:bg-[#1C2541] transition p-6 rounded-2xl border border-[#2E3856] space-y-3">
              <div className="w-9 h-9 rounded-xl bg-teal-600/20 text-teal-400 flex items-center justify-center font-bold text-base">
                3
              </div>
              <div className="text-base font-bold text-white flex items-center space-x-2">
                <GitCompare className="w-4 h-4 text-teal-400" />
                <span>Compare alternatives</span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">
                Evaluate candidate interventions against physical review, authority permissions, and pedestrian mode conflicts.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* 4. Footer */}
      <footer className="border-t border-[#2E3856] bg-[#070D1E] py-8">
        <div className="max-w-[1280px] mx-auto px-5 sm:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-3">
          <div>OpenStreetMap Contributors (ODbL) | Palarivattom–Kakkanad Road Corridor Research Case Study</div>
          <div>Research prototype for academic evaluation. Not an approved operational deployment.</div>
        </div>
      </footer>
    </div>
  );
};
