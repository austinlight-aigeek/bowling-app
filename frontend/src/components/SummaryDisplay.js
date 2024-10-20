import React, { useState, useEffect } from "react";
import { getSummary, getScore } from "../api"; // Import API functions

const SummaryDisplay = ({ gameId, model }) => {
  const [summary, setSummary] = useState(""); // Store the LLM summary
  const [gameStatus, setGameStatus] = useState(null); // Store the current game status

  const fetchSummary = async () => {
    try {
      // Fetch the LLM summary from the backend
      const summaryData = await getSummary(gameId, model);
      setSummary(summaryData.summary);

      // Fetch the current game status (score, etc.)
      const scoreData = await getScore(gameId);
      setGameStatus(scoreData);
    } catch (error) {
      console.error("Error fetching summary:", error);
    }
  };

  useEffect(() => {
    fetchSummary(); // Fetch summary and game status when triggered
  }, [gameId, model]);

  return (
    <div>
      <h2>Game Summary</h2>

      {/* Display current game status */}
      {gameStatus && (
        <div>
          <p>Game ID: {gameId}</p>
          <p>Player Name: {gameStatus.player_name}</p>
          <p>Current Frame: {gameStatus.current_frame}</p>
          <p>Total Score: {gameStatus.score}</p>
        </div>
      )}

      {/* Display LLM-generated summary */}
      <p>{summary || "Loading summary..."}</p>
    </div>
  );
};

export default SummaryDisplay;
