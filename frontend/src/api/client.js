import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  timeout: 60000,
});

export const uploadResume = (sessionId, file) => {
  const form = new FormData();
  form.append("file", file);
  form.append("session_id", sessionId);
  return api.post("/upload/resume", form);
};

export const uploadJD = (sessionId, file) => {
  const form = new FormData();
  form.append("file", file);
  form.append("session_id", sessionId);
  return api.post("/upload/jd", form);
};

export const ragQuery = (sessionId, query) =>
  api.post("/rag/query", { session_id: sessionId, query });

export const startInterview = (sessionId, interviewType = "technical", numQuestions = 5) =>
  api.post("/interview/start", {
    session_id: sessionId,
    interview_type: interviewType,
    num_questions: numQuestions,
  });

export const submitAnswer = (sessionId, interviewId, answer) =>
  api.post("/interview/answer", {
    session_id: sessionId,
    interview_id: interviewId,
    answer,
  });

export const getFeedback = (sessionId, interviewId) =>
  api.get(`/feedback/${sessionId}/${interviewId}`);
