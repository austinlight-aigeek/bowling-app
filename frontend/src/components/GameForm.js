import React, { useState } from "react";
import { createGame } from "../api"; // Import API function
import RollForm from "./RollForm";
import ScoreDisplay from "./ScoreDisplay";
import SummaryDisplay from "./SummaryDisplay"; // Import Summary Component

const GameForm = () => {
  const [playerName, setPlayerName] = useState(""); // To input player name
  const [gameId, setGameId] = useState(null); // To store the created game ID
  const [llmModel, setLlmModel] = useState("gpt"); // LLM selection
  const [showSummary, setShowSummary] = useState(false); // To trigger summary display

  const handleCreateGame = async (event) => {
    event.preventDefault();
    try {
      const data = await createGame(playerName); // Create game via API
      setGameId(data.game_id); // Store gameId for further actions
      alert(
        `Game created! Game ID: ${data.game_id}, Player: ${data.player_name}`
      );
    } catch (error) {
      console.error("Error creating game:", error);
    }
  };

  const handleReset = () => {
    // Reset the form and state to start a new game
    setPlayerName("");
    setGameId(null);
    setLlmModel("gpt");
    setShowSummary(false);
  };

  return (
    <div>
      {!gameId ? (
        // Show the game creation form if no game has been created yet
        <form onSubmit={handleCreateGame}>
          <label>
            Player Name:
            <input
              type="text"
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
              required
            />
          </label>
          <button type="submit">Create Game</button>
        </form>
      ) : (
        // Once the game is created, show the RollForm, ScoreDisplay, and SummaryDisplay components
        <div>
          <RollForm gameId={gameId} /> {/* RollForm to input rolls */}
          <ScoreDisplay gameId={gameId} /> {/* Show score updates */}
          {/* LLM Model Selection */}
          <label>
            Select LLM for Summary:
            <select
              value={llmModel}
              onChange={(e) => setLlmModel(e.target.value)}
            >
              <option value="gpt">GPT</option>
              <option value="bert">BERT</option>
              <option value="t5">T5</option>
              <option value="llama">LLaMA</option>
            </select>
          </label>
          {/* Button to trigger summary */}
          <button onClick={() => setShowSummary(true)}>Generate Summary</button>
          {/* Generate Summary with Selected LLM only when triggered */}
          {showSummary && <SummaryDisplay gameId={gameId} model={llmModel} />}
          {/* Reset Button */}
          <button onClick={handleReset}>Reset</button>
        </div>
      )}
    </div>
  );
};

export default GameForm;
