import apiClient from "./client";

export function fetchChatbotSummary({ place_id = null, question } = {}) {
  return apiClient
    .post("/chatbot/summary", { place_id, question })
    .then((res) => res.data);
}
