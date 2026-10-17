import React from "react";
import { Compass, Layers, Users, Sliders, FileText } from "lucide-react";

export type StudioTab = "explore" | "define" | "impact" | "alternatives" | "summary";

interface NavigationRailProps {
  activeTab: StudioTab;
  onSelectTab: (tab: StudioTab) => void;
}

export const NavigationRail: React.FC<NavigationRailProps> = ({ activeTab, onSelectTab }) => {
  const ITEMS: { id: StudioTab; stepNum: string; label: string; icon: React.ReactNode }[] = [
    { id: "explore", stepNum: "1", label: "Explore Area", icon: <Compass className="w-5 h-5" /> },
    { id: "define", stepNum: "2", label: "Define Change", icon: <Layers className="w-5 h-5" /> },
    { id: "impact", stepNum: "3", label: "See Impact", icon: <Users className="w-5 h-5" /> },
    { id: "alternatives", stepNum: "4", label: "Alternatives", icon: <Sliders className="w-5 h-5" /> },
    { id: "summary", stepNum: "5", label: "Summary", icon: <FileText className="w-5 h-5" /> }
  ];

  return (
    <nav className="w-20 bg-[#1C2541] border-r border-[#2E3856] flex flex-col items-center py-4 space-y-4 shrink-0 select-none z-20">
      <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center font-extrabold text-white text-base shadow-lg shadow-teal-950/40">
        SB
      </div>

      <div className="w-10 border-b border-[#2E3856] pt-1" />

      <div className="flex-1 flex flex-col space-y-2 w-full px-2">
        {ITEMS.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectTab(item.id)}
              className={`w-full py-2.5 px-1 rounded-xl flex flex-col items-center justify-center transition-all ${
                isActive
                  ? "bg-teal-600 text-white font-bold shadow-md shadow-teal-950/30"
                  : "text-slate-400 hover:text-slate-100 hover:bg-[#253256]"
              }`}
            >
              {item.icon}
              <span className="text-[10px] mt-1 tracking-tight leading-none text-center">
                {item.label}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
