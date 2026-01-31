"use client";

import { useState, useEffect } from "react";
import ChatInterface from "../components/ChatInterface";
import StageSidebar from "../components/StageSidebar";
// 👇 IMPORT THE NEW PANEL
import ShortlistPanel from "../components/ShortlistPanel"; 

export default function Home() {
  const [stage, setStage] = useState("LOADING...");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/user/1/stage")
      .then((res) => res.json())
      .then((data) => setStage(data.stage))
      .catch((err) => console.error(err));
  }, []);

  return (
    <main className="flex min-h-screen bg-gray-100 p-8 items-center justify-center">
      {/* 👇 FLEX CONTAINER KEEPS EVERYTHING IN A ROW */}
      <div className="flex w-full max-w-7xl h-[85vh] bg-white rounded-xl shadow-2xl overflow-hidden">
        
        {/* 1. LEFT: Journey Sidebar */}
        <StageSidebar currentStage={stage} />

        {/* 2. MIDDLE: Chat Interface */}
        <div className="flex-1 flex flex-col border-r border-gray-100">
            <header className="p-6 border-b bg-white z-10">
                <h1 className="text-2xl font-bold text-gray-800">AI Study Counsellor</h1>
                <p className="text-sm text-gray-500">Guided Decision Support System</p>
            </header>
            
            <div className="flex-1 p-6 overflow-hidden bg-white">
                <ChatInterface />
            </div>
        </div>

        {/* 3. RIGHT: Shortlist Panel (This was missing!) */}
        <ShortlistPanel currentStage={stage} />

      </div>
    </main>
  );
}