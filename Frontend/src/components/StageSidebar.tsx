import { useState } from "react";

export default function StageSidebar({ currentStage }: { currentStage: string }) {
  const [loading, setLoading] = useState(false);

  // Function to move to next stage (Calls Backend)
  const advanceStage = async () => {
    setLoading(true);
    try {
      // 1. Call Backend to update DB (Backend logic handles the stage increments)
      await fetch("http://127.0.0.1:8000/user/1/advance_stage", { method: "POST" });
      
      // 2. Reload page to reflect changes (Simple but effective)
      window.location.reload();
    } catch (error) {
      console.error("Failed to advance stage:", error);
      setLoading(false);
    }
  };

  // Define the stages (Includes the hidden 'ADMITTED' stage for logic)
  const stages = [
    { id: "ONBOARDING", label: "1. Profile Setup" },
    { id: "SHORTLISTING", label: "2. University Search" },
    { id: "APPLICATION", label: "3. Applications" },
    { id: "ADMITTED", label: "4. Success!" }, // Hidden "Goal" stage
  ];

  return (
    <div className="w-64 bg-gray-900 text-white p-6 flex flex-col h-full rounded-l-xl justify-between">
      
      {/* Top Section: Visual Journey */}
      <div>
        <h2 className="text-xl font-bold mb-8 text-blue-400">Your Journey</h2>
        <div className="space-y-6">
          {/* We strictly slice(0,3) to hide the "Success" bubble from the list, 
              but the logic below still works because 'ADMITTED' is in the array */}
          {stages.slice(0, 3).map((stage) => {
            const isActive = stage.id === currentStage;
            // Check if this stage is "past" in the array order
            const isCompleted = stages.findIndex(s => s.id === stage.id) < stages.findIndex(s => s.id === currentStage);
            
            return (
              <div key={stage.id} className={`flex items-center gap-3 ${isActive ? "opacity-100" : "opacity-50"}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 
                  ${isActive ? "border-blue-500 bg-blue-500 text-white" : 
                    isCompleted ? "border-green-500 bg-green-500 text-black" : "border-gray-600 text-gray-500"}`}
                >
                  {isCompleted ? "✓" : isActive ? "●" : "🔒"}
                </div>
                <span className={`font-medium ${isActive ? "text-white" : "text-gray-400"}`}>{stage.label}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Bottom Section: Action Buttons */}
      <div className="pt-6 border-t border-gray-700">
        <p className="text-xs text-gray-500 mb-2">
            Status: <span className="text-yellow-400">{currentStage}</span>
        </p>
        
        {/* Stage 1 Button */}
        {currentStage === "ONBOARDING" && (
          <button 
            onClick={advanceStage} 
            disabled={loading} 
            className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded transition"
          >
            {loading ? "Updating..." : "Complete Profile ->"}
          </button>
        )}

        {/* Stage 3 Victory Button */}
        {currentStage === "APPLICATION" && (
            <button 
              onClick={advanceStage} 
              disabled={loading} 
              className="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 rounded transition font-bold"
            >
              {loading ? "Celebrating..." : "I Got Admitted! 🎉"}
            </button>
        )}

        {/* Victory Message (When fully admitted) */}
        {currentStage === "ADMITTED" && (
            <div className="text-center p-2 bg-green-900 rounded border border-green-500">
                <p className="text-sm text-green-300 font-bold">🎉 CONGRATULATIONS! 🎓</p>
            </div>
        )}
      </div>

    </div>
  );
}