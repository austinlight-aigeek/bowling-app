import axios from "axios";

// Set up a default instance for axios
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000", // Adjust the baseURL as needed
  headers: {
    "Content-Type": "application/json",
  },
});

// Function to create a new game
export const createGame = async (playerName) => {
  try {
    const response = await api.post("/games", { player: playerName });
    return response.data;
  } catch (error) {
    console.error("Error creating game:", error);
    throw error;
  }
};

// Function to record a roll for a specific game
export const recordFrames = async (gameId, frames) => {
  try {
    const response = await api.post(`/games/${gameId}/rolls`, {
      gameId,
      frames,
    });

    return response.data; // Return the recorded roll details
  } catch (error) {
    console.error("Error recording roll:", error);
    throw error;
  }
};

// Function to get the current score for a specific game
export const getScore = async (gameId) => {
  try {
    const response = await api.get(`/games/${gameId}/score`);
    return response.data; // Return the current score
  } catch (error) {
    console.error("Error fetching score:", error);
    throw error;
  }
};

// Function to get a summary of the game using LLM
export const getSummary = async (gameId) => {
  try {
    const response = await api.get(`/games/${gameId}/summary`);
    return response.data; // Return the game summary
  } catch (error) {
    console.error("Error fetching summary:", error);
    throw error;
  }
};
