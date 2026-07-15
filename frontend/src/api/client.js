import axios from "axios";

const apiClient = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}/api`,
});

apiClient.interceptors.response.use(
  (response) => {
    const warning = response.headers["x-chatbot-warning"];
    if (warning) {
      console.warn(`[Backend Warning] ${decodeURIComponent(warning)}`);
    }
    return response;
  },
  (error) => {
    error.detail =
      error.response?.data?.detail ??
      (error.response
        ? error.message
        : "서버에 연결할 수 없습니다. 잠시 후 다시 시도해 주세요.");
    return Promise.reject(error);
  },
);

export default apiClient;
