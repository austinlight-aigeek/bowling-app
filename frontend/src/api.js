import axios from "axios";

// Use the environment variable for the API URL
const API_URL = process.env.REACT_APP_API_URL;

export const createGame = async () => {
  const response = await axios.post(`${API_URL}/games`);
  return response.data;
};

export const recordRoll = async (gameId, pins) => {
  const response = await axios.post(`${API_URL}/games/${gameId}/rolls`, {
    pins,
  });
  return response.data;
};

export const getScore = async (gameId) => {
  const response = await axios.get(`${API_URL}/games/${gameId}/score`);
  return response.data;
};

export const getSummary = async (gameId, model) => {
  const response = await axios.get(`${API_URL}/games/${gameId}/summary`, {
    params: { model },
  });
  return response.data;
};
