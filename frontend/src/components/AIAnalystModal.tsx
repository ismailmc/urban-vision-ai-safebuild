import React, { useState } from "react";
import { X, Sparkles, Send } from "lucide-react";
import { askAIAnalyst } from "@/lib/api";

interface AIAnalystModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedTravelMode: string;
  selectedCandidateId: string;
}

export const AIAnalystModal: React.FC<AIAnalystModalProps> = ({
  isOpen,
  onClose,
  selectedTravelMode,
  selectedCandidateId
}) => {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSend = async (q: string) => {
    if (!q.trim()) return;
    setLoading(true);
    setAnswer(null);
    try {
      const res = await askAIAnalyst(q, selectedTravelMode, selectedCandidateId);
      setAnswer(res.analysis);
    } catch {
      setAnswer("Could not reach analyst backend. Verify the API server on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    "Explain how restricting this road changes hospital access.",
    "Why is the contraflow candidate not verified?",
    "Which community anchor experiences the highest route increase?",
    "Does this scenario create any newly unreachable points?"
  ];

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white border border-slate-200 rounded-2xl max-w-lg w-full shadow-2xl overflow-hidden text-slate-800">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-teal-700" />
            <span className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              Explain with AI — Grounded Routing Analyst
            </span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 cursor-pointer">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-4 text-xs">
          <p className="text-slate-600 leading-relaxed">
            Responses are verified against deterministic Dijkstra shortest-path calculations across the authentic Kakkanad network. The system never fabricates resident numbers, ambulance timing, or false approvals.
          </p>

          <div className="space-y-1.5">
            <label className="font-semibold text-slate-700 block text-[11px] uppercase tracking-wide">
              Quick Verified Questions:
            </label>
            <div className="space-y-1">
              {samplePrompts.map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => {
                    setQuery(p);
                    handleSend(p);
                  }}
                  className="w-full text-left p-2 bg-slate-50 hover:bg-teal-50 border border-slate-200 hover:border-teal-300 rounded-lg text-slate-700 text-xs transition cursor-pointer"
                >
                  • {p}
                </button>
              ))}
            </div>
          </div>

          <div className="flex items-center space-x-2 pt-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSend(query);
              }}
              placeholder="Ask an access or alternative question..."
              className="flex-1 p-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-1 focus:ring-teal-500"
            />
            <button
              type="button"
              disabled={loading || !query.trim()}
              onClick={() => handleSend(query)}
              className="py-2 px-3 bg-teal-700 hover:bg-teal-800 disabled:bg-slate-300 text-white rounded-xl text-xs font-bold shadow-sm transition flex items-center space-x-1 cursor-pointer"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Ask</span>
            </button>
          </div>

          {loading && (
            <div className="p-3 bg-slate-50 rounded-xl text-center text-slate-500 italic">
              Traversing directed graph shortest paths...
            </div>
          )}

          {answer && (
            <div className="p-3 bg-teal-50/70 border border-teal-200 rounded-xl text-slate-900 leading-relaxed space-y-1">
              <div className="font-bold text-teal-900 text-xs">Grounded Analysis:</div>
              <div>{answer}</div>
            </div>
          )}
        </div>

        <div className="px-5 py-3 bg-slate-50 border-t border-slate-100 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
