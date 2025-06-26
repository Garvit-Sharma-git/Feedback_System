// src/api/http.js
import axios from "axios";

const api = axios.create({
  baseURL: "https://feedback-system-backend-39y1.onrender.com",
});

api.interceptors.request.use((config) => {
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    const user = JSON.parse(storedUser);
    config.headers["x-user-email"] = user.email;
  }
  return config;
});

export default api;
