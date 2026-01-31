import { useState, useEffect } from "react";

interface ShortlistItem {
  id: number;
  university: string;
  category: string;
  is_locked: boolean;
}

export default function ShortlistPanel({ currentStage }: { currentStage: string }) {
  const [list, setList] = useState<ShortlistItem[]>([]);

  // Refresh list every 2 seconds (Simple polling to see AI updates instantly)
  useEffect(() => {
    const fetchList = async () => {
        try {
            const res = await fetch("http://127.0.0.1:8000/user/1/shortlist");
            const data = await res.json();
            setList(data);
        } catch (e) {
            console.error("Fetch error", e);
        }
    };
    fetchList(); // Initial call
    const interval = setInterval(fetchList, 2000); // Poll every 2s
    return () => clearInterval(interval);
  }, []);

  const lockUni = async (id: number) => {
    await fetch(`http://127.0.0.1:8000/user/1/lock/${id}`, { method: "POST" });
    window.location.reload(); // Reload to update stage
  };

  return (
    <div className="w-80 bg-white border-l p-6 flex flex-col h-full">
      <h2 className="text-xl font-bold mb-6 text-gray-800">Your Shortlist</h2>

      <div className="space-y-4 overflow-y-auto flex-1">
        {list.length === 0 ? (
          <p className="text-gray-400 text-sm italic">Ask AI to add universities...</p>
        ) : (
          list.map((item) => (
            <div key={item.id} className={`p-4 rounded-lg border ${item.is_locked ? "bg-green-50 border-green-500" : "bg-gray-50 border-gray-200"}`}>
              <div className="flex justify-between items-start">
                <h3 className="font-bold text-gray-800">{item.university}</h3>
                <span className={`text-[10px] px-2 py-1 rounded font-bold ${
                    item.category === "DREAM" ? "bg-purple-100 text-purple-700" : 
                    item.category === "SAFE" ? "bg-green-100 text-green-700" : "bg-blue-100 text-blue-700"
                }`}>
                    {item.category}
                </span>
              </div>

              {/* Lock Button (Only visible in Stage 2) */}
              {!item.is_locked && currentStage === "SHORTLISTING" && (
                <button 
                    onClick={() => lockUni(item.id)}
                    className="mt-3 w-full text-xs bg-gray-900 text-white py-2 rounded hover:bg-gray-700 transition"
                >
                    Lock & Apply 🔒
                </button>
              )}

              {item.is_locked && (
                <div className="mt-2 text-xs text-green-700 font-bold flex items-center gap-1">
                    <span>✓ Application Track Started</span>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}