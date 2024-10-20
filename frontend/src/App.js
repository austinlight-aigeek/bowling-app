import React, { useState } from "react";
import GameForm from "./components/GameForm";
import RollForm from "./components/RollForm";
import ScoreDisplay from "./components/ScoreDisplay";
import SummaryDisplay from "./components/SummaryDisplay";

const App = () => {
  const [gameId, setGameId] = useState(null);

  return (
    <div>
      <h1>Bowling Game</h1>
      <GameForm setGameId={setGameId} />
      {gameId && (
        <>
          <RollForm gameId={gameId} />
          <ScoreDisplay gameId={gameId} />
          <SummaryDisplay gameId={gameId} />
        </>
      )}
    </div>
  );
};

export default App;
