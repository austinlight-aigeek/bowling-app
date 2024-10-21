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

// Function to get the statistical data with player name
export const getStatistics = async (player) => {
  try {
    const response = await api.get(`/players/${player}/statistics`);
    return response.data; // Return the current score
  } catch (error) {
    console.error("Error fetching statistics:", error);
    throw error;
  }
};

// Fetch the player's historical game data
export const getPlayerHistory = async (playerName) => {
  try {
    // Call the API to get the player's history
    const response = await api.get(`/players/${playerName}/history`);

    // Return the list of games (including score, strikes, spares, and start time)
    return response.data.games;
  } catch (error) {
    console.error("Error fetching player history:", error);
    throw error;
  }
};

// Function to get a summary of the game using LLM
export const getSummary = async (gameId, llm) => {
  try {
    const response = await api.get(`/games/${gameId}/summary`, {
      params: { llm }, // Pass the LLM as a query parameter
    });
    return response.data.summary; // Return the summary from the response
  } catch (error) {
    console.error("Error fetching game summary:", error);
    throw error; // Rethrow the error to handle it in the component
  }
};
