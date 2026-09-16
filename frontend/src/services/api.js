import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};

export const fetchDashboard = async () => {
  const res = await api.get('/dashboard');
  return res.data;
};

export const fetchAlerts = async (params = {}) => {
  const res = await api.get('/alerts', { params });
  return res.data;
};

export const fetchAlertDetail = async (id) => {
  const res = await api.get(`/alerts/${id}`);
  return res.data;
};

export const updateAlertStatus = async (id, status) => {
  const res = await api.post(`/alerts/${id}/status`, { status });
  return res.data;
};

export const fetchTrafficFlows = async (params = {}) => {
  const res = await api.get('/traffic', { params });
  return res.data;
};

export const fetchAnalytics = async () => {
  const res = await api.get('/analytics');
  return res.data;
};

export const fetchModelsInfo = async () => {
  const res = await api.get('/models');
  return res.data;
};

export const predictFlow = async (flowData) => {
  const res = await api.post('/predict', flowData);
  return res.data;
};

export const analyzePcapFile = async (file, onUploadProgress) => {
  const formData = new FormData();
  formData.append('file', file);

  const res = await api.post('/analyze-pcap', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress,
  });
  return res.data;
};

export default api;
