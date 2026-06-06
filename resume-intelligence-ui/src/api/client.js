import axios from "axios";

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
});

export const createCandidate = async (name, email) => {
  const response = await api.post("/candidates", { name, email });
  return response.data;
};

export const uploadResume = async (candidateId, file) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post(
    `/candidates/${candidateId}/resume`,
    formData,
    { headers: { "Content-Type": "multipart/form-data" } },
  );
  return response.data;
};

export const createJobDescription = async (title, company, descriptionText) => {
  const response = await api.post("/job-descriptions", {
    title,
    company,
    description_text: descriptionText,
  });
  return response.data;
};

export const bulkMatch = async (candidateId, jdIds) => {
  const response = await api.post("/match/bulk", {
    candidate_id: candidateId,
    job_description_ids: jdIds,
  });
  return response.data;
};

export const getMatchHistory = async (candidateId) => {
  const response = await api.get(`/candidates/${candidateId}/matches`);
  return response.data;
};
