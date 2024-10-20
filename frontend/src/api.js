import axios from "axios";

// Create an axios instance to communicate with the backend
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
});

// API call to create a new game
export const createGame = async (playerName) => {
  try {
    const response = await api.post("/games", { player_name: playerName });
    return response.data;
  } catch (error) {
    console.error("Error creating game:", error);
    throw error;
  }
};

// API call to record a roll for a game
export const recordRoll = async (gameId, pinsKnocked) => {
  try {
    const response = await api.post(`/games/${gameId}/rolls`, {
      pins_knocked: pinsKnocked,
    });
    return response.data;
  } catch (error) {
    console.error("Error recording roll:", error);
    throw error;
  }
};

// API call to get the current score of the game and game status
export const getScore = async (gameId) => {
  try {
    const response = await api.get(`/games/${gameId}/score`);
    return response.data; // Assume this response contains score, player name, and current frame
  } catch (error) {
    console.error("Error fetching score:", error);
    throw error;
  }
};

// API call to get the game summary using an LLM model
export const getSummary = async (gameId, model = "gpt") => {
  try {
    const response = await api.get(`/games/${gameId}/summary`, {
      params: { model },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching summary:", error);
    throw error;
  }
};

export default api;
