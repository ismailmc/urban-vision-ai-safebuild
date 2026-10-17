import React, { useEffect, useRef, useState } from "react";
import * as maplibregl from "maplibre-gl";
import { OriginResult, AnalyticalState, Facility, DisruptedSegment } from "@/types";
import { fetchBuildings, fetchRoadGeometries } from "@/lib/api";
import { Layers, Maximize2, Split, Box, Compass, Info } from "lucide-react";

export interface SelectedRoadInfo {
  way_id: string;
  name: string;
  highway: string;
  oneway: string;
}

interface MapCanvasProps {
  origins: OriginResult[];
  selectedOriginId: string | null;
  onSelectOrigin: (id: string) => void;
  selectedState: AnalyticalState;
  facility: Facility | null;
  disruptedSegments?: DisruptedSegment[];
  onSelectRoad?: (road: SelectedRoadInfo | null) => void;
  selectedRoad?: SelectedRoadInfo | null;
  selectedRoadWayId?: string | null;
  focusAreaTrigger?: number;
  onAddRoadRestriction?: (road: SelectedRoadInfo) => void;
}

export const MapCanvas: React.FC<MapCanvasProps> = ({
  origins,
  selectedOriginId,
  onSelectOrigin,
  selectedState,
  facility,
  disruptedSegments = [],
  onSelectRoad,
  selectedRoadWayId,
  focusAreaTrigger,
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const [showComparisonSplit, setShowComparisonSplit] = useState(false);
  const [showWorkzones, setShowWorkzones] = useState(true);
  const [is3DMode, setIs3DMode] = useState(false);
  const [showBuildings, setShowBuildings] = useState(true);

  // GeoJSON caches
  const buildingsGeojsonRef = useRef<GeoJSON.FeatureCollection | null>(null);
  const roadsGeojsonRef = useRef<GeoJSON.FeatureCollection | null>(null);

  // Use Wikimedia / OpenStreetMap standard public tiles without API key restrictions
  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    // Explicitly set workerUrl to avoid Worker failed to load error in Next.js bundle
    try {
      if (typeof window !== "undefined") {
        (maplibregl as unknown as { setWorkerUrl?: (u: string) => void }).setWorkerUrl?.("/maplibre-gl-worker.js");
      }
    } catch {
      // fallback
    }

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm_tiles: {
            type: "raster",
            tiles: [
              "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            ],
            tileSize: 256,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          }
        },
        layers: [
          {
            id: "osm-base",
            type: "raster",
            source: "osm_tiles",
            minzoom: 0,
            maxzoom: 19
          }
        ]
      },
      center: [76.342, 10.023],
      zoom: 14.3,
      pitch: 0,
      bearing: 0
    });

    map.addControl(new maplibregl.NavigationControl({ showCompass: true }), "bottom-right");
    mapRef.current = map;

    // Load authentic building footprints and road centerlines
    map.on("load", async () => {
      try {
        const [bData, rData] = await Promise.all([
          fetchBuildings().catch(() => null),
          fetchRoadGeometries().catch(() => null)
        ]);

        if (bData && mapRef.current) {
          buildingsGeojsonRef.current = bData;
          if (!mapRef.current.getSource("osm-buildings")) {
            mapRef.current.addSource("osm-buildings", { type: "geojson", data: bData });
            mapRef.current.addLayer({
              id: "osm-buildings-extrusion",
              type: "fill-extrusion",
              source: "osm-buildings",
              paint: {
                "fill-extrusion-color": [
                  "case",
                  ["==", ["get", "is_estimated"], false], "#94A3B8",
                  "#CBD5E1"
                ],
                "fill-extrusion-height": ["get", "height"],
                "fill-extrusion-base": 0,
                "fill-extrusion-opacity": 0.75
              },
              layout: {
                visibility: "none"
              }
            });
          }
        }

        if (rData && mapRef.current) {
          roadsGeojsonRef.current = rData;
          if (!mapRef.current.getSource("selectable-roads")) {
            mapRef.current.addSource("selectable-roads", { type: "geojson", data: rData });
            // Transparent wide stroke for easy clicking
            mapRef.current.addLayer({
              id: "selectable-roads-hitbox",
              type: "line",
              source: "selectable-roads",
              paint: {
                "line-color": "#3B82F6",
                "line-width": 12,
                "line-opacity": 0.01
              }
            });
            // Visible subtle centerline
            mapRef.current.addLayer({
              id: "selectable-roads-visible",
              type: "line",
              source: "selectable-roads",
              paint: {
                "line-color": "#64748B",
                "line-width": 1.5,
                "line-opacity": 0.35
              }
            });
            // Highlighted road layer
            mapRef.current.addLayer({
              id: "selected-road-highlight",
              type: "line",
              source: "selectable-roads",
              paint: {
                "line-color": "#F59E0B",
                "line-width": 6,
                "line-opacity": 0.95
              },
              filter: ["==", "way_id", ""]
            });

            // Road click event
            mapRef.current.on("click", "selectable-roads-hitbox", (e) => {
              if (e.features && e.features[0] && onSelectRoad) {
                const props = e.features[0].properties;
                onSelectRoad({
                  way_id: String(props.way_id),
                  name: String(props.name || "Unnamed road"),
                  highway: String(props.highway || "road"),
                  oneway: String(props.oneway || "no")
                });
              }
            });

            mapRef.current.on("mouseenter", "selectable-roads-hitbox", () => {
              if (mapRef.current) mapRef.current.getCanvas().style.cursor = "pointer";
            });
            mapRef.current.on("mouseleave", "selectable-roads-hitbox", () => {
              if (mapRef.current) mapRef.current.getCanvas().style.cursor = "";
            });
          }
        }
      } catch (err) {
        console.warn("Geographic vector layers error:", err);
      }
    });

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [onSelectRoad]);

  // Update selected road highlight filter
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !map.isStyleLoaded()) return;
    if (map.getLayer("selected-road-highlight")) {
      map.setFilter("selected-road-highlight", ["==", "way_id", selectedRoadWayId || ""]);
    }
  }, [selectedRoadWayId]);

  // Handle 3D / 2D toggle
  const toggle3DMode = () => {
    const map = mapRef.current;
    if (!map) return;
    const nextState = !is3DMode;
    setIs3DMode(nextState);

    if (nextState) {
      map.easeTo({
        pitch: 52,
        bearing: -22,
        duration: 900
      });
      if (map.getLayer("osm-buildings-extrusion")) {
        map.setLayoutProperty("osm-buildings-extrusion", "visibility", showBuildings ? "visible" : "none");
      }
    } else {
      map.easeTo({
        pitch: 0,
        bearing: 0,
        duration: 900
      });
      if (map.getLayer("osm-buildings-extrusion")) {
        map.setLayoutProperty("osm-buildings-extrusion", "visibility", "none");
      }
    }
  };

  // Toggle buildings extrusion visibility
  const toggleBuildings = () => {
    const map = mapRef.current;
    if (!map || !map.getLayer("osm-buildings-extrusion")) return;
    const nextVal = !showBuildings;
    setShowBuildings(nextVal);
    map.setLayoutProperty("osm-buildings-extrusion", "visibility", (nextVal && is3DMode) ? "visible" : "none");
  };

  // Focus affected study area / corridor
  const handleFocusStudyArea = () => {
    mapRef.current?.flyTo({
      center: [76.345, 10.024],
      zoom: 15.2,
      pitch: is3DMode ? 45 : 0,
      essential: true
    });
  };

  // Reset view
  const handleResetView = () => {
    mapRef.current?.flyTo({
      center: [76.342, 10.023],
      zoom: 14.3,
      pitch: 0,
      bearing: 0,
      essential: true
    });
    setIs3DMode(false);
    if (mapRef.current?.getLayer("osm-buildings-extrusion")) {
      mapRef.current.setLayoutProperty("osm-buildings-extrusion", "visibility", "none");
    }
  };

  // Focus trigger reaction
  useEffect(() => {
    if (focusAreaTrigger && focusAreaTrigger > 0) {
      handleFocusStudyArea();
    }
  }, [focusAreaTrigger]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    if (map.isStyleLoaded()) {
      renderLayers();
    } else {
      map.on("load", renderLayers);
    }

    function renderLayers() {
      if (!map) return;

      const selectedOrigin = origins.find(o => o.origin_id === selectedOriginId) || origins[0];

      // 1. Comparison Route (Baseline G0)
      const baselineRoute = selectedOrigin?.routes["G0"];
      const baseCoords = baselineRoute?.geometry?.map(([lat, lon]) => [lon, lat]) || [];
      const baseGeojson: GeoJSON.FeatureCollection = {
        type: "FeatureCollection",
        features: showComparisonSplit ? [
          {
            type: "Feature",
            geometry: { type: "LineString", coordinates: baseCoords },
            properties: { type: "baseline" }
          }
        ] : []
      };

      if (map.getSource("baseline-route")) {
        (map.getSource("baseline-route") as maplibregl.GeoJSONSource).setData(baseGeojson);
      } else {
        map.addSource("baseline-route", { type: "geojson", data: baseGeojson });
        map.addLayer({
          id: "baseline-route-casing",
          type: "line",
          source: "baseline-route",
          layout: { "line-join": "round", "line-cap": "round" },
          paint: { "line-color": "#FFFFFF", "line-width": 6, "line-opacity": 0.95 }
        });
        map.addLayer({
          id: "baseline-route-line",
          type: "line",
          source: "baseline-route",
          layout: { "line-join": "round", "line-cap": "round" },
          paint: {
            "line-color": "#0D9488",
            "line-width": 4,
            "line-dasharray": [2, 2],
            "line-opacity": 0.95
          }
        });
      }

      // 2. Active Scenario Route (e.g. G0_C)
      const activeRoute = selectedOrigin?.routes[selectedState];
      const activeCoords = activeRoute?.geometry?.map(([lat, lon]) => [lon, lat]) || [];
      const activeGeojson: GeoJSON.FeatureCollection = {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            geometry: { type: "LineString", coordinates: activeCoords },
            properties: { type: "active" }
          }
        ]
      };

      if (map.getSource("active-route")) {
        (map.getSource("active-route") as maplibregl.GeoJSONSource).setData(activeGeojson);
      } else {
        map.addSource("active-route", { type: "geojson", data: activeGeojson });
        map.addLayer({
          id: "route-casing",
          type: "line",
          source: "active-route",
          layout: { "line-join": "round", "line-cap": "round" },
          paint: { "line-color": "#FFFFFF", "line-width": 7, "line-opacity": 0.95 }
        });
        map.addLayer({
          id: "route-line",
          type: "line",
          source: "active-route",
          layout: { "line-join": "round", "line-cap": "round" },
          paint: {
            "line-color": selectedState === "G0" ? "#0D9488" : selectedState.includes("C") ? "#E11D48" : "#2563EB",
            "line-width": 4,
            "line-opacity": 1.0
          }
        });
      }

      // 3. Work-zone / Disrupted Segments
      const disruptionFeatures: GeoJSON.Feature[] = [];
      if (showWorkzones) {
        disruptedSegments.forEach(seg => {
          if (seg.geometry && seg.geometry.length > 1) {
            disruptionFeatures.push({
              type: "Feature",
              geometry: {
                type: "LineString",
                coordinates: seg.geometry.map(([lat, lon]) => [lon, lat])
              },
              properties: { name: seg.name, way_id: seg.way_id }
            });
          }
        });
      }

      const disruptionGeojson: GeoJSON.FeatureCollection = {
        type: "FeatureCollection",
        features: disruptionFeatures
      };

      if (map.getSource("disrupted-segments")) {
        (map.getSource("disrupted-segments") as maplibregl.GeoJSONSource).setData(disruptionGeojson);
      } else {
        map.addSource("disrupted-segments", { type: "geojson", data: disruptionGeojson });
        map.addLayer({
          id: "disruption-casing",
          type: "line",
          source: "disrupted-segments",
          paint: {
            "line-color": "#FEF3C7",
            "line-width": 9,
            "line-opacity": 0.85
          }
        });
        map.addLayer({
          id: "disruption-line",
          type: "line",
          source: "disrupted-segments",
          paint: {
            "line-color": "#D97706",
            "line-width": 4.5,
            "line-dasharray": [1.5, 1.5],
            "line-opacity": 1.0
          }
        });
      }

      // 4. Origins and Destination Entrance Markers
      const markersFeatures: GeoJSON.Feature[] = [];

      // Destination Hospital Entrance
      if (facility) {
        markersFeatures.push({
          type: "Feature",
          geometry: { type: "Point", coordinates: [facility.lon, facility.lat] },
          properties: {
            id: facility.id,
            name: facility.name,
            entity_type: "facility"
          }
        });
      }

      // Residential Community Sampling Anchors
      origins.forEach(o => {
        markersFeatures.push({
          type: "Feature",
          geometry: { type: "Point", coordinates: [o.origin_coords[1], o.origin_coords[0]] },
          properties: {
            id: o.origin_id,
            name: o.origin_name,
            entity_type: "origin",
            is_selected: o.origin_id === selectedOriginId,
            detour_m: o.construction_delta_m || 0
          }
        });
      });

      const markersGeojson: GeoJSON.FeatureCollection = {
        type: "FeatureCollection",
        features: markersFeatures
      };

      if (map.getSource("map-entities")) {
        (map.getSource("map-entities") as maplibregl.GeoJSONSource).setData(markersGeojson);
      } else {
        map.addSource("map-entities", { type: "geojson", data: markersGeojson });

        map.addLayer({
          id: "entity-markers",
          type: "circle",
          source: "map-entities",
          paint: {
            "circle-radius": [
              "case",
              ["==", ["get", "entity_type"], "facility"], 10,
              ["==", ["get", "is_selected"], true], 9,
              7
            ],
            "circle-color": [
              "case",
              ["==", ["get", "entity_type"], "facility"], "#0F766E",
              [">", ["get", "detour_m"], 100], "#E11D48",
              "#2563EB"
            ],
            "circle-stroke-width": 2.5,
            "circle-stroke-color": "#FFFFFF"
          }
        });

        // Click interaction
        map.on("click", "entity-markers", (e) => {
          if (!e.features || !e.features[0]) return;
          const props = e.features[0].properties;
          if (props?.entity_type === "origin") {
            onSelectOrigin(props.id);
          }
        });

        map.on("mouseenter", "entity-markers", () => {
          map.getCanvas().style.cursor = "pointer";
        });
        map.on("mouseleave", "entity-markers", () => {
          map.getCanvas().style.cursor = "";
        });
      }
    }
  }, [origins, selectedOriginId, selectedState, facility, disruptedSegments, showComparisonSplit, showWorkzones, onSelectOrigin]);

  const selectedOrigin = origins.find(o => o.origin_id === selectedOriginId) || origins[0];

  return (
    <div className="relative w-full h-full min-h-[480px] rounded-xl overflow-hidden border border-slate-200/90 shadow-sm bg-slate-100">
      <div ref={mapContainer} className="w-full h-full" />
      
      {/* Top Floating Map Controls Toolbar */}
      <div className="absolute top-4 right-4 z-10 flex flex-wrap items-center justify-end gap-2 max-w-[calc(100%-300px)]">
        {/* 2D / 3D Toggle */}
        <button
          onClick={toggle3DMode}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 shadow-sm transition-all border ${
            is3DMode
              ? "bg-slate-900 text-white border-slate-950 shadow-slate-900/30"
              : "bg-white text-slate-700 hover:bg-slate-50 border-slate-200"
          }`}
          title="Toggle 2D / 3D perspective"
        >
          <Box className="w-3.5 h-3.5" />
          <span>{is3DMode ? "3D View Active" : "2D View"}</span>
        </button>

        {is3DMode && (
          <button
            onClick={toggleBuildings}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 shadow-sm transition-all border ${
              showBuildings
                ? "bg-indigo-600 text-white border-indigo-700"
                : "bg-white text-slate-700 hover:bg-slate-50 border-slate-200"
            }`}
            title="Toggle illustrative building extrusions"
          >
            <span>{showBuildings ? "Buildings Extruded" : "Buildings Flat"}</span>
          </button>
        )}

        <button
          onClick={() => setShowComparisonSplit(!showComparisonSplit)}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 shadow-sm transition-all border ${
            showComparisonSplit
              ? "bg-teal-700 text-white border-teal-800 shadow-teal-900/20"
              : "bg-white text-slate-700 hover:bg-slate-50 border-slate-200"
          }`}
          title="Toggle baseline route comparison overlay"
        >
          <Split className="w-3.5 h-3.5" />
          <span>{showComparisonSplit ? "Comparing: Baseline + " + selectedState : "Synchronize Baseline Route"}</span>
        </button>

        <button
          onClick={() => setShowWorkzones(!showWorkzones)}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 shadow-sm transition-all border ${
            showWorkzones
              ? "bg-amber-600 text-white border-amber-700"
              : "bg-white text-slate-700 hover:bg-slate-50 border-slate-200"
          }`}
          title="Toggle workzone layer visibility"
        >
          <Layers className="w-3.5 h-3.5" />
          <span>{showWorkzones ? "Workzone Visible" : "Workzone Hidden"}</span>
        </button>

        <button
          onClick={handleFocusStudyArea}
          className="px-3 py-1.5 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-lg text-xs font-semibold shadow-sm transition flex items-center space-x-1"
          title="Focus affected study corridor"
        >
          <Compass className="w-3.5 h-3.5 text-teal-600" />
          <span>Focus Area</span>
        </button>

        <button
          onClick={handleResetView}
          className="p-1.5 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-lg shadow-sm transition"
          title="Reset Study Extent (2D Fallback)"
        >
          <Maximize2 className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* 3D Extrusion Assumption Callout (Visible in 3D Mode, positioned neatly bottom-right) */}
      {is3DMode && (
        <div className="absolute bottom-16 right-4 bg-slate-900/95 backdrop-blur-md border border-slate-800 text-slate-200 rounded-xl p-3 text-[11px] shadow-xl max-w-[280px] z-10 leading-relaxed animate-in fade-in slide-in-from-bottom-2 duration-200">
          <div className="flex items-center space-x-1.5 text-amber-400 font-bold mb-1">
            <Info className="w-3.5 h-3.5 shrink-0" />
            <span>Illustrative 3D Massing Notice</span>
          </div>
          <p className="text-slate-300">
            Building heights reflect sourced OSM tags where recorded, or an illustrative 8m default height assumption.
          </p>
          <div className="text-[10px] text-amber-300/90 mt-1 pt-1 border-t border-slate-800">
            Assumption visible: Illustrative only. Does not infer occupancy, engineering properties, obstruction, or legal rights of way.
          </div>
        </div>
      )}

      {/* Selected Object Context Callout: Origin */}
      {selectedOrigin && (
        <div className="absolute top-4 left-4 bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-xl p-3 shadow-sm z-10 max-w-[280px]">
          <div className="text-[11px] font-semibold uppercase tracking-wider text-teal-800">Selected Community Anchor</div>
          <div className="font-bold text-slate-900 text-sm mt-0.5">{selectedOrigin.origin_name}</div>
          <div className="flex items-center justify-between text-xs mt-2 pt-2 border-t border-slate-100">
            <span className="text-slate-500">Modeled Detour:</span>
            <span className={`font-mono font-bold ${selectedOrigin.construction_delta_m && selectedOrigin.construction_delta_m > 0 ? "text-rose-600" : "text-teal-700"}`}>
              {selectedOrigin.construction_delta_m ? `+${selectedOrigin.construction_delta_m} m` : "0 m"}
            </span>
          </div>
        </div>
      )}

      {/* Selected Object Context Callout: Clicked Road */}
      {/* High-Contrast Legible Map Legend */}
      <div className="absolute bottom-8 left-4 bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-xl p-3 text-xs shadow-sm space-y-2 z-10 min-w-[220px]">
        <div className="font-bold text-slate-800 border-b border-slate-100 pb-1 flex items-center justify-between">
          <span>Geographic Legend</span>
          <span className="text-[10px] text-slate-400 font-mono">EPSG:4326</span>
        </div>
        <div className="flex items-center space-x-2.5">
          <span className="w-3.5 h-3.5 rounded-full bg-teal-800 border-2 border-white shadow-sm inline-block shrink-0" />
          <span className="text-slate-700 font-medium">Sunrise Hospital (Destination)</span>
        </div>
        <div className="flex items-center space-x-2.5">
          <span className="w-3.5 h-3.5 rounded-full bg-rose-600 border-2 border-white shadow-sm inline-block shrink-0" />
          <span className="text-slate-700">Detoured Origin (&gt;100 m)</span>
        </div>
        <div className="flex items-center space-x-2.5">
          <span className="w-3.5 h-3.5 rounded-full bg-blue-600 border-2 border-white shadow-sm inline-block shrink-0" />
          <span className="text-slate-700">Preserved Origin</span>
        </div>
        {showWorkzones && (
          <div className="flex items-center space-x-2.5">
            <span className="w-5 h-2 bg-amber-500 rounded border border-amber-600 inline-block shrink-0" />
            <span className="text-slate-700">Workzone Restriction (C)</span>
          </div>
        )}
        <div className="flex items-center space-x-2.5 pt-1 border-t border-slate-100">
          <span className="w-5 h-1.5 bg-rose-600 rounded inline-block shrink-0" />
          <span className="text-slate-600 font-medium">Active State Route</span>
        </div>
        {showComparisonSplit && (
          <div className="flex items-center space-x-2.5">
            <span className="w-5 h-1 border-b-2 border-dashed border-teal-600 inline-block shrink-0" />
            <span className="text-teal-800 font-semibold">Baseline Route (G0)</span>
          </div>
        )}
      </div>
    </div>
  );
};
