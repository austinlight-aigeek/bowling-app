import React, { useEffect, useState } from "react";
import { getScore } from "../api"; // Import the API function

const ScoreDisplay = ({ gameId }) => {
  const [score, setScore] = useState(null); // Store the current score

  const fetchScore = async () => {
    try {
      const data = await getScore(gameId); // Fetch current score from API
      setScore(data.score); // Update score
    } catch (error) {
      console.error("Error fetching score:", error);
    }
  };

  // Fetch score whenever gameId changes or when a roll is recorded
  useEffect(() => {
    fetchScore();
  }, [gameId]);

  return (
    <div>
      <h2>Game Score</h2>
      {score !== null ? <p>Current Score: {score}</p> : <p>Loading...</p>}
    </div>
  );
};

export default ScoreDisplay;
