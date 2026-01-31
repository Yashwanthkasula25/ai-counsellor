// frontend/src/lib/api.ts

const API_BASE_URL = "http://127.0.0.1:8000"; // Your FastAPI URL

export interface ChatResponse {
  response: string;
  action_taken?: {
    tool_use: string;
    university_name: string;
    category: string;
    reasoning: string;
  };
}

export async function sendMessage(userId: number, message: string): Promise<ChatResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        message: message,
      }),
    });

    if (!res.ok) {
      throw new Error(`Server Error: ${res.statusText}`);
    }

    return await res.json();
  } catch (error) {
    console.error("API Call Failed:", error);
    return { response: "⚠️ Error connecting to AI Counsellor." };
  }
}