import React, { useState } from "react";
import Game from "./components/Game/Game";
import { useSelector, useDispatch } from "react-redux";
import { actions } from "./store/reducer";
import { createGame } from "./api";

const App = () => {
  const { gameId } = useSelector((state) => state);
  const [name, setName] = useState("");

  const dispatch = useDispatch();

  const onNameChange = (name) => {
    setName(name);
  };

  const handleNewGame = async () => {
    try {
      const game = await createGame(name);
      console.log(game);
      dispatch(
        actions.startGame({
          gameId: game.id,
          playerName: name,
        })
      );
    } catch (error) {
      console.error("Failed to start game:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="Title">Bowling</h1>
      </header>
      {gameId ? (
        <Game />
      ) : (
        <div>
          <input
            type="text"
            placeholder="Enter player name"
            value={name}
            onChange={(e) => onNameChange(e.target.value)}
          />
          <button onClick={handleNewGame}>Start Game</button>
        </div>
      )}
    </div>
  );
};

export default App;
