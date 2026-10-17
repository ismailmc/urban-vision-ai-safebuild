import React, { useState, useEffect } from "react";
import Head from "next/head";
import dynamic from "next/dynamic";
import { StudioTopBar } from "@/components/StudioTopBar";
import { TaskPanel, WorkspaceStep } from "@/components/TaskPanel";
import { ContextDrawer, DrawerContent } from "@/components/ContextDrawer";
import { EvidenceModal } from "@/components/EvidenceModal";
import { AIAnalystModal } from "@/components/AIAnalystModal";
import { fetchAnalysis, fetchOptimizer, fetchRoadsCatalog, updateDisruption } from "@/lib/api";
import { AnalysisResponse, OptimizerResponse, AnalyticalState, RoadWayItem } from "@/types";
import { SelectedRoadInfo } from "@/components/MapCanvas";

const MapCanvas = dynamic(() => import("@/components/MapCanvas").then((m) => m.MapCanvas), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full min-h-[440px] bg-slate-100 flex items-center justify-center text-slate-400 text-sm font-medium">
      Loading Kakkanad Geospatial Canvas...
    </div>
  )
});

export default function Home() {
  const [currentStep, setCurrentStep] = useState<WorkspaceStep>("choose_road");
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null);
  const [optimizerData, setOptimizerData] = useState<OptimizerResponse | null>(null);
  const [roadsCatalog, setRoadsCatalog] = useState<RoadWayItem[]>([]);
  const [selectedState, setSelectedState] = useState<AnalyticalState>("G0_C");
  const [selectedOriginId, setSelectedOriginId] = useState<string | null>("orig_kakkanad_west");
  const [selectedTravelMode, setSelectedTravelMode] = useState<string>("motor_vehicle");
  const [selectedCandidateId, setSelectedCandidateId] = useState<string>("cand_m1_phased_contraflow");
  const [selectedRoad, setSelectedRoad] = useState<SelectedRoadInfo | null>({
    way_id: "197827530",
    name: "Palarivattom - Kakkanad Road",
    highway: "secondary",
    oneway: "no"
  });
  const [focusAreaTrigger, setFocusAreaTrigger] = useState<number>(0);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [isComparing, setIsComparing] = useState<boolean>(false);
  const [is3DMode, setIs3DMode] = useState<boolean>(false);

  // Context Drawer State
  const [drawerContent, setDrawerContent] = useState<DrawerContent>(null);

  // Modals for Secondary Actions (Outside Main Task)
  const [isEvidenceOpen, setIsEvidenceOpen] = useState(false);
  const [isAIOpen, setIsAIOpen] = useState(false);

  useEffect(() => {
    loadData(selectedTravelMode, selectedCandidateId);
    fetchRoadsCatalog().then((data) => setRoadsCatalog(data)).catch(() => null);
  }, [selectedTravelMode, selectedCandidateId]);

  const loadData = async (mode: string, candidateId: string) => {
    try {
      const [ana, opt] = await Promise.all([
        fetchAnalysis(mode, candidateId),
        fetchOptimizer(mode)
      ]);
      setAnalysisData(ana);
      setOptimizerData(opt);
    } catch (err) {
      console.error("Failed to load scenario data", err);
    }
  };

  // Step 2: "Check impact" primary action
  const handleRunAnalysis = async () => {
    setIsAnalyzing(true);
    try {
      await loadData(selectedTravelMode, selectedCandidateId);
      setSelectedState("G0_C");
      setFocusAreaTrigger((prev) => prev + 1);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Step 3: Run Candidate Comparison
  const handleRunCandidateComparison = async (candidateId: string) => {
    setIsComparing(true);
    setSelectedCandidateId(candidateId);
    try {
      await loadData(selectedTravelMode, candidateId);
      setSelectedState("G0_P_C_M");
      const cand = optimizerData?.all_evaluated_candidates.find((c) => c.candidate_id === candidateId);
      if (cand) setDrawerContent({ type: "candidate", data: cand });
    } finally {
      setIsComparing(false);
    }
  };

  // Step 1: Add hypothetical restriction
  const handleAddRoadRestriction = async (
    road: SelectedRoadInfo,
    direction: string = "both",
    mode: string = "motor_vehicle",
    phase: string = "Hypothetical Civil Workzone"
  ) => {
    try {
      const currentWays = analysisData?.disruption_definition.target_way_ids || [];
      const updatedWays = Array.from(new Set([...currentWays, road.way_id]));
      await updateDisruption({
        target_way_ids: updatedWays,
        name: `Restricted: ${road.name}`,
        direction,
        mode: mode || selectedTravelMode,
        phase
      });
      await loadData(selectedTravelMode, selectedCandidateId);
      setDrawerContent({ type: "road", data: road });
    } catch (err) {
      console.error("Failed to add restriction", err);
    }
  };

  // First-Open Experience: Try the Kakkanad Example
  const handleLoadKakkanadExample = () => {
    setSelectedRoad({
      way_id: "197827530",
      name: "Palarivattom - Kakkanad Road",
      highway: "secondary",
      oneway: "no"
    });
    setSelectedOriginId("orig_kakkanad_west");
    setSelectedState("G0_C");
    setCurrentStep("check_access");
    setFocusAreaTrigger((prev) => prev + 1);
  };

  const activeDisruptedWayIds = analysisData?.disruption_definition.target_way_ids || [];

  return (
    <>
      <Head>
        <title>SafeBuild — Construction Access Review | Kakkanad</title>
        <meta
          name="description"
          content="If this road is restricted during construction, how does community access change, and would another arrangement help?"
        />
      </Head>

      <div className="h-screen w-screen bg-[#F8FAFC] flex flex-col overflow-hidden font-sans text-slate-800">
        {/* TOP BAR */}
        <StudioTopBar
          selectedTravelMode={selectedTravelMode}
          onSelectTravelMode={(mode) => setSelectedTravelMode(mode)}
          is3DMode={is3DMode}
          onToggle3DMode={() => setIs3DMode(!is3DMode)}
          onOpenEvidenceModal={() => setIsEvidenceOpen(true)}
          onOpenAIModal={() => setIsAIOpen(true)}
          onLoadKakkanadExample={handleLoadKakkanadExample}
        />

        {/* MAIN BODY: LEFT COMPACT TASK PANEL + LARGE CENTER MAP */}
        <div className="flex-1 flex flex-col md:flex-row min-h-0 overflow-hidden relative">
          {/* COMPACT TASK PANEL (340px) */}
          <TaskPanel
            currentStep={currentStep}
            onSelectStep={(step) => {
              setCurrentStep(step);
              if (step === "choose_road") setSelectedState("G0_C");
              else if (step === "check_access") setSelectedState("G0_C");
              else if (step === "compare_arrangement") setSelectedState("G0_P_C_M");
            }}
            roadsCatalog={roadsCatalog}
            selectedRoad={selectedRoad}
            onSelectRoadItem={(road) => {
              setSelectedRoad(road);
              setDrawerContent({ type: "road", data: road });
            }}
            onClearSelectedRoad={() => setSelectedRoad(null)}
            onAddRoadRestriction={(road, dir, mode, phase) => handleAddRoadRestriction(road, dir, mode, phase)}
            activeDisruptedWayIds={activeDisruptedWayIds}
            selectedTravelMode={selectedTravelMode}
            onSelectTravelMode={(mode) => setSelectedTravelMode(mode)}
            onRunAnalysis={handleRunAnalysis}
            isAnalyzing={isAnalyzing}
            origins={analysisData?.per_origin_results || []}
            selectedOriginId={selectedOriginId}
            onSelectOrigin={(id) => {
              setSelectedOriginId(id);
              const orig = analysisData?.per_origin_results.find((o) => o.origin_id === id);
              if (orig) setDrawerContent({ type: "origin", data: orig });
            }}
            facility={analysisData?.primary_facility || null}
            analysisSummary={analysisData?.summary || null}
            allCandidates={optimizerData?.all_evaluated_candidates || []}
            selectedCandidateId={selectedCandidateId}
            onSelectCandidate={(cid) => {
              setSelectedCandidateId(cid);
              const cand = optimizerData?.all_evaluated_candidates.find((c) => c.candidate_id === cid);
              if (cand) setDrawerContent({ type: "candidate", data: cand });
            }}
            onRunCandidateComparison={handleRunCandidateComparison}
            isComparing={isComparing}
            onLoadKakkanadExample={handleLoadKakkanadExample}
          />

          {/* LARGE MAP CANVAS */}
          <div className="flex-1 h-full min-w-0 relative flex flex-col">
            <MapCanvas
              origins={analysisData?.per_origin_results || []}
              selectedOriginId={selectedOriginId}
              onSelectOrigin={(id) => {
                setSelectedOriginId(id);
                const orig = analysisData?.per_origin_results.find((o) => o.origin_id === id);
                if (orig) setDrawerContent({ type: "origin", data: orig });
              }}
              selectedState={selectedState}
              facility={analysisData?.primary_facility || null}
              disruptedSegments={analysisData?.disrupted_segments || []}
              onSelectRoad={(road) => {
                setSelectedRoad(road);
                if (road) {
                  setDrawerContent({ type: "road", data: road });
                  if (currentStep !== "choose_road") {
                    setCurrentStep("choose_road");
                  }
                }
              }}
              selectedRoad={selectedRoad}
              selectedRoadWayId={selectedRoad?.way_id || null}
              focusAreaTrigger={focusAreaTrigger}
              onAddRoadRestriction={(road) => handleAddRoadRestriction(road)}
            />

            {/* CONTEXT DRAWER: Opens only on object selection */}
            <ContextDrawer
              content={drawerContent}
              onClose={() => setDrawerContent(null)}
              onAddRoadRestriction={(road) => handleAddRoadRestriction(road)}
              isRoadRestricted={selectedRoad ? activeDisruptedWayIds.includes(selectedRoad.way_id) : false}
            />
          </div>
        </div>

        {/* SECONDARY ACTION MODALS */}
        <EvidenceModal
          isOpen={isEvidenceOpen}
          onClose={() => setIsEvidenceOpen(false)}
          metadata={analysisData?.metadata || null}
          facility={analysisData?.primary_facility || null}
          runId={analysisData?.run_id || null}
        />

        <AIAnalystModal
          isOpen={isAIOpen}
          onClose={() => setIsAIOpen(false)}
          selectedTravelMode={selectedTravelMode}
          selectedCandidateId={selectedCandidateId}
        />
      </div>
    </>
  );
}
