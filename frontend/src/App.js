import React, { useState } from "react";
import RollForm from "./components/RollForm";
import ScoreDisplay from "./components/ScoreDisplay";
import { createGame, recordRoll, getScore, getSummary } from "./api";

function App() {
  const [gameId, setGameId] = useState(null);
  const [score, setScore] = useState(null);
  const [summary, setSummary] = useState("");
  const [error, setError] = useState("");

  const handleCreateGame = async () => {
    try {
      const data = await createGame();
      setGameId(data.game_id);
      setScore(null);
      setSummary("");
      setError("");
    } catch (err) {
      setError("Error creating game");
    }
  };

  const handleRecordRoll = async (pins) => {
    try {
      await recordRoll(gameId, pins);
      const data = await getScore(gameId);
      setScore(data.score);
      setError("");
    } catch (err) {
      setError("Error recording roll");
    }
  };

  const handleGetSummary = async (model) => {
    try {
      const data = await getSummary(gameId, model);
      setSummary(data.summary);
      setError("");
    } catch (err) {
      setError("Error fetching summary");
    }
  };

  return (
    <div className="App">
      <h1>Bowling Game</h1>
      {gameId ? (
        <div>
          <p>Game ID: {gameId}</p>
          <RollForm onSubmit={handleRecordRoll} />
          {score && <ScoreDisplay score={score} />}
          <button onClick={() => handleGetSummary("gpt")}>
            Get GPT Summary
          </button>
          <button onClick={() => handleGetSummary("bert")}>
            Get BERT Summary
          </button>
          {summary && <p>Game Summary: {summary}</p>}
        </div>
      ) : (
        <button onClick={handleCreateGame}>Start New Game</button>
      )}
      {error && <p>{error}</p>}
    </div>
  );
}

export default App;
