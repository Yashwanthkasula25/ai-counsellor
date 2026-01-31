// frontend/src/components/ChatInterface.tsx
"use client"; // Required for React State hooks

import { useState } from "react";
import { sendMessage } from "../lib/api";

export default function ChatInterface() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ sender: "user" | "ai"; text: string }[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    // 1. Add User Message to UI
    const userMsg = { sender: "user" as const, text: input };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setInput(""); // Clear input

    // 2. Call Backend
    const data = await sendMessage(1, input); // Hardcoded User ID 1 for now

    // 3. Add AI Response to UI
    const aiMsg = { sender: "ai" as const, text: data.response };
    setMessages((prev) => [...prev, aiMsg]);
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-[500px] border rounded-lg p-4 bg-gray-50">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-2">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-2 rounded-lg max-w-[80%] ${
              msg.sender === "user"
                ? "bg-blue-600 text-white self-end ml-auto"
                : "bg-white border text-gray-800 self-start"
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <div className="text-gray-400 text-sm">AI is thinking...</div>}
      </div>

      {/* Input Area */}
      <div className="flex gap-2">
        <input
          type="text"
          className="flex-1 border rounded p-2 text-black"
          placeholder="Ask about universities..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}