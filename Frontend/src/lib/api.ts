// Frontend/src/lib/api.ts

// 🟢 FORCE the Render URL. Do not use localhost.
const API_URL = "https://ai-counsellor-yw5v.onrender.com";

export async function chatWithAI(message: string, userId: string = "user_1") {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        message: message,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to connect to AI Counsellor");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

// Add other functions here if you have them (like getting history)
export async function getHistory(userId: string = "user_1") {
    const response = await fetch(`${API_URL}/history/${userId}`);
    return await response.json();
}