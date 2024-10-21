import React, { useEffect, useState } from "react";
import Game from "./components/Game/Game";
import { useSelector, useDispatch } from "react-redux";
import { actions } from "./store/reducer";
import { createGame } from "./api";
import "./App.css";

const App = () => {
  const { gameId } = useSelector((state) => state);
  const [player, setPlayer] = useState("");

  const dispatch = useDispatch();

  const onPlayerChange = (name) => {
    setPlayer(name);
  };

  const handleNewGame = async () => {
    try {
      const game = await createGame(player);
      dispatch(
        actions.startGame({
          gameId: game.id,
          playerName: player,
        })
      );
    } catch (error) {
      console.error("Failed to start game:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="title">Bowling Game</h1>
      </header>
      {gameId ? (
        <Game />
      ) : (
        <div>
          <input
            className="player"
            type="text"
            placeholder="Enter player name"
            value={player}
            onChange={(e) => onPlayerChange(e.target.value)}
          />
          <button onClick={handleNewGame}>Start Game</button>
        </div>
      )}
    </div>
  );
};

export default App;
